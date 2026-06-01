from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .checker import run_all_checks
from .config import RuntimeConfig, load_runtime_config
from .evaluation import evaluate_suite
from .exporter import Exporter
from .llm_client import get_llm_client
from .parser import parse_trace
from .repair import local_repair
from .risk import assess_requirement_risk, assign_case_priorities
from .reranker import aggregate_score, select_best
from .schemas import CandidateEvaluation, ParsedTrace
from .state_model import build_state_model
from .utils import derive_stage_seed, extract_requirement_id, float_from_env, gold_spec_path, load_prompt, read_text, requirement_category


CANDIDATE_PROFILES = [
    {
        "label": "balanced_coverage",
        "instruction": "Prioritize balanced black-box coverage with at least one strong happy path and one representative negative case.",
    },
    {
        "label": "boundary_and_rules",
        "instruction": "Emphasize boundary values, threshold-adjacent cases, and tight decision-rule mapping without changing the output format.",
    },
    {
        "label": "negative_and_state_stress",
        "instruction": "Emphasize invalid partitions, illegal transitions, and failure-path coverage while keeping expected outputs concrete.",
    },
]


class ARGTestPipeline:
    def __init__(
        self,
        base_dir: Path | None = None,
        provider: str | None = None,
        model: str | None = None,
        candidates: int | None = None,
        openai_api_mode: str | None = None,
        seed: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        output_root: str | None = None,
    ) -> None:
        self.config: RuntimeConfig = load_runtime_config(
            base_dir=base_dir,
            provider=provider,
            model=model,
            candidates=candidates,
            openai_api_mode=openai_api_mode,
            seed=seed,
            temperature=temperature,
            top_p=top_p,
            output_root=output_root,
        )
        self.client = get_llm_client(
            self.config.provider,
            self.config.model,
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL'),
            timeout=float_from_env('OPENAI_TIMEOUT_SECONDS'),
            api_mode=self.config.openai_api_mode,
            seed=self.config.seed,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
        )
        self.exporter = Exporter(self.config.paths.artifacts, self.config.paths.outputs)

    def _compose_prompt(self, prompt_name: str, replacements: dict[str, str]) -> str:
        system = load_prompt(self.config.paths.prompts / 'system_prompt.txt')
        user = load_prompt(self.config.paths.prompts / prompt_name, replacements)
        return f"{system}\n\n{user}".strip()

    def _candidate_profile(self, index: int) -> dict[str, str]:
        return CANDIDATE_PROFILES[index % len(CANDIDATE_PROFILES)]

    def _normalize_review_guidance(
        self,
        *,
        forced_techniques: list[str] | None = None,
        coverage_items: list[str] | None = None,
        designer_review_notes: str | None = None,
    ) -> dict[str, Any] | None:
        technique_aliases = {
            "ep": "EP",
            "equivalence partitioning": "EP",
            "equivalence partition": "EP",
            "bva": "BVA",
            "boundary value analysis": "BVA",
            "decision table": "Decision Table",
            "decision table testing": "Decision Table",
            "state transition": "State Transition",
            "state transition testing": "State Transition",
        }
        normalized_techniques: list[str] = []
        for item in forced_techniques or []:
            key = item.strip().lower()
            if not key:
                continue
            label = technique_aliases.get(key, item.strip())
            if label not in normalized_techniques:
                normalized_techniques.append(label)

        normalized_items = [item.strip() for item in (coverage_items or []) if item and item.strip()]
        normalized_notes = (designer_review_notes or "").strip()

        if not normalized_techniques and not normalized_items and not normalized_notes:
            return None

        return {
            "forced_techniques": normalized_techniques,
            "coverage_items": normalized_items,
            "designer_review_notes": normalized_notes,
        }

    def build_stage_control(
        self,
        requirement_id: str,
        stage: str,
        slot: int = 0,
        profile: dict[str, str] | None = None,
        review_guidance: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = {
            "stage": stage,
            "seed": derive_stage_seed(self.config.seed, requirement_id, stage, slot),
        }
        if slot:
            payload["candidate_index"] = slot
        if profile:
            payload["profile_label"] = profile["label"]
            payload["profile_instruction"] = profile["instruction"]
        if review_guidance:
            payload.update(review_guidance)
        return payload

    def build_candidate_controls(
        self,
        requirement_id: str,
        candidates: int,
        review_guidance: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        controls: list[dict[str, Any]] = []
        for index in range(candidates):
            controls.append(
                self.build_stage_control(
                    requirement_id,
                    stage="structured_generation",
                    slot=index + 1,
                    profile=self._candidate_profile(index),
                    review_guidance=review_guidance,
                )
            )
        return controls

    def generation_prompt(self, requirement_text: str, control: dict[str, Any] | None = None) -> str:
        prompt = self._compose_prompt('generation_prompt.txt', {'REQUIREMENT_TEXT': requirement_text})
        if not control:
            return prompt
        tail = [
            "",
            "Deterministic candidate focus:",
            f"- Candidate slot: {control.get('candidate_index', 1)}",
        ]
        if control.get("profile_label"):
            tail.append(f"- Focus profile: {control['profile_label']}")
        if control.get("profile_instruction"):
            tail.append(f"- Internal focus guidance: {control['profile_instruction']}")
        if control.get("seed") is not None:
            tail.append(f"- Reproducibility seed tag: {control['seed']}")
        forced_techniques = control.get("forced_techniques") or []
        coverage_items = control.get("coverage_items") or []
        designer_review_notes = (control.get("designer_review_notes") or "").strip()
        if forced_techniques or coverage_items or designer_review_notes:
            tail.extend(["", "Designer review guidance:"])
            if forced_techniques:
                tail.append(f"- Required techniques to emphasize: {', '.join(forced_techniques)}")
            if coverage_items:
                tail.append(f"- Coverage items to inspect explicitly: {'; '.join(coverage_items)}")
            if designer_review_notes:
                tail.append(f"- Reviewer notes: {designer_review_notes}")
            tail.append("- Treat the designer guidance as mandatory planning input.")
        tail.append("- Use the focus guidance internally to diversify coverage.")
        tail.append("- Do not repeat the control metadata verbatim in the final answer.")
        return "\n".join([prompt, *tail]).strip()

    def plain_prompt(self, requirement_text: str, control: dict[str, Any] | None = None) -> str:
        prompt = self._compose_prompt('baseline_plain_llm.txt', {'REQUIREMENT_TEXT': requirement_text})
        if not control:
            return prompt
        tail = ["", "Deterministic baseline control:"]
        if control.get("seed") is not None:
            tail.append(f"- Reproducibility seed tag: {control['seed']}")
        tail.append("- Keep the output concise and machine-readable.")
        return "\n".join([prompt, *tail]).strip()

    def repair_prompt(self, requirement_text: str, raw_trace: str, diagnostics: list[str]) -> str:
        return self._compose_prompt(
            'repair_prompt.txt',
            {
                'REQUIREMENT_TEXT': requirement_text,
                'RAW_TRACE': raw_trace,
                'DIAGNOSTICS': '\n'.join(f'- {item}' for item in diagnostics),
            },
        )

    def detect_split(self, requirement_path: Path) -> str:
        parts = {part.lower() for part in requirement_path.parts}
        return 'test' if 'test' in parts else 'dev'

    def annotate_trace(self, parsed: ParsedTrace, split: str, requirement_text: str) -> ParsedTrace:
        parsed.category = requirement_category(self.config.paths.root, split, parsed.requirement_id)
        parsed.risk_assessment = assess_requirement_risk(requirement_text, parsed, parsed.category)
        parsed.state_model = build_state_model(requirement_text, parsed)
        assign_case_priorities(parsed)
        return parsed

    def build_requirement_run_context(self, split: str, candidates: int) -> dict:
        return {
            'split': split,
            'provider': self.config.provider,
            'model': self.config.model,
            'candidates': candidates,
            'openai_api_mode': self.config.openai_api_mode,
            'seed': self.config.seed,
            'temperature': self.config.temperature,
            'top_p': self.config.top_p,
            'enable_repair': self.config.enable_repair,
            'runtime_root': str(self.config.paths.runtime_root),
            'outputs_root': str(self.config.paths.outputs),
            'artifacts_root': str(self.config.paths.artifacts),
        }

    def assess_trace(
        self,
        parsed: ParsedTrace,
        requirement_text: str,
        source: str = 'structured',
        repaired: bool = False,
        candidate_index: int | None = None,
        generation_metadata: dict[str, Any] | None = None,
    ) -> CandidateEvaluation:
        candidate = CandidateEvaluation(
            requirement_id=parsed.requirement_id,
            requirement_text=requirement_text,
            raw_text=parsed.raw_text,
            parsed_trace=parsed,
            checks=run_all_checks(parsed),
            score=0.0,
            repaired=repaired,
            source=source,
            candidate_index=candidate_index,
            generation_metadata=generation_metadata or {},
        )
        candidate.score = aggregate_score(candidate)
        return candidate

    def summarize_raw_candidates(
        self,
        requirement_text: str,
        requirement_id: str,
        split: str,
        raw_candidates: list[str],
        generation_metadata: list[dict[str, Any]] | None = None,
        candidate_controls: list[dict[str, Any]] | None = None,
        export: bool = True,
    ) -> dict:
        metadata_rows = generation_metadata or [{} for _ in raw_candidates]
        evaluated = [
            self.assess_trace(
                self.annotate_trace(parse_trace(raw, requirement_id), split, requirement_text),
                requirement_text=requirement_text,
                candidate_index=(metadata_rows[index] if index < len(metadata_rows) else {}).get("candidate_index", index + 1),
                generation_metadata=metadata_rows[index] if index < len(metadata_rows) else {},
            )
            for index, raw in enumerate(raw_candidates)
        ]
        selected = select_best(evaluated)

        if self.config.enable_repair:
            repaired_trace = local_repair(selected)
            repaired_trace.category = selected.parsed_trace.category
            repaired_trace.risk_assessment = selected.parsed_trace.risk_assessment
            repaired_trace.state_model = selected.parsed_trace.state_model
            assign_case_priorities(repaired_trace)
            repaired_candidate = self.assess_trace(
                repaired_trace,
                requirement_text=requirement_text,
                source=selected.source,
                repaired=True,
                candidate_index=selected.candidate_index,
                generation_metadata=selected.generation_metadata,
            )
            if repaired_candidate.score >= selected.score:
                selected = repaired_candidate

        gold_path = gold_spec_path(self.config.paths.root, split, requirement_id)
        metrics = evaluate_suite(selected.parsed_trace.test_cases, gold_path)
        metrics['checker_score'] = selected.score
        metrics['repaired'] = selected.repaired
        run_context = self.build_requirement_run_context(split, len(raw_candidates))
        if export:
            self.exporter.export_run(
                requirement_id,
                split,
                raw_candidates,
                metadata_rows,
                selected,
                metrics,
                run_context,
                candidate_controls,
            )
        return {
            'requirement_id': requirement_id,
            'split': split,
            'category': selected.parsed_trace.category,
            'score': selected.score,
            'repaired': selected.repaired,
            'candidate_index': selected.candidate_index,
            'generation_metadata': selected.generation_metadata,
            'candidate_controls': candidate_controls or [],
            'risk_assessment': selected.parsed_trace.risk_assessment.to_dict() if selected.parsed_trace.risk_assessment else None,
            'state_model': selected.parsed_trace.state_model.to_dict() if selected.parsed_trace.state_model else None,
            'metrics': metrics,
            'diagnostics': selected.diagnostics(),
        }

    def _process_requirement(
        self,
        requirement_text: str,
        requirement_id: str,
        split: str,
        candidates: int | None = None,
        export: bool = True,
        review_guidance: dict[str, Any] | None = None,
    ) -> dict:
        requested_candidates = candidates or self.config.candidates
        candidate_controls = self.build_candidate_controls(requirement_id, requested_candidates, review_guidance=review_guidance)
        raw_candidates = self.client.generate_structured_candidates(
            requirement_id=requirement_id,
            requirement_text=requirement_text,
            prompt=[self.generation_prompt(requirement_text, control) for control in candidate_controls],
            candidates=requested_candidates,
            candidate_controls=candidate_controls,
        )
        generation_metadata = self.client.get_last_generation_metadata()
        summary = self.summarize_raw_candidates(
            requirement_text,
            requirement_id,
            split,
            raw_candidates,
            generation_metadata=generation_metadata,
            candidate_controls=candidate_controls,
            export=export,
        )
        if review_guidance:
            summary["designer_review"] = review_guidance
        return summary

    def process_requirement_text(
        self,
        requirement_text: str,
        requirement_id: str | None = None,
        split: str = 'adhoc',
        candidates: int | None = None,
        export: bool = True,
        forced_techniques: list[str] | None = None,
        coverage_items: list[str] | None = None,
        designer_review_notes: str | None = None,
    ) -> dict:
        resolved_id = extract_requirement_id(requirement_text, requirement_id or 'adhoc_requirement')
        review_guidance = self._normalize_review_guidance(
            forced_techniques=forced_techniques,
            coverage_items=coverage_items,
            designer_review_notes=designer_review_notes,
        )
        return self._process_requirement(
            requirement_text,
            resolved_id,
            split,
            candidates=candidates,
            export=export,
            review_guidance=review_guidance,
        )

    def process_requirement_file(
        self,
        requirement_path: Path,
        candidates: int | None = None,
        export: bool = True,
    ) -> dict:
        requirement_text = read_text(requirement_path)
        requirement_id = extract_requirement_id(requirement_text, requirement_path.stem)
        split = self.detect_split(requirement_path)
        return self._process_requirement(requirement_text, requirement_id, split, candidates=candidates, export=export)

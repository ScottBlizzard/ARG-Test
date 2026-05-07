from __future__ import annotations

import os
from pathlib import Path

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
from .utils import extract_requirement_id, float_from_env, gold_spec_path, load_prompt, read_text, requirement_category


class ARGTestPipeline:
    def __init__(
        self,
        base_dir: Path | None = None,
        provider: str | None = None,
        model: str | None = None,
        candidates: int | None = None,
        output_root: str | None = None,
    ) -> None:
        self.config: RuntimeConfig = load_runtime_config(
            base_dir=base_dir,
            provider=provider,
            model=model,
            candidates=candidates,
            output_root=output_root,
        )
        self.client = get_llm_client(
            self.config.provider,
            self.config.model,
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL'),
            timeout=float_from_env('OPENAI_TIMEOUT_SECONDS'),
        )
        self.exporter = Exporter(self.config.paths.artifacts, self.config.paths.outputs)

    def _compose_prompt(self, prompt_name: str, replacements: dict[str, str]) -> str:
        system = load_prompt(self.config.paths.prompts / 'system_prompt.txt')
        user = load_prompt(self.config.paths.prompts / prompt_name, replacements)
        return f"{system}\n\n{user}".strip()

    def generation_prompt(self, requirement_text: str) -> str:
        return self._compose_prompt('generation_prompt.txt', {'REQUIREMENT_TEXT': requirement_text})

    def plain_prompt(self, requirement_text: str) -> str:
        return self._compose_prompt('baseline_plain_llm.txt', {'REQUIREMENT_TEXT': requirement_text})

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
        assign_case_priorities(parsed)
        return parsed

    def build_requirement_run_context(self, split: str, candidates: int) -> dict:
        return {
            'split': split,
            'provider': self.config.provider,
            'model': self.config.model,
            'candidates': candidates,
            'enable_repair': self.config.enable_repair,
            'runtime_root': str(self.config.paths.runtime_root),
            'outputs_root': str(self.config.paths.outputs),
            'artifacts_root': str(self.config.paths.artifacts),
        }

    def assess_trace(self, parsed: ParsedTrace, source: str = 'structured', repaired: bool = False) -> CandidateEvaluation:
        candidate = CandidateEvaluation(
            requirement_id=parsed.requirement_id,
            raw_text=parsed.raw_text,
            parsed_trace=parsed,
            checks=run_all_checks(parsed),
            score=0.0,
            repaired=repaired,
            source=source,
        )
        candidate.score = aggregate_score(candidate)
        return candidate

    def process_requirement_file(
        self,
        requirement_path: Path,
        candidates: int | None = None,
        export: bool = True,
    ) -> dict:
        requirement_text = read_text(requirement_path)
        requirement_id = extract_requirement_id(requirement_text, requirement_path.stem)
        split = self.detect_split(requirement_path)
        requested_candidates = candidates or self.config.candidates
        raw_candidates = self.client.generate_structured_candidates(
            requirement_id=requirement_id,
            requirement_text=requirement_text,
            prompt=self.generation_prompt(requirement_text),
            candidates=requested_candidates,
        )
        evaluated = [
            self.assess_trace(self.annotate_trace(parse_trace(raw, requirement_id), split, requirement_text))
            for raw in raw_candidates
        ]
        selected = select_best(evaluated)

        if self.config.enable_repair and selected.score < 0.95:
            repaired_trace = local_repair(selected)
            repaired_trace.category = selected.parsed_trace.category
            repaired_trace.risk_assessment = selected.parsed_trace.risk_assessment
            assign_case_priorities(repaired_trace)
            repaired_candidate = self.assess_trace(repaired_trace, source=selected.source, repaired=True)
            if repaired_candidate.score >= selected.score:
                selected = repaired_candidate

        gold_path = gold_spec_path(self.config.paths.root, split, requirement_id)
        metrics = evaluate_suite(selected.parsed_trace.test_cases, gold_path)
        metrics['checker_score'] = selected.score
        metrics['repaired'] = selected.repaired
        run_context = self.build_requirement_run_context(split, requested_candidates)
        if export:
            self.exporter.export_run(requirement_id, split, raw_candidates, selected, metrics, run_context)
        return {
            'requirement_id': requirement_id,
            'split': split,
            'category': selected.parsed_trace.category,
            'score': selected.score,
            'repaired': selected.repaired,
            'risk_assessment': selected.parsed_trace.risk_assessment.to_dict() if selected.parsed_trace.risk_assessment else None,
            'metrics': metrics,
            'diagnostics': selected.diagnostics(),
        }

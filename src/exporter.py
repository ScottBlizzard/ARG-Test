from __future__ import annotations

from pathlib import Path

from .schemas import CandidateEvaluation
from .utils import write_csv, write_json


class Exporter:
    def __init__(self, artifacts_root: Path, outputs_root: Path) -> None:
        self.artifacts_root = artifacts_root
        self.outputs_root = outputs_root

    def export_run(
        self,
        requirement_id: str,
        split: str,
        raw_candidates: list[str],
        selected: CandidateEvaluation,
        metrics: dict | None = None,
        run_context: dict | None = None,
    ) -> None:
        for index, raw_text in enumerate(raw_candidates, start=1):
            raw_path = self.artifacts_root / 'raw_generations' / split / f'{requirement_id}_candidate_{index}.md'
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_text(raw_text, encoding='utf-8')

        parsed_path = self.artifacts_root / 'parsed_traces' / split / f'{requirement_id}.json'
        write_json(parsed_path, selected.parsed_trace.to_dict())

        if selected.parsed_trace.state_model:
            state_artifact_dir = self.artifacts_root / 'state_models' / split
            state_output_dir = self.outputs_root / 'state_models' / split
            write_json(state_artifact_dir / f'{requirement_id}.json', selected.parsed_trace.state_model.to_dict())
            write_json(state_output_dir / f'{requirement_id}.json', selected.parsed_trace.state_model.to_dict())
            (state_output_dir / f'{requirement_id}.md').write_text(
                selected.parsed_trace.state_model.to_markdown(requirement_id),
                encoding='utf-8',
            )

        checker_path = self.artifacts_root / 'checker_logs' / split / f'{requirement_id}.json'
        write_json(
            checker_path,
            {
                'requirement_id': requirement_id,
                'category': selected.parsed_trace.category,
                'score': selected.score,
                'repaired': selected.repaired,
                'risk_assessment': selected.parsed_trace.risk_assessment.to_dict() if selected.parsed_trace.risk_assessment else None,
                'state_model': selected.parsed_trace.state_model.to_dict() if selected.parsed_trace.state_model else None,
                'checks': [check.to_dict() for check in selected.checks],
                'diagnostics': selected.diagnostics(),
                'run_context': run_context or {},
            },
        )

        tests_dir = self.outputs_root / 'final_tests' / split
        tests_dir.mkdir(parents=True, exist_ok=True)
        write_json(tests_dir / f'{requirement_id}.json', selected.parsed_trace.to_dict())
        write_csv(tests_dir / f'{requirement_id}.csv', [case.to_dict() for case in selected.parsed_trace.test_cases])
        (tests_dir / f'{requirement_id}.md').write_text(selected.parsed_trace.to_markdown(), encoding='utf-8')

        report_payload = {
            'requirement_id': requirement_id,
            'split': split,
            'category': selected.parsed_trace.category,
            'score': selected.score,
            'repaired': selected.repaired,
            'risk_assessment': selected.parsed_trace.risk_assessment.to_dict() if selected.parsed_trace.risk_assessment else None,
            'state_model': selected.parsed_trace.state_model.to_dict() if selected.parsed_trace.state_model else None,
            'metrics': metrics or {},
            'diagnostics': selected.diagnostics(),
            'run_context': run_context or {},
        }
        write_json(self.outputs_root / 'reports' / split / f'{requirement_id}_summary.json', report_payload)

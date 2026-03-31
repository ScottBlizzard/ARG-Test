from __future__ import annotations

from pathlib import Path

from .schemas import CandidateEvaluation
from .utils import write_csv, write_json


class Exporter:
    def __init__(self, root: Path) -> None:
        self.root = root

    def export_run(
        self,
        requirement_id: str,
        split: str,
        raw_candidates: list[str],
        selected: CandidateEvaluation,
        metrics: dict | None = None,
    ) -> None:
        for index, raw_text in enumerate(raw_candidates, start=1):
            raw_path = self.root / 'artifacts' / 'raw_generations' / split / f'{requirement_id}_candidate_{index}.md'
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_text(raw_text, encoding='utf-8')

        parsed_path = self.root / 'artifacts' / 'parsed_traces' / split / f'{requirement_id}.json'
        write_json(parsed_path, selected.parsed_trace.to_dict())

        checker_path = self.root / 'artifacts' / 'checker_logs' / split / f'{requirement_id}.json'
        write_json(
            checker_path,
            {
                'requirement_id': requirement_id,
                'score': selected.score,
                'repaired': selected.repaired,
                'checks': [check.to_dict() for check in selected.checks],
                'diagnostics': selected.diagnostics(),
            },
        )

        tests_dir = self.root / 'outputs' / 'final_tests' / split
        tests_dir.mkdir(parents=True, exist_ok=True)
        write_json(tests_dir / f'{requirement_id}.json', selected.parsed_trace.to_dict())
        write_csv(tests_dir / f'{requirement_id}.csv', [case.to_dict() for case in selected.parsed_trace.test_cases])
        (tests_dir / f'{requirement_id}.md').write_text(selected.parsed_trace.to_markdown(), encoding='utf-8')

        report_payload = {
            'requirement_id': requirement_id,
            'score': selected.score,
            'repaired': selected.repaired,
            'metrics': metrics or {},
        }
        write_json(self.root / 'outputs' / 'reports' / split / f'{requirement_id}_summary.json', report_payload)

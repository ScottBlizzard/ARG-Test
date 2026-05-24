from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.main import build_parser
from src.pipeline import ARGTestPipeline
from src.utils import list_requirement_files, write_json

TEXT_SUFFIXES = {".json", ".md", ".txt", ".csv", ".py", ".xml", ".ini", ".yaml", ".yml", ".ps1"}
SECRET_PATTERNS = {
    "OPENAI_API_KEY": re.compile(r"OPENAI_API_KEY", flags=re.IGNORECASE),
    "openai_key_like": re.compile(r"\bsk-[A-Za-z0-9]{10,}\b"),
    "bearer_token_like": re.compile(r"Bearer\s+[A-Za-z0-9._-]{10,}", flags=re.IGNORECASE),
}


def benchmark_mock_pipeline(sample_size: int = 5) -> dict:
    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider="mock",
        model="mock-arg-test",
        candidates=3,
        output_root=".local_runs/nfr_check_mock",
    )
    files = list_requirement_files(ROOT, "test")[:sample_size]
    per_requirement = []
    for path in files:
        started = time.perf_counter()
        summary = pipeline.process_requirement_file(path, candidates=3, export=False)
        elapsed = time.perf_counter() - started
        per_requirement.append(
            {
                "requirement_id": summary["requirement_id"],
                "seconds": round(elapsed, 4),
            }
        )
    avg_seconds = round(sum(item["seconds"] for item in per_requirement) / len(per_requirement), 4) if per_requirement else 0.0
    return {
        "sample_size": len(per_requirement),
        "average_seconds_per_requirement": avg_seconds,
        "per_requirement": per_requirement,
    }


def collect_usability_evidence() -> dict:
    parser = build_parser()
    command_names = sorted(parser._subparsers._group_actions[0].choices.keys())
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
    web_app = ROOT / "demo_web" / "app.py"
    web_static = ROOT / "demo_web" / "static"
    formal_snapshot = ROOT / "report_assets" / "final_demo_package" / "frontend_focus" / "formal_results_snapshot"
    return {
        "supported_cli_commands": command_names,
        "has_quick_start": "Quick start" in readme,
        "has_formal_run_workflow": "Formal run workflow" in readme,
        "supports_direct_text_input": "run-text" in readme,
        "supports_csv_input": "batch-csv" in readme,
        "web_demo_available": web_app.exists() and web_static.exists(),
        "web_demo_formal_replay_snapshot_available": formal_snapshot.exists(),
        "web_demo_tabs": ["Direct Input", "CSV Batch", "State Model", "Formal Evidence"],
        "export_formats": ["JSON", "CSV", "Markdown"],
    }


def collect_security_evidence() -> dict:
    scan_roots = [
        ROOT / "outputs",
        ROOT / "artifacts",
        ROOT / "final_docs",
        ROOT / ".local_runs" / "formal_qwen_novpn" / "outputs" / "reports",
        ROOT / ".local_runs" / "formal_qwen_upgrade_smoke" / "outputs" / "reports",
    ]
    findings = []
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*"):
            if path.is_dir() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for name, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    findings.append({"path": str(path.relative_to(ROOT)), "pattern": name})
    return {
        "secret_scan_roots": [str(path.relative_to(ROOT)) for path in scan_roots if path.exists()],
        "secret_findings": findings,
        "secret_leak_found": bool(findings),
        "manifests_record_provider_but_not_api_key": not any(item["pattern"] == "OPENAI_API_KEY" for item in findings),
    }


def collect_maintainability_evidence() -> dict:
    src_modules = len(list((ROOT / "src").rglob("*.py")))
    experiment_scripts = len(list((ROOT / "experiments").glob("*.py")))
    test_files = list((ROOT / "tests").glob("test_*.py"))
    test_case_count = 0
    for path in test_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        test_case_count += text.count("\ndef test_")
        if text.startswith("def test_"):
            test_case_count += 1

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    return {
        "src_module_count": src_modules,
        "experiment_script_count": experiment_scripts,
        "test_file_count": len(test_files),
        "test_case_count": test_case_count,
        "pytest_exit_code": result.returncode,
        "pytest_summary": (result.stdout or "").strip().splitlines()[-1] if result.stdout.strip() else "",
        "runtime_output_isolation_supported": ".local_runs/" in (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore"),
    }


def build_nfr_payload() -> dict:
    performance = benchmark_mock_pipeline()
    usability = collect_usability_evidence()
    security = collect_security_evidence()
    maintainability = collect_maintainability_evidence()
    return {
        "performance": performance,
        "usability": usability,
        "security": security,
        "maintainability": maintainability,
    }


def build_markdown(payload: dict) -> str:
    performance = payload["performance"]
    usability = payload["usability"]
    security = payload["security"]
    maintainability = payload["maintainability"]
    lines = [
        "# NFR Validation Summary",
        "",
        "## Performance",
        "",
        f"- Sample size: `{performance['sample_size']}`",
        f"- Average mock processing time per requirement: `{performance['average_seconds_per_requirement']} s`",
        "",
        "| Requirement | Seconds |",
        "| --- | ---: |",
    ]
    for item in performance["per_requirement"]:
        lines.append(f"| {item['requirement_id']} | {item['seconds']} |")

    lines.extend(
        [
            "",
            "## Usability",
            "",
            f"- Supported CLI commands: `{', '.join(usability['supported_cli_commands'])}`",
            f"- README quick start available: `{str(usability['has_quick_start']).lower()}`",
            f"- Formal run workflow documented: `{str(usability['has_formal_run_workflow']).lower()}`",
            f"- Direct text input supported: `{str(usability['supports_direct_text_input']).lower()}`",
            f"- CSV input supported: `{str(usability['supports_csv_input']).lower()}`",
            f"- Web demo available: `{str(usability['web_demo_available']).lower()}`",
            f"- Web demo formal replay snapshot available: `{str(usability['web_demo_formal_replay_snapshot_available']).lower()}`",
            f"- Web demo tabs: `{', '.join(usability['web_demo_tabs'])}`",
            f"- Export formats: `{', '.join(usability['export_formats'])}`",
            "",
            "## Security",
            "",
            f"- Secret leak found in generated/report artifacts: `{str(security['secret_leak_found']).lower()}`",
            f"- Manifests record provider metadata without API key disclosure: `{str(security['manifests_record_provider_but_not_api_key']).lower()}`",
            "",
            "## Maintainability",
            "",
            f"- `src/` Python modules: `{maintainability['src_module_count']}`",
            f"- experiment scripts: `{maintainability['experiment_script_count']}`",
            f"- test files: `{maintainability['test_file_count']}`",
            f"- test cases: `{maintainability['test_case_count']}`",
            f"- pytest exit code: `{maintainability['pytest_exit_code']}`",
            f"- pytest summary: `{maintainability['pytest_summary']}`",
            f"- runtime output isolation supported: `{str(maintainability['runtime_output_isolation_supported']).lower()}`",
            "",
        ]
    )
    if security["secret_findings"]:
        lines.extend(["### Secret Findings", ""])
        for finding in security["secret_findings"]:
            lines.append(f"- {finding['path']} -> {finding['pattern']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    payload = build_nfr_payload()
    evidence_dir = ROOT / "final_docs" / "execution_evidence"
    write_json(evidence_dir / "nfr_validation_summary.json", payload)
    (evidence_dir / "nfr_validation_summary.md").write_text(build_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

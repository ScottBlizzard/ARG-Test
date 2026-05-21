from __future__ import annotations

import csv
import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from .schemas import TestCase

SECTION_ORDER = ["Analysis", "Pattern", "Steps", "Verification", "FinalAnswer"]


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_dotenv_file(path: Path, override: bool = False) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding='utf-8-sig').splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if stripped.startswith('export '):
            stripped = stripped[len('export '):].strip()
        if '=' not in stripped:
            continue
        key, value = stripped.split('=', 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if value and len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        if override or key not in os.environ:
            os.environ[key] = value


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return re.sub(r"_+", "_", cleaned).strip("_").lower()


def list_requirement_files(base_dir: Path, split: str) -> list[Path]:
    folder = base_dir / "data" / "requirements" / split
    return sorted(folder.glob("*.txt"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


@lru_cache(maxsize=8)
def _manifest_index(root: str) -> dict[tuple[str, str], dict]:
    manifest_path = Path(root) / "data" / "requirements" / "manifest.json"
    if not manifest_path.exists():
        return {}
    manifest = load_json(manifest_path)
    index: dict[tuple[str, str], dict] = {}
    for item in manifest:
        requirement_id = str(item.get("requirement_id", "")).strip()
        split = str(item.get("split", "")).strip()
        if requirement_id and split:
            index[(split, requirement_id)] = item
    return index


def requirement_manifest_entry(base_dir: Path, split: str, requirement_id: str) -> dict | None:
    return _manifest_index(str(base_dir.resolve())).get((split, requirement_id))


def requirement_category(base_dir: Path, split: str, requirement_id: str) -> str | None:
    entry = requirement_manifest_entry(base_dir, split, requirement_id)
    if not entry:
        return None
    return str(entry.get("category", "")).strip() or None


def extract_requirement_id(text: str, fallback: str) -> str:
    match = re.search(r"^Requirement ID:\s*(.+)$", text, flags=re.MULTILINE)
    if match:
        return slugify(match.group(1))
    return slugify(fallback)


def extract_rule_lines(text: str) -> list[str]:
    rules: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^\d+\.\s+", stripped):
            rules.append(stripped)
    return rules


def infer_techniques(text: str) -> list[str]:
    lowered = text.lower()
    techniques: list[str] = []
    if any(token in lowered for token in ["between", "inclusive", "at least", "up to", "must be", "characters", "above"]):
        techniques.extend(["EP", "BVA"])
    if any(token in lowered for token in ["only one", "if", "when", "must not", "cannot", "require", "returns"]):
        techniques.append("Decision Table")
    if any(token in lowered for token in ["state", "locked", "unlock", "moves the order", "starts in", "returns to the active state"]):
        techniques.append("State Transition")
    unique: list[str] = []
    for item in techniques:
        if item not in unique:
            unique.append(item)
    return unique or ["EP"]


def extract_numeric_hints(text: str) -> list[dict[str, object]]:
    hints: list[dict[str, object]] = []
    for line in extract_rule_lines(text):
        lowered = line.lower()
        range_match = re.search(r"(?P<low>\d+)\s+to\s+(?P<high>\d+)", lowered)
        between_match = re.search(r"between\s+(?P<low>\d+)\s+and\s+(?P<high>\d+)", lowered)
        threshold_match = re.search(r"at least\s+(?P<low>\d+)", lowered)
        field = re.sub(r"^\d+\.\s+", "", lowered).split(" is ")[0].split(" must ")[0].split(" are ")[0]
        if range_match:
            hints.append({
                "field": field.strip(),
                "type": "range",
                "low": int(range_match.group("low")),
                "high": int(range_match.group("high")),
                "source": line,
            })
        elif between_match:
            hints.append({
                "field": field.strip(),
                "type": "range",
                "low": int(between_match.group("low")),
                "high": int(between_match.group("high")),
                "source": line,
            })
        elif threshold_match:
            hints.append({
                "field": field.strip(),
                "type": "threshold",
                "low": int(threshold_match.group("low")),
                "source": line,
            })
    return hints


def dedupe_test_cases(test_cases: Iterable[TestCase]) -> list[TestCase]:
    seen: set[str] = set()
    unique_cases: list[TestCase] = []
    for case in test_cases:
        signature = case.normalized_signature()
        if signature in seen:
            continue
        seen.add(signature)
        unique_cases.append(case)
    return unique_cases


def duplicate_count(test_cases: Iterable[TestCase]) -> int:
    seen: set[str] = set()
    duplicates = 0
    for case in test_cases:
        signature = case.normalized_signature()
        if signature in seen:
            duplicates += 1
        else:
            seen.add(signature)
    return duplicates


def load_prompt(prompt_path: Path, replacements: dict[str, str] | None = None) -> str:
    content = read_text(prompt_path)
    replacements = replacements or {}
    for key, value in replacements.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def gold_spec_path(base_dir: Path, split: str, requirement_id: str) -> Path:
    return base_dir / "data" / "gold_specs" / split / f"{requirement_id}.json"


def bool_from_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def float_from_env(name: str, default: float | None = None) -> float | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return float(raw.strip())

from __future__ import annotations

import re
from typing import Iterable

from .schemas import ParsedTrace, TestCase
from .utils import SECTION_ORDER

SECTION_PATTERN = re.compile(r"^(Analysis|Pattern|Steps|Verification|FinalAnswer)\s*:\s*$", flags=re.MULTILINE)


def _split_sections(text: str) -> tuple[dict[str, str], list[str]]:
    matches = list(SECTION_PATTERN.finditer(text))
    sections = {name: "" for name in SECTION_ORDER}
    missing: list[str] = []
    if not matches:
        return sections, SECTION_ORDER.copy()
    for index, match in enumerate(matches):
        name = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    missing = [name for name in SECTION_ORDER if not sections[name]]
    return sections, missing


def _parse_steps(section_text: str) -> list[str]:
    steps: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped:
            steps.append(stripped)
    return steps


def _parse_markdown_table(table_text: str, requirement_id: str) -> list[TestCase]:
    rows = [line.strip() for line in table_text.splitlines() if line.strip().startswith("|")]
    if len(rows) < 2:
        return []
    header = [cell.strip() for cell in rows[0].strip("|").split("|")]
    data_rows = rows[2:] if len(rows) >= 2 and set(rows[1].replace("|", "").replace("-", "").strip()) == set() else rows[1:]
    canonical = {name.lower(): index for index, name in enumerate(header)}

    def pick(values: list[str], key: str, default: str = "") -> str:
        index = canonical.get(key.lower())
        if index is None or index >= len(values):
            return default
        return values[index].strip()

    test_cases: list[TestCase] = []
    for row in data_rows:
        values = [cell.strip() for cell in row.strip("|").split("|")]
        if not any(values):
            continue
        test_cases.append(
            TestCase(
                test_id=pick(values, "test id", f"{requirement_id}-auto"),
                technique=pick(values, "technique", "EP"),
                requirement_target=pick(values, "requirement target", requirement_id),
                preconditions=pick(values, "preconditions", "None"),
                input_data=pick(values, "input", "N/A"),
                expected_output=pick(values, "expected output", "TBD"),
                covered_item=pick(values, "covered item", "unspecified"),
                priority=pick(values, "priority", "Medium"),
                checker_status=pick(values, "checker status", "pending"),
            )
        )
    return test_cases


def verification_references(verification_text: str) -> list[int]:
    return [int(match.group(1)) for match in re.finditer(r"step\s+(\d+)", verification_text, flags=re.IGNORECASE)]


def parse_trace(raw_text: str, requirement_id: str) -> ParsedTrace:
    sections, missing = _split_sections(raw_text)
    steps = _parse_steps(sections["Steps"])
    test_cases = _parse_markdown_table(sections["FinalAnswer"], requirement_id)
    return ParsedTrace(
        requirement_id=requirement_id,
        analysis=sections["Analysis"],
        pattern=sections["Pattern"],
        steps=steps,
        verification=sections["Verification"],
        test_cases=test_cases,
        raw_text=raw_text,
        missing_sections=missing,
    )

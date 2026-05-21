from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .utils import extract_requirement_id


@dataclass
class RequirementInput:
    requirement_id: str
    requirement_text: str
    split: str


def load_requirements_from_csv(
    path: Path,
    *,
    text_column: str = "requirement_text",
    id_column: str = "requirement_id",
    split_column: str = "split",
    default_split: str = "adhoc",
) -> list[RequirementInput]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV file has no header: {path}")
        fieldnames = {name.strip(): name for name in reader.fieldnames if name}
        if text_column not in fieldnames:
            raise ValueError(f"CSV column `{text_column}` is required in {path}")

        items: list[RequirementInput] = []
        for index, row in enumerate(reader, start=1):
            requirement_text = (row.get(fieldnames[text_column], "") or "").strip()
            if not requirement_text:
                continue
            raw_id = (row.get(fieldnames.get(id_column, id_column), "") or "").strip()
            requirement_id = raw_id or extract_requirement_id(requirement_text, f"csv_requirement_{index}")
            raw_split = (row.get(fieldnames.get(split_column, split_column), "") or "").strip()
            split = raw_split or default_split
            items.append(
                RequirementInput(
                    requirement_id=requirement_id,
                    requirement_text=requirement_text,
                    split=split,
                )
            )
    return items

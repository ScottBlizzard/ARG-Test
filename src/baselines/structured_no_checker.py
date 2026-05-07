from __future__ import annotations

from ..parser import parse_trace


def build_structured_no_checker_trace(
    requirement_id: str,
    requirement_text: str,
    client,
    generation_prompt: str | list[str],
    control: dict | None = None,
):
    raw = client.generate_structured_candidates(
        requirement_id=requirement_id,
        requirement_text=requirement_text,
        prompt=generation_prompt,
        candidates=1,
        candidate_controls=[control] if control else None,
    )[0]
    return parse_trace(raw, requirement_id)

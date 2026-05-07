from __future__ import annotations

from ..parser import parse_trace


def build_plain_llm_trace(
    requirement_id: str,
    requirement_text: str,
    client,
    plain_prompt: str,
    control: dict | None = None,
):
    table = client.generate_plain_table(
        requirement_id=requirement_id,
        requirement_text=requirement_text,
        prompt=plain_prompt,
        control=control,
    )
    wrapped = '\n'.join(
        [
            'Analysis:',
            '- Plain LLM baseline does not enforce structured reasoning.',
            '',
            'Pattern:',
            '- Selected technique is unconstrained and may be incomplete.',
            '',
            'Steps:',
            '1. Request test cases directly from the model.',
            '',
            'Verification:',
            '- No checker-aware verification is applied in this baseline.',
            '',
            'FinalAnswer:',
            table,
        ]
    )
    return parse_trace(wrapped, requirement_id)

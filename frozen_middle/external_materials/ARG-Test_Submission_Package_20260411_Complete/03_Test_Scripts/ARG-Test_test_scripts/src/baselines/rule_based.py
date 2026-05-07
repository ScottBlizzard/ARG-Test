from __future__ import annotations

from ..schemas import ParsedTrace, TestCase
from ..utils import extract_numeric_hints, infer_techniques


def build_rule_based_trace(requirement_id: str, requirement_text: str) -> ParsedTrace:
    techniques = infer_techniques(requirement_text)
    hints = extract_numeric_hints(requirement_text)
    primary = techniques[0]
    test_cases = [
        TestCase(
            test_id='T01',
            technique=primary,
            requirement_target=requirement_id,
            preconditions='None',
            input_data='representative valid input',
            expected_output='request accepted',
            covered_item='valid partition',
            priority='High',
            checker_status='baseline',
        ),
        TestCase(
            test_id='T02',
            technique=primary,
            requirement_target=requirement_id,
            preconditions='None',
            input_data='representative invalid input',
            expected_output='request rejected',
            covered_item='invalid partition',
            priority='High',
            checker_status='baseline',
        ),
    ]
    if 'BVA' in techniques and hints:
        hint = hints[0]
        low = int(hint.get('low', 1))
        test_cases.append(
            TestCase(
                test_id='T03',
                technique='BVA',
                requirement_target=requirement_id,
                preconditions='None',
                input_data=f"{hint['field']}={low}",
                expected_output='boundary accepted',
                covered_item='on lower boundary',
                priority='Medium',
                checker_status='baseline',
            )
        )
    if 'Decision Table' in techniques:
        test_cases.append(
            TestCase(
                test_id=f"T{len(test_cases) + 1:02d}",
                technique='Decision Table',
                requirement_target=requirement_id,
                preconditions='relevant conditions satisfied',
                input_data='rule combination',
                expected_output='rule outcome',
                covered_item='decision rule coverage',
                priority='Medium',
                checker_status='baseline',
            )
        )
    if 'State Transition' in techniques:
        test_cases.append(
            TestCase(
                test_id=f"T{len(test_cases) + 1:02d}",
                technique='State Transition',
                requirement_target=requirement_id,
                preconditions='legal source state',
                input_data='legal event',
                expected_output='transition succeeds',
                covered_item='legal transition',
                priority='High',
                checker_status='baseline',
            )
        )
        test_cases.append(
            TestCase(
                test_id=f"T{len(test_cases) + 1:02d}",
                technique='State Transition',
                requirement_target=requirement_id,
                preconditions='illegal source state',
                input_data='illegal event',
                expected_output='transition rejected',
                covered_item='illegal transition',
                priority='High',
                checker_status='baseline',
            )
        )
    trace = ParsedTrace(
        requirement_id=requirement_id,
        analysis='- Deterministic baseline generated from explicit requirement rules only.',
        pattern='- Selected techniques: ' + ', '.join(techniques),
        steps=['1. Translate explicit rules into representative tests without LLM generation.'],
        verification='- No checker-aware generation in this baseline.',
        test_cases=test_cases,
        raw_text='',
        missing_sections=[],
    )
    trace.raw_text = trace.to_markdown()
    return trace

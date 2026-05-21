from __future__ import annotations

from ..schemas import CheckResult, ParsedTrace
from .bva_checker import check_bva
from .decision_checker import check_decision_table
from .ep_checker import check_ep
from .schema_checker import check_schema
from .state_checker import check_state_transition


def run_all_checks(parsed: ParsedTrace) -> list[CheckResult]:
    return [
        check_schema(parsed),
        check_ep(parsed),
        check_bva(parsed),
        check_decision_table(parsed),
        check_state_transition(parsed),
    ]

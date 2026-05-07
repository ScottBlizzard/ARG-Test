from __future__ import annotations

import re
from collections import deque

from .schemas import ParsedTrace, StateCoveragePlan, StateModel, StateTestSequence, StateTransition
from .utils import extract_rule_lines

STATE_PATTERN = r"[A-Z][A-Z0-9_]+|[A-Z][a-zA-Z0-9]+"
START_RE = re.compile(rf"starts in (?P<state>{STATE_PATTERN})", flags=re.IGNORECASE)
ALLOWED_RE = re.compile(
    rf"^(?P<trigger>.+?) is allowed only from (?P<source>{STATE_PATTERN}) and moves .*? to (?P<target>{STATE_PATTERN})\.?$",
    flags=re.IGNORECASE,
)
FROM_RE = re.compile(
    rf"^From (?P<source>{STATE_PATTERN}), (?P<trigger>.+?) (?:transition|transitions|moves?) .*? to (?P<target>{STATE_PATTERN})\.?$",
    flags=re.IGNORECASE,
)
CONDITIONAL_RE = re.compile(
    rf"^(?P<prefix>If|After) (?P<trigger>.+?), (?:the )?(?:order|payment|system) (?:moves to|becomes|enters) (?P<target>{STATE_PATTERN})\.?$",
    flags=re.IGNORECASE,
)
ILLEGAL_ARROW_RE = re.compile(
    rf"^Illegal:\s*(?P<source>{STATE_PATTERN})\s*(?:->|to)\s*(?P<target>{STATE_PATTERN})\.?$",
    flags=re.IGNORECASE,
)


def _title_or_original(value: str) -> str:
    cleaned = value.strip().strip(".")
    return cleaned if cleaned.upper() == cleaned else cleaned[:1].upper() + cleaned[1:]


def _dedupe_states(states: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for state in states:
        normalized = state.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        unique.append(normalized)
    return unique


def _dedupe_transitions(transitions: list[StateTransition]) -> list[StateTransition]:
    unique: list[StateTransition] = []
    seen: set[tuple[str, str, str, bool]] = set()
    for transition in transitions:
        key = (transition.source_state, transition.trigger, transition.target_state, transition.legal)
        if key in seen:
            continue
        seen.add(key)
        unique.append(transition)
    return unique


def _extract_explicit_states(requirement_text: str) -> list[str]:
    states: list[str] = []
    for rule in extract_rule_lines(requirement_text):
        content = re.sub(r"^\d+\.\s+", "", rule).strip()
        for match in re.finditer(
            rf"(?:starts in|from|to|becomes|enters)\s+(?P<state>{STATE_PATTERN})",
            content,
            flags=re.IGNORECASE,
        ):
            states.append(_title_or_original(match.group("state")))
        arrow_match = ILLEGAL_ARROW_RE.match(content)
        if arrow_match:
            states.append(_title_or_original(arrow_match.group("source")))
            states.append(_title_or_original(arrow_match.group("target")))
    return _dedupe_states(states)


def _infer_conditional_source(
    trigger_text: str,
    start_states: list[str],
    known_states: list[str],
    previous_target: str | None,
) -> str | None:
    lowered = trigger_text.lower()
    state_set = set(known_states)
    if "3ds" in lowered or "authentication" in lowered:
        if "AUTH_REQUIRED" in state_set:
            return "AUTH_REQUIRED"
        if "AuthRequired" in state_set:
            return "AuthRequired"
    if "retry" in lowered and "FAILED" in state_set:
        return "FAILED"
    if "expired" in lowered and "EXPIRED" in state_set:
        return "EXPIRED"
    if previous_target:
        return previous_target
    if start_states:
        return start_states[0]
    return None


def _extract_legal_transitions(requirement_text: str, start_states: list[str]) -> list[StateTransition]:
    transitions: list[StateTransition] = []
    known_states = _extract_explicit_states(requirement_text)
    previous_target: str | None = None
    for rule in extract_rule_lines(requirement_text):
        content = re.sub(r"^\d+\.\s+", "", rule).strip()
        match = ALLOWED_RE.match(content)
        if match:
            source = _title_or_original(match.group("source"))
            target = _title_or_original(match.group("target"))
            trigger = match.group("trigger").strip()
            transitions.append(
                StateTransition(
                    source_state=source,
                    trigger=trigger,
                    target_state=target,
                    legal=True,
                    source_rule=content,
                )
            )
            previous_target = target
            continue

        match = FROM_RE.match(content)
        if match:
            source = _title_or_original(match.group("source"))
            target = _title_or_original(match.group("target"))
            trigger = match.group("trigger").strip()
            transitions.append(
                StateTransition(
                    source_state=source,
                    trigger=trigger,
                    target_state=target,
                    legal=True,
                    source_rule=content,
                )
            )
            previous_target = target
            continue

        match = CONDITIONAL_RE.match(content)
        if match:
            target = _title_or_original(match.group("target"))
            trigger = match.group("trigger").strip()
            source = _infer_conditional_source(trigger, start_states, known_states, previous_target)
            if source:
                transitions.append(
                    StateTransition(
                        source_state=source,
                        trigger=trigger,
                        target_state=target,
                        legal=True,
                        source_rule=content,
                    )
                )
            previous_target = target
            if "may be CAPTURED" in content:
                transitions.append(
                    StateTransition(
                        source_state=target,
                        trigger="CAPTURE",
                        target_state="CAPTURED",
                        legal=True,
                        source_rule=content,
                    )
                )
            continue

        if "may be CAPTURED" in content and previous_target:
            transitions.append(
                StateTransition(
                    source_state=previous_target,
                    trigger="CAPTURE",
                    target_state="CAPTURED",
                    legal=True,
                    source_rule=content,
                )
            )

    return _dedupe_transitions(transitions)


def _extract_illegal_transitions(requirement_text: str, states: list[str]) -> list[StateTransition]:
    transitions: list[StateTransition] = []
    state_set = set(states)
    for rule in extract_rule_lines(requirement_text):
        content = re.sub(r"^\d+\.\s+", "", rule).strip()
        match = ILLEGAL_ARROW_RE.match(content)
        if match:
            transitions.append(
                StateTransition(
                    source_state=_title_or_original(match.group("source")),
                    trigger="ILLEGAL",
                    target_state=_title_or_original(match.group("target")),
                    legal=False,
                    source_rule=content,
                )
            )
            continue

        lowered = content.lower()
        if not lowered.startswith("illegal:"):
            continue
        if "capture before authentication" in lowered:
            source = "AUTH_REQUIRED" if "AUTH_REQUIRED" in state_set else "AuthRequired"
            target = "CAPTURED"
            if source:
                transitions.append(
                    StateTransition(
                        source_state=source,
                        trigger="CAPTURE",
                        target_state=target,
                        legal=False,
                        source_rule=content,
                    )
                )
        elif "back to" in lowered:
            states_in_line = re.findall(STATE_PATTERN, content)
            if len(states_in_line) >= 2:
                transitions.append(
                    StateTransition(
                        source_state=_title_or_original(states_in_line[0]),
                        trigger="ILLEGAL",
                        target_state=_title_or_original(states_in_line[1]),
                        legal=False,
                        source_rule=content,
                    )
                )
    return _dedupe_transitions(transitions)


def _adjacency(legal_transitions: list[StateTransition]) -> dict[str, list[StateTransition]]:
    graph: dict[str, list[StateTransition]] = {}
    for transition in legal_transitions:
        graph.setdefault(transition.source_state, []).append(transition)
    return graph


def _shortest_path(
    graph: dict[str, list[StateTransition]],
    start_states: list[str],
    target_state: str,
) -> list[StateTransition] | None:
    queue = deque()
    for start in start_states:
        queue.append((start, []))
    visited = set(start_states)
    while queue:
        state, path = queue.popleft()
        if state == target_state:
            return path
        for transition in graph.get(state, []):
            if transition.target_state in visited:
                continue
            visited.add(transition.target_state)
            queue.append((transition.target_state, path + [transition]))
    return None


def _sequence_steps(path: list[StateTransition], start_state: str) -> list[str]:
    steps = [f"Start in {start_state}"]
    current = start_state
    for transition in path:
        current = transition.target_state
        steps.append(f"Trigger `{transition.trigger}`: {transition.source_state} -> {transition.target_state}")
    if not path:
        steps.append(f"State `{start_state}` is already covered by the initial condition.")
    return steps


def _states_from_path(start_state: str, path: list[StateTransition]) -> list[str]:
    states = [start_state]
    for transition in path:
        if transition.target_state not in states:
            states.append(transition.target_state)
    return states


def _build_all_states_plan(states: list[str], start_states: list[str], legal_transitions: list[StateTransition]) -> StateCoveragePlan:
    graph = _adjacency(legal_transitions)
    uncovered = set(states)
    sequences: list[StateTestSequence] = []
    sequence_index = 1

    for start_state in start_states:
        uncovered.discard(start_state)

    while uncovered:
        target_state = sorted(uncovered)[0]
        path = _shortest_path(graph, start_states, target_state)
        if path is None:
            sequences.append(
                StateTestSequence(
                    sequence_id=f"AS{sequence_index:02d}",
                    coverage_goal="All States",
                    steps=[f"Target state `{target_state}` is currently unreachable from the declared start states."],
                    covered_states=[],
                    covered_transitions=[],
                )
            )
            sequence_index += 1
            uncovered.discard(target_state)
            continue
        start_state = path[0].source_state if path else start_states[0]
        covered_states = _states_from_path(start_state, path)
        uncovered -= set(covered_states)
        sequences.append(
            StateTestSequence(
                sequence_id=f"AS{sequence_index:02d}",
                coverage_goal="All States",
                steps=_sequence_steps(path, start_state),
                covered_states=covered_states,
                covered_transitions=[transition.signature() for transition in path],
            )
        )
        sequence_index += 1

    if not sequences and start_states:
        sequences.append(
            StateTestSequence(
                sequence_id="AS01",
                coverage_goal="All States",
                steps=[f"Start in {start_states[0]}"],
                covered_states=start_states[:1],
                covered_transitions=[],
            )
        )
    covered_union = {state for sequence in sequences for state in sequence.covered_states}
    covered_union.update(start_states)
    return StateCoveragePlan(
        coverage_goal="All States",
        sequence_count=len(sequences),
        fully_covered=set(states).issubset(covered_union),
        sequences=sequences,
    )


def _build_all_transitions_plan(start_states: list[str], legal_transitions: list[StateTransition]) -> StateCoveragePlan:
    if not legal_transitions:
        return StateCoveragePlan(coverage_goal="All Transitions", sequence_count=0, fully_covered=True, sequences=[])

    graph = _adjacency(legal_transitions)
    uncovered = {transition.signature(): transition for transition in legal_transitions}
    sequences: list[StateTestSequence] = []
    sequence_index = 1

    while uncovered:
        seed_signature = sorted(uncovered)[0]
        seed = uncovered[seed_signature]
        prefix = _shortest_path(graph, start_states, seed.source_state) or []
        walk = prefix.copy()
        current_state = seed.source_state if not prefix else prefix[-1].target_state
        if current_state == seed.source_state and seed_signature in uncovered:
            walk.append(seed)
            uncovered.pop(seed_signature, None)
            current_state = seed.target_state
        elif seed_signature in uncovered and seed in graph.get(current_state, []):
            walk.append(seed)
            uncovered.pop(seed_signature, None)
            current_state = seed.target_state

        extended = True
        while extended:
            extended = False
            for transition in graph.get(current_state, []):
                signature = transition.signature()
                if signature not in uncovered:
                    continue
                walk.append(transition)
                uncovered.pop(signature, None)
                current_state = transition.target_state
                extended = True
                break

        start_state = walk[0].source_state if walk else start_states[0]
        sequences.append(
            StateTestSequence(
                sequence_id=f"AT{sequence_index:02d}",
                coverage_goal="All Transitions",
                steps=_sequence_steps(walk, start_state),
                covered_states=_states_from_path(start_state, walk),
                covered_transitions=[transition.signature() for transition in walk],
            )
        )
        for transition in walk:
            uncovered.pop(transition.signature(), None)
        sequence_index += 1

    covered_transition_signatures = {signature for sequence in sequences for signature in sequence.covered_transitions}
    return StateCoveragePlan(
        coverage_goal="All Transitions",
        sequence_count=len(sequences),
        fully_covered=covered_transition_signatures == {transition.signature() for transition in legal_transitions},
        sequences=sequences,
    )


def build_state_model(requirement_text: str, parsed: ParsedTrace) -> StateModel | None:
    if "State Transition" not in parsed.selected_techniques():
        return None

    start_states = []
    for rule in extract_rule_lines(requirement_text):
        content = re.sub(r"^\d+\.\s+", "", rule).strip()
        match = START_RE.search(content)
        if match:
            start_states.append(_title_or_original(match.group("state")))
    start_states = _dedupe_states(start_states)

    legal_transitions = _extract_legal_transitions(requirement_text, start_states)
    states = _dedupe_states(
        start_states
        + [transition.source_state for transition in legal_transitions]
        + [transition.target_state for transition in legal_transitions]
        + _extract_explicit_states(requirement_text)
    )
    illegal_transitions = _extract_illegal_transitions(requirement_text, states)

    notes: list[str] = []
    if not start_states:
        notes.append("No explicit start state was detected from the requirement text.")
    if not legal_transitions:
        notes.append("No explicit legal transitions were extracted from the requirement text.")

    coverage_plans = [
        _build_all_states_plan(states, start_states or states[:1], legal_transitions),
        _build_all_transitions_plan(start_states or states[:1], legal_transitions),
    ]

    return StateModel(
        states=states,
        start_states=start_states,
        legal_transitions=legal_transitions,
        illegal_transitions=illegal_transitions,
        coverage_plans=coverage_plans,
        notes=notes,
    )

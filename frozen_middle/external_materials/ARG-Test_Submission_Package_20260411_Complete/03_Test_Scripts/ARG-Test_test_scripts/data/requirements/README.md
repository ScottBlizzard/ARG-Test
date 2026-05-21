# Requirement Set

This scaffold ships with:

- `dev/`: 50 requirements for prompt tuning, checker tuning, and repair iteration
- `test/`: 16 requirements for final comparison and reporting

Current category balance:

- `dev`: 11 `input_validation`, 30 `business_rules`, 9 `workflow_state`
- `test`: 4 `input_validation`, 7 `business_rules`, 5 `workflow_state`

The test split is intentionally broader than the original scaffold so the final report can discuss:

- category-level generalization
- baseline comparisons on a less fragile test set
- workflow-heavy failure modes instead of mostly business-rule cases

Each requirement file should be plain text and contain:

1. requirement ID
2. short domain description
3. explicit rules or constraints
4. expected system behavior for valid and invalid inputs

When adding a new scenario, keep the repository consistent by updating all three assets together:

1. `data/requirements/<split>/<requirement_id>.txt`
2. `data/gold_specs/<split>/<requirement_id>.json`
3. `data/requirements/manifest.json`

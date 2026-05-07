from experiments.run_mutation_demo import build_mutation_demo_payload


def test_curated_coupon_cases_kill_all_seeded_mutants():
    payload = build_mutation_demo_payload()

    assert payload["reference_failures"] == []
    assert payload["mutant_count"] >= 4
    assert payload["killed_mutant_count"] == payload["mutant_count"]
    assert payload["kill_rate"] == 1.0
    assert all(mutant["killed_by"] for mutant in payload["mutants"])

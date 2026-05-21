# Mutants

Use this directory for optional executable evaluation.

Suggested layout:

```text
data/mutants/
├── password_policy/
│   ├── correct.py
│   ├── mutant_missing_special.py
│   └── mutant_off_by_one.py
└── shipping_fee/
    ├── correct.py
    └── mutant_free_shipping_threshold.py
```

This scaffold does not force a mutation framework. A simple script that runs generated tests against correct and buggy versions is enough for the course project.

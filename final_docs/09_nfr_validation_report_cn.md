# Non-Functional Requirements Validation Report

Date: 2026-05-07

This report formalizes the non-functional requirement evidence for the final ARG-Test submission. It is aligned with the teacher-provided `Requirement_Specification.md` and covers performance, usability, security, and maintainability.

Primary evidence files:

- `final_docs/execution_evidence/nfr_validation_summary.md`
- `final_docs/execution_evidence/nfr_validation_summary.json`

## 1. Performance

The controlled performance claim is scoped to the local/mock path because this is the part of the system controlled by the repository. Live LLM latency is provider-bound and is therefore discussed as external variance rather than used for deterministic NFR thresholds.

Latest local/mock benchmark:

- Sample size: `100` requirement jobs
- Unique requirement files used before cycling: `66`
- Total processing time: `0.3646 s`
- Average processing time per requirement: `0.0036 s`
- Maximum single-requirement processing time: `0.0056 s`
- NFR 4.1.1 local-path threshold, `100 requirements within 5 seconds`: `passed`
- NFR 4.1.2 local-path threshold, `single requirement within 2 seconds`: `passed`

Conclusion: the deterministic local path has a large margin against both performance thresholds. The final report should still state clearly that live provider calls may take longer and are not fully controlled by the tool.

## 2. Usability

The final system exposes both reproducible CLI workflows and a stable Web demo workflow.

Supported CLI commands:

- `run`
- `run-text`
- `batch`
- `batch-csv`
- `state-model`

Supported input modes:

- Plain requirement file
- Direct text input
- CSV batch input
- Built-in formal-example replay through the Web demo

The Web demo provides four main pages:

- Direct Input
- CSV Batch
- State Model
- Formal Evidence

The Direct Input page now also supports post-generation manual test-case editing and revised-suite export, which strengthens the required interactive review path rather than limiting the UI to one-shot generation only.

Conclusion: the final system exceeds the minimal input requirement because it supports plain files, direct text, CSV batches, and a frontend demonstration path.

## 3. Security

The course-project security goal is to prevent accidental credential exposure and keep generated artifacts auditable.

Validated controls:

- API keys are expected to be injected through `.env` or environment variables.
- Runtime manifests record provider/model metadata but do not record API keys.
- Generated/report artifacts are scanned for obvious secret leakage.

Latest result:

- Secret leak found in generated/report artifacts: `false`
- Manifests record provider metadata without API key disclosure: `true`

Conclusion: the project satisfies the course-level security requirement. Final submission should still avoid uploading `.env` files, API tokens, or screenshots containing credentials.

## 4. Maintainability

Maintainability is supported through modular implementation, isolated experiment outputs, automated tests, and documented evidence paths.

Latest repository evidence:

- `src/` Python modules: `27`
- Experiment scripts: `19`
- Test files: `8`
- Automated test cases: `45`
- Pytest summary: `45 passed, 1 warning in 1.41s`
- Runtime output isolation supported: `true`

Key maintainability structures:

- `src/` for the tool implementation
- `experiments/` for formal runs, baselines, ablation, replay, and validation
- `tests/` for regression and executable evidence
- `final_docs/` for required course documents
- `report_assets/` for final report, figures, demo package, and presentation support

Conclusion: maintainability is now supported by implementation structure and executable evidence rather than by narrative claims only.

## 5. Summary

The NFR package now gives explicit evidence for all four non-functional dimensions:

- Performance is measured against the teacher's local-path thresholds and passes both.
- Usability is demonstrated through CLI and Web workflows.
- Security is supported by secret-separation and artifact scanning.
- Maintainability is supported by modular code, tests, scripts, documentation, and isolated result roots.

Therefore, NFR validation can be treated as a formal, evidence-backed part of the final submission.

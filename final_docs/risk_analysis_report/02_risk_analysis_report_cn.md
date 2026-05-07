# Risk Analysis Report

## 1. Purpose and Scope

This document analyzes the main delivery and quality risks of the final `ARG-Test` submission. The scope covers:

- the AI-driven AutoTestDesign tool itself
- the frozen formal result bundle used by the final report
- the independent final documents and evidence package
- the demo and presentation readiness of the submission

The goal is not only to enumerate risks, but also to show which risks were already controlled during the final upgrade and which residual risks still need to be stated honestly in the submission.

## 2. Risk Scoring Method

Each risk is evaluated with three 1-to-5 dimensions:

- `Impact`: how much the risk would damage correctness, defensibility, or grading outcome
- `Likelihood`: how likely the risk is to occur in the current repository and evidence state
- `Detectability`: how hard it is to detect the risk before submission

The final priority score is:

`Risk Priority = Impact x Likelihood x Detectability`

Priority bands used in this report:

- `High`: `>= 60`
- `Medium`: `36-59`
- `Low`: `<= 35`

## 3. Priority Overview

![Risk Priority Heatmap](figures/risk_priority_heatmap.png)

Figure 1 is useful because it makes the project posture immediately visible. The current high-priority risks are no longer "missing functionality" risks; they are mostly evidence, consistency, and interpretation risks. This is a good sign for a final project because it means the technical system is already substantially complete and the remaining work is about making the submission defensible.

## 4. Risk Register

| Risk ID | Risk statement | Impact | Likelihood | Detectability | Priority | Band | Current status | Main mitigation | Evidence / owner |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| R1 | Final showcase examples could still contain overly templated wording or weak expected-result phrasing. | 5 | 4 | 3 | 60 | High | Controlled | Manually review final showcase cases and keep `coupon_discount_engine` as the anchor example. | Final report case-study sections and exported suites |
| R2 | `checker_score` and `overall_coverage` could be misinterpreted if the report explains only one of them. | 5 | 4 | 4 | 80 | High | Controlled | Always report both metrics together and explain why they measure different qualities. | Main comparison table and ablation discussion |
| R3 | Workflow/state requirements may generalize less consistently than rule-oriented requirements. | 4 | 4 | 3 | 48 | Medium | Residual but acceptable | Keep category-level generalization, add state-model evidence, and discuss the boundary honestly. | Generalization section and state-model exports |
| R4 | The final package could be challenged for lacking executable white-box evidence. | 5 | 5 | 5 | 125 | High | Closed | Add a reference implementation, executable `pytest` suite, branch/statement coverage, and mutation evidence. | `reference_impl/`, `tests/`, coverage XML, mutation demo |
| R5 | The report could cite non-canonical or mock-only results instead of the approved formal result source. | 5 | 3 | 5 | 75 | High | Controlled | Freeze a single formal result root and reference it consistently across report and figures. | `.local_runs/formal_qwen_novpn` manifests and summaries |
| R6 | Independent documents could drift away from each other in terminology, scope, or selected evidence. | 4 | 3 | 3 | 36 | Medium | Controlled | Reuse the same selected module, architecture, result source, and metric definitions across all documents. | `final_docs/` package |
| R7 | Evidence may exist in the repository but be difficult to locate during presentation or Q&A. | 4 | 3 | 4 | 48 | Medium | Controlled | Organize evidence under `final_docs/execution_evidence/` and keep a single source map in the final package. | `05_evidence_and_submission_checklist_cn.md` |
| R8 | Schedule and cost estimation could look generic and weaken the professionalism of the test plan. | 3 | 4 | 3 | 36 | Medium | Controlled | Use concrete phases, named responsibilities, and person-day estimates instead of template wording. | Final test plan |
| R9 | Repository entry points and document references could become inconsistent after the final upgrade. | 2 | 3 | 5 | 30 | Low | Controlled | Keep `README`, `final_docs`, and report references synchronized. | Root `README.md` and `final_docs/README.md` |
| R10 | Reviewers could confuse frozen middle-phase artifacts with final deliverables. | 3 | 2 | 4 | 24 | Low | Controlled | Isolate historical materials under `frozen_middle/` and cite final assets from current paths only. | `frozen_middle/README.md` and final package structure |

## 5. High-Priority Risk Analysis

### R2. Metric interpretation risk

This is a genuine grading risk because a reviewer could ask why a method with a high checker score does not automatically imply maximal coverage. The final submission already addresses this well:

- the main comparison reports `checker_score`, `overall_coverage`, and `test_count` together
- the ablation section now uses the same numbers as the main comparison table
- the final report explicitly explains that the checker measures contract consistency, while coverage measures obligation breadth

Residual action:

- keep this explanation consistent in the PPT and demo script

### R4. Missing executable white-box evidence

This was the most serious technical gap after the middle phase, and it is now closed. The project includes:

- `reference_impl/coupon_discount_engine.py`
- `tests/test_coupon_discount_engine_blackbox.py`
- `tests/test_coupon_discount_engine_whitebox.py`
- `100%` statement coverage
- `100%` branch coverage
- a `4/4` mutant kill demonstration

Residual action:

- none beyond keeping the cited evidence paths stable

### R5. Non-canonical result citation

This risk matters because final projects often lose credibility when numbers are copied from exploratory runs, mock outputs, or inconsistent reruns. The project now avoids that failure mode by using a single canonical formal result root for the report:

- `.local_runs/formal_qwen_novpn`

Residual action:

- do not introduce any new report table or PPT number that is not traceable to this formal root or to the dedicated execution evidence files

### R1. Showcase realism

Even strong pipelines can look weak if the two or three demo examples are phrased poorly. This is why showcase realism remains a high-priority delivery risk. The mitigation is already practical:

- anchor the detailed execution on `coupon_discount_engine`
- keep one strong input-validation example
- keep one strong workflow/state example
- manually inspect only the final showcased examples rather than attempting to hand-polish the full dataset

## 6. Medium-Priority Risks and Accepted Boundaries

The remaining medium-priority risks should be managed by explicit wording rather than by pretending they do not exist.

### R3. Workflow/state generalization

This is a methodological boundary, not a project failure. The correct final stance is:

- the workflow/state category is covered
- state-model extraction and sequence planning are implemented
- the category still deserves an honest "limitations" note

### R6 and R7. Cross-document consistency and evidence discoverability

These are final-package engineering risks. They are best controlled by a single submission discipline:

- same architecture figure across report and test plan
- same selected module across risk report, test plan, detailed execution, and final report
- same evidence filenames across all documents

### R8. Generic schedule and cost language

This risk can reduce the perceived professionalism of the final package even when the technical work is strong. The solution is simple and already adopted in the revised test plan:

- named responsibilities
- explicit phases
- person-day estimates
- concrete exit criteria

## 7. Residual Risks Accepted in the Final Submission

Some risks should remain visible because hiding them would weaken the credibility of the final project.

Accepted residual risks:

- the live provider is not perfectly deterministic, so strict reproducibility claims must rely on frozen generations plus replay
- workflow/state requirements are supported, but they remain more sensitive to requirement phrasing than some business-rule cases
- final showcase examples still benefit from one round of human review before presentation

These residual risks are acceptable because they are already bounded by evidence, explicitly documented, and do not invalidate the core project claims.

## 8. Conclusion

The final risk posture of `ARG-Test` is strong. The most important risks after the middle phase were not feature ideas but final-delivery risks: missing executable white-box evidence, inconsistent result citation, and weak explanation of evaluation metrics. Those high-priority risks are now either closed or clearly controlled. The remaining risks are presentation- and interpretation-oriented, which is the expected state of a strong course final project near submission.

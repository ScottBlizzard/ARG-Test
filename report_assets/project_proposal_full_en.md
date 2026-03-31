# ARG-Test Project Proposal

## Project Title

ARG-Test: Auditable Requirement-Driven Black-Box Test Generation with Structured LLM Reasoning and Contract Verification

## Team Information

- Team ID: TBD
- Member Names: TBD
- Student IDs: TBD

## Compact Outline

- Problem: free-form LLM test generation is convenient but hard to audit, verify, and compare.
- Core idea: force the model to output a five-section testing trace, then validate it with technique-specific contracts.
- Method modules: prompt builder, structured trace generator, parser, checker, reranker, repair, exporter, evaluator.
- Evaluation: compare against rule-based, plain LLM, and structured-no-checker baselines on requirement coverage and test quality.
- Deliverables: prompts, model settings, generated artifacts, final test suites, report, PPT, and test scripts.

## Abstract

Black-box test design from natural-language requirements is time-consuming and error-prone, especially when testers must cover valid cases, invalid cases, boundaries, and rule combinations under limited time. Large language models can reduce this workload, but their free-form outputs are difficult to audit because the reasoning process is implicit, the chosen testing technique is often unclear, and missing coverage is hard to detect automatically. This project proposes ARG-Test, an AI-assisted black-box testing tool that converts requirement documents into auditable test suites through structured reasoning and contract verification. Instead of asking the model to directly produce test cases, ARG-Test constrains the model to generate a five-section testing trace: Analysis, Pattern, Steps, Verification, and FinalAnswer. The trace is parsed and validated by technique-specific checkers for Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing, and optional State Transition Testing. The system then reranks multiple candidates and performs targeted repair when the generated suite violates coverage or structure constraints. We plan to evaluate ARG-Test against traditional rule-based generation, plain LLM prompting, and structured prompting without verification on a mixed requirement set covering input validation, business rules, and workflow behavior. The project aims to show that structured reasoning and contract-aware control can make AI-generated test design more complete, more explainable, and more usable for software testing practice.

Claim-Evidence Map:
- Claim: Free-form LLM outputs are hard to audit for testing coverage. | Evidence: explicit motivation from assignment scope and reference paper design philosophy. | Status: supported.
- Claim: ARG-Test can provide a more auditable testing workflow than direct prompting. | Evidence: method design with structured trace, parser, and checker modules. | Status: supported for design, needs evidence for empirical advantage.
- Claim: ARG-Test will improve completeness and explainability over plain prompting. | Evidence: planned comparison and ablation experiments. | Status: needs evidence.

## 1. Introduction

[Opening] Requirement-driven black-box testing is a practical and important software testing task because many projects begin from textual requirements long before a stable codebase or executable test oracle is available. In this setting, testers must derive valid and invalid partitions, boundary cases, and rule-based scenarios from natural-language descriptions, and the quality of this manual work directly affects later verification quality.

[Challenge] Although large language models are attractive for this task, direct prompting is not enough for a rigorous testing workflow. A model may produce plausible test cases, but it may also omit key invalid classes, miss just-below or just-above boundary points, merge several test design techniques without justification, or invent expected outputs that are not grounded in the requirement text. These failures are especially problematic because they are difficult to detect if the model output is only a free-form list of test cases.

[Method] Our project addresses this gap with ARG-Test, a requirement-driven black-box testing pipeline inspired by the structured reasoning and verification strategy in the reference paper. The key idea is to move from free-form generation to an auditable interface: the model must first expose a structured testing trace, and the system must then validate whether that trace satisfies the logic of the claimed testing technique. This design separates generation from verification and turns hidden reasoning into a checkable artifact.

[Advantage] This project is well aligned with the assignment for three reasons. First, it directly matches the required input-output form of requirement documents to test cases. Second, it supports several standard black-box techniques taught in software testing, including EP, BVA, Decision Table Testing, and State Transition Testing. Third, it naturally supports the required project report dimensions: comparison with non-AI methods, coverage analysis, failure-mode analysis, and discussion of AI limitations.

[Evidence plan] Our evaluation plan focuses on whether structure and verification actually add value beyond plain prompting. We will compare ARG-Test with a traditional rule-based baseline, a plain LLM baseline, and a structured-no-checker baseline, and we will analyze not only final coverage but also checker pass rate, redundancy, and optional executable usefulness. This design lets us test both effectiveness and causality.

Claim-Evidence Map:
- Claim: Requirement-driven black-box testing is a meaningful task for the assignment. | Evidence: assignment explicitly allows requirement input and black-box test-case output. | Status: supported.
- Claim: Direct prompting is insufficient for auditable test design. | Evidence: known failure modes and reference paper motivation about free-form traces. | Status: supported for motivation, needs empirical evidence for this project instance.
- Claim: Structured reasoning plus checking is the central contribution of ARG-Test. | Evidence: proposed pipeline and implementation scaffold. | Status: supported.

## 2. Background and Motivation

[Background] Black-box testing techniques provide complementary ways to derive test cases from requirements. Equivalence Partitioning groups inputs into representative valid and invalid classes. Boundary Value Analysis targets values around lower and upper limits. Decision Table Testing captures combinations of conditions and actions. State Transition Testing models workflow behavior across states and triggers. Together, these techniques form a strong basis for requirement-driven testing.

[Gap] However, manual application of these techniques is labor-intensive and inconsistent. Testers must first identify constraints in the requirement text, then decide which testing technique is appropriate, and finally translate the resulting reasoning into executable or at least reviewable test cases. In student projects and small development teams, this process is often too slow and too dependent on individual experience.

[Motivation] AI can reduce manual effort, but a useful AI testing tool should do more than generate text quickly. It should expose why a technique was selected, show how coverage was derived, allow automatic detection of omissions, and preserve artifacts needed for report writing and presentation. The reference paper is valuable here because it reframes reasoning quality as trace-contract consistency rather than as an inaccessible internal thought process. We adopt the same philosophy for software testing.

Claim-Evidence Map:
- Claim: Standard black-box techniques are suitable foundations for requirement-driven testing. | Evidence: software testing theory and assignment specification. | Status: supported.
- Claim: A useful AI testing tool must be auditable rather than only fluent. | Evidence: assignment deliverables require prompts, models, outputs, comparisons, and AI limitation analysis. | Status: supported.

## 3. Problem Definition

[Definition] We define the target task as follows: given a natural-language software requirement, generate a set of black-box test cases together with a structured testing trace and validation artifacts. The primary input is a requirement document. Optional supporting inputs may include field constraints, workflow descriptions, or business rules if they are available.

[Outputs] The system output contains five components. First, it returns a structured reasoning trace with Analysis, Pattern, Steps, Verification, and FinalAnswer. Second, it produces a normalized test-case table with fields such as test ID, technique, preconditions, input, expected output, covered item, priority, and checker status. Third, it records parser and checker results. Fourth, it exports machine-readable artifacts such as JSON and CSV. Fifth, it generates evaluation summaries for later reporting.

[Objectives] The project pursues four objectives. It should improve requirement coverage, especially over valid partitions, invalid partitions, and boundaries. It should reduce obvious omissions and contradictions in generated expected outputs. It should improve auditability by exposing the intermediate testing design process. It should support experimental comparison against AI and non-AI baselines.

[Challenges] The problem remains difficult because requirement text may be ambiguous, multiple testing techniques may apply simultaneously, and expected outputs may depend on hidden business assumptions. Moreover, a checker can validate structure and contract consistency, but it cannot fully guarantee semantic correctness. Our method therefore aims at reliable structure and diagnosable failure modes rather than a perfect proof of correctness.

Claim-Evidence Map:
- Claim: The task can be operationalized with structured inputs, outputs, and validation artifacts. | Evidence: implemented scaffold and explicit schema definitions. | Status: supported.
- Claim: Checker-based validation is helpful but not omnipotent. | Evidence: method design limits and reference paper argument about contract consistency. | Status: supported.

## 4. Research Questions

[Question set] We organize the project around four research questions.

1. RQ1: Compared with plain LLM prompting, does structured testing trace generation improve test-suite completeness and consistency?
2. RQ2: Does introducing technique-specific contract checking reduce missing invalid classes, missing boundaries, incomplete rule coverage, or missing illegal transitions?
3. RQ3: Does candidate reranking with targeted repair improve the final selected suite beyond a single structured generation pass?
4. RQ4: How well does the method generalize across different requirement types such as input validation, rule-based business logic, and workflow/state behavior?

[Purpose] These questions separate effect from mechanism. RQ1 examines whether structure alone matters. RQ2 isolates the effect of checker-guided control. RQ3 studies the value of additional inference-time control. RQ4 ensures that the project does not only work on one convenient requirement category.

Claim-Evidence Map:
- Claim: The research questions align with the main design claims of the project. | Evidence: each research question maps to one module or design choice in the pipeline. | Status: supported.

## 5. Proposed Method

### 5.1 System Overview

[Overview] ARG-Test consists of seven modules: Requirement Preprocessor, Prompt Builder, Structured Trace Generator, Parser, Technique Contract Checker, Candidate Reranker and Repair Module, and Final Exporter with Evaluation Support. The overall pipeline takes a requirement document as input and converts it into one or more candidate traces. Each trace is parsed into typed sections, checked against schema and technique contracts, scored, optionally repaired, and exported as final testing artifacts.

[Need] This modular structure is necessary because the assignment demands more than final test cases. We must preserve prompts, model choices, raw outputs, parsed artifacts, and analysis results. A single free-form generation call cannot provide that level of control or reproducibility.

[Why it works] The system works because each module removes one specific failure mode. The structured prompt reduces format drift, the parser enforces the trace schema, the checkers detect missing obligations, the reranker prefers better candidates, and repair adds targeted fixes without rewriting the entire answer. This design keeps the pipeline inspectable and easy to present in a course setting.

### 5.2 Structured Testing Trace Schema

[Design] The core representation is a five-section testing trace. The Analysis section extracts fields, constraints, rules, states, and possible exceptions from the requirement. The Pattern section explicitly states which testing techniques are selected and why they are appropriate. The Steps section shows how the test designer derives partitions, boundaries, decision rules, or state transitions. The Verification section performs self-checking and must reference earlier steps. The FinalAnswer section contains the normalized test-case table.

[Motivation] This schema is needed because testing quality depends on the process used to derive the suite, not only on the final list of cases. If the method claims to use BVA, it should expose which boundaries were identified. If it claims to use Decision Table Testing, it should show which conditions and actions were mapped into rules. The trace therefore acts as an auditable interface between the model and the evaluator.

[Advantage] The schema provides three advantages. It makes parser-based validation possible, it supports direct report writing because the reasoning is already organized, and it enables targeted repair because failures can be localized to a specific section instead of treating the whole output as an opaque block.

### 5.3 Technique-Specific Contract Checkers

[Design] We define one generic schema checker and four technique-aware checkers. The schema checker verifies section order, non-empty content, Verification-to-Steps references, and parseable FinalAnswer tables. The EP checker verifies that the suite includes representative valid and invalid partitions. The BVA checker looks for lower-boundary, on-boundary, and upper-boundary style cases. The Decision Table checker verifies that rule-oriented cases are present and that rule mapping is explicit. The State Transition checker checks whether both legal and illegal transitions are covered.

[Motivation] These checkers are needed because a structured trace alone does not guarantee that the claimed testing logic is complete. A model may produce a beautifully formatted answer that still omits invalid cases or fails to distinguish legal and illegal workflow transitions. The contract layer turns testing theory into concrete obligations.

[Advantage] The checker design is intentionally lightweight and practical. It does not attempt full formal semantics. Instead, it provides deterministic structure validation, transparent diagnostics, and interpretable pass or fail signals that are suitable for a course project. This trade-off gives us control without creating an unnecessarily brittle system.

### 5.4 Candidate Reranking and Repair

[Design] For each requirement, the system can sample multiple candidate traces. Each candidate receives a score based on schema validity, checker pass rate, and duplicate penalties. The reranker selects the best candidate. If the selected candidate still falls below a quality threshold, the repair module either issues a repair prompt or performs targeted local repair by inserting missing representative cases and removing duplicates.

[Motivation] Candidate control is needed because LLM outputs vary across runs. A single sample can fail due to a small omission even when a second sample is much better. Reranking uses checker-backed signals to exploit this diversity, while repair addresses common omissions without requiring a full restart.

[Advantage] This module connects directly to our research questions. It lets us test whether structure, checking, and control each contribute measurable gains. It also creates clear ablation conditions for the report.

Claim-Evidence Map:
- Claim: Each module has a clear role in the full pipeline. | Evidence: explicit module decomposition and implemented repository scaffold. | Status: supported.
- Claim: The schema and checker design enable auditable trace validation. | Evidence: parser and checker architecture. | Status: supported.
- Claim: Reranking and repair should improve final suite quality. | Evidence: planned ablation experiments. | Status: needs evidence.

## 6. Implementation Plan

[Implementation] The system will be implemented in Python. The repository already contains directories for prompts, requirements, gold specifications, outputs, artifacts, checkers, baselines, evaluation scripts, and report assets. The main entry point runs the full pipeline over one requirement or a split of requirements. Raw generations, parsed traces, checker logs, final tests, and summary reports are saved automatically.

[Model interface] The scaffold currently supports a mock provider for local dry-runs and a provider interface for real API calls. In the final version, we will connect the tool to a real LLM, record the model name and inference configuration, and preserve both prompts and raw generations as required by the assignment.

[Artifacts] We will export final tests as Markdown, CSV, and JSON. This format supports both human review and downstream analysis. The final repository will also preserve baseline outputs, ablation summaries, and any optional executable evaluation artifacts.

Claim-Evidence Map:
- Claim: The project is implementable within the assignment scope. | Evidence: repository scaffold, CLI scripts, datasets, and export paths already exist. | Status: supported.
- Claim: The implementation design can preserve all required deliverables. | Evidence: explicit artifact directories and exporter design. | Status: supported.

## 7. Experimental Plan

### 7.1 Requirement Dataset

[Design] We plan to use a small but diverse requirement dataset. The development split will contain four requirements for prompt tuning, checker adjustment, and repair design. The test split will contain four to six held-out requirements for final reporting. Requirement types will include input validation, business-rule logic, and workflow/state behavior.

[Motivation] This split is necessary to avoid tuning directly on the final reported examples. Even in a small course project, separating development from evaluation improves the credibility of the analysis.

### 7.2 Baselines

[Design] We will compare ARG-Test with three baselines. The first baseline is a traditional rule-based generator that maps explicit requirement patterns to representative tests. The second baseline is a plain LLM baseline that asks the model to generate test cases directly. The third baseline is a structured-no-checker baseline that keeps the five-section trace but removes checker-aware control.

[Why these baselines] These baselines answer different questions. The rule-based baseline anchors the comparison against non-AI automation. The plain LLM baseline measures the value of structure. The structured-no-checker baseline isolates the effect of contract verification and repair.

### 7.3 Metrics

[Outcome metrics] We will evaluate requirement coverage, valid partition coverage, invalid partition coverage, boundary coverage, decision-rule coverage, transition coverage, exception coverage, and redundancy. Where possible, we will also assess expected-output consistency.

[Process metrics] We will report schema validity, checker pass rate, repair rate, and duplicate count. These metrics are important because the reference paper emphasizes that structure quality and correctness should not be collapsed into a single number.

[Optional practical metrics] If time allows, we will add an executable usefulness study by writing small reference implementations and seeded mutants for a subset of requirements, then converting generated tests into simple scripts or pytest cases. This would allow us to measure executable test rate and mutation kill rate.

### 7.4 Generalizability and Ablation

[Generalizability] We will analyze whether the method behaves differently on validation-style, rule-based, and state-machine requirements.

[Ablation] We will compare plain LLM, structured-no-checker, and full ARG-Test. If time allows, we will also compare single-candidate generation against best-of-N reranking with repair.

Claim-Evidence Map:
- Claim: The planned experiments can test effectiveness, causality, and generalizability. | Evidence: comparison, ablation, and split design. | Status: supported as plan, needs execution for empirical support.

## 8. Comparison with Traditional Non-AI Techniques

[Comparison strategy] The proposal includes an explicit comparison with traditional non-AI methods because the assignment requires it. Our primary non-AI baseline is a rule-based template generator. This baseline will detect simple numeric ranges, derive representative boundary points, and build coarse rule-based tests when conditions are explicit.

[Interpretation] We do not expect the rule-based baseline to match the flexibility of the AI system on complex language, but it provides an important control. If ARG-Test outperforms it only slightly, then the additional complexity may not be justified. If ARG-Test provides clearly better coverage with reasonable trace quality, then the AI contribution becomes meaningful.

Claim-Evidence Map:
- Claim: A non-AI baseline is necessary for a complete course project comparison. | Evidence: assignment explicitly requires comparison with traditional non-AI techniques. | Status: supported.

## 9. Risks, Limitations, and Mitigation

[Risk] The main technical risk is semantic uncertainty in requirements. Some expected outputs may depend on assumptions not explicitly stated in the text.

[Mitigation] We mitigate this by keeping the system requirement-driven, by logging diagnostics, and by treating checker success as contract consistency rather than semantic proof.

[Risk] A second risk is overclaiming empirical benefit before experiments are complete.

[Mitigation] We avoid this by phrasing expected gains as hypotheses in the proposal and by designing experiments that can falsify our assumptions.

[Risk] A third risk is that lightweight checkers may miss subtle logical errors.

[Mitigation] This is acceptable for the course scope because our main objective is auditable and reproducible test design rather than full formal verification.

## 10. Expected Deliverables

[Deliverables] The final project submission will include the following:

- a project report in PDF format with cover information;
- a presentation deck in PDF format;
- a zipped codebase containing prompts, model settings, source code, and testing scripts;
- raw model outputs and parsed artifacts;
- final test suites in human-readable and machine-readable formats;
- experimental summaries and error analyses.

These outputs are already reflected in the repository structure.

## 11. Timeline

[Schedule] We propose the following execution order.

1. Finalize the requirement set and gold specifications.
2. Connect the scaffold to the target LLM and refine prompts.
3. Stabilize parser, checker, reranking, and repair behavior.
4. Run baseline and ablation experiments.
5. Summarize findings, build figures and tables, and finish the report and presentation.

## 12. Conclusion

[Conclusion] This project proposes ARG-Test, a requirement-driven AI black-box testing tool that emphasizes structure, validation, and auditability. The central idea is not to let an LLM freely produce test cases, but to require a typed testing trace and then verify whether that trace satisfies technique-specific testing obligations. This design fits the assignment well because it combines AI-assisted generation with classical software testing concepts and produces artifacts that are suitable for analysis, comparison, and presentation. If the planned experiments support our hypotheses, the project will show that structured reasoning and contract-guided control are a practical way to improve the quality and transparency of AI-generated test design.

Claim-Evidence Map:
- Claim: ARG-Test is a strong fit for the assignment and the reference paper. | Evidence: direct alignment between input/output requirements and the structured reasoning philosophy of the paper. | Status: supported.
- Claim: The project can demonstrate practical value if the planned experiments confirm the hypotheses. | Evidence: experimental design and implementation scaffold. | Status: needs evidence.

## Self-Review Checklist

- Clarity: each section has one clear purpose and stable terminology.
- Flow: the proposal moves from task, to challenge, to method, to experiments, to deliverables.
- Unsupported claims: empirical advantages are written as planned hypotheses rather than final results.
- Missing evidence: all performance claims still require execution of the baseline and ablation studies.
- Practical risk: checker validity is limited to contract consistency and should not be described as full semantic correctness.

## End-of-Draft Adversarial Review

### 1. Contribution

- What is new here? A structured, auditable requirement-to-test pipeline with technique-specific contracts.
- Is the contribution non-trivial? Yes for a course project, because it goes beyond direct prompting and includes validation/control.
- Remaining risk: the contribution may look incremental if experiments do not show a clear advantage over plain prompting.

### 2. Writing Clarity

- Is the pipeline reproducible from the text? Yes at a high level.
- Remaining risk: final report must include concrete model settings and checker details.

### 3. Experimental Strength

- Are strong enough baselines planned? Yes for the course scope.
- Remaining risk: if only mock outputs are shown, the empirical section will not be credible.

### 4. Evaluation Completeness

- Do the experiments test effectiveness and causality? Yes through comparison and ablation.
- Remaining risk: executable evaluation is still optional, so practical usefulness may remain under-supported.

### 5. Method Design Soundness

- Is the method realistic? Yes for requirement-driven testing support.
- Remaining risk: semantic ambiguity in requirements limits full correctness guarantees.

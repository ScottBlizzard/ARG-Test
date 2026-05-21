# ARG-Test Proposal Presentation Script

## Slide 1. Title

**Title**
ARG-Test: Auditable Requirement-Driven Black-Box Test Generation with Structured LLM Reasoning and Contract Verification

**On-slide bullets**
- Team ID
- Member names
- Student IDs

**Speaker script**
Good morning. Our project is called ARG-Test. It is an AI-assisted black-box testing tool that generates auditable test cases from natural-language software requirements. The core idea is simple: instead of asking an LLM to directly output a list of tests, we force it to produce a structured testing trace and then verify whether that trace satisfies the logic of the claimed testing technique.

## Slide 2. Problem and Motivation

**On-slide bullets**
- Requirement-driven test design is slow and error-prone
- Plain LLM prompting is convenient but unreliable
- Missing boundaries and invalid cases are hard to detect

**Speaker script**
Our task starts from software requirements, not from source code. In this setting, testers must manually derive valid cases, invalid cases, boundaries, and rule combinations from text. LLMs can help, but direct prompting creates a new problem: the output may look fluent while still missing important coverage. In particular, it is hard to know whether the model actually considered invalid partitions, boundary points, or rule combinations.

## Slide 3. Why Plain LLM Is Not Enough

**On-slide bullets**
- Free-form reasoning is opaque
- Technique choice is often implicit
- Expected outputs can be inconsistent
- Missing coverage is difficult to audit

**Speaker script**
The limitation of plain prompting is not only accuracy. The deeper issue is auditability. If the model gives us only a table of test cases, we cannot easily inspect why a certain case was produced, why another one was omitted, or whether the model really followed EP, BVA, or Decision Table logic. This is exactly the gap we want to solve.

## Slide 4. Key Insight

**On-slide bullets**
- Adopt the reference paper's philosophy
- Turn hidden reasoning into typed artifacts
- Validate trace-contract consistency

**Speaker script**
The key insight comes from the reference paper. Instead of treating model reasoning as a hidden internal process, we expose it as a typed artifact that can be parsed and checked. For our testing project, that means the model must first output a structured testing trace, and then we verify whether this trace is consistent with the claimed testing logic.

## Slide 5. Project Goal and Research Questions

**On-slide bullets**
- RQ1: does structure help?
- RQ2: does contract checking help?
- RQ3: do reranking and repair help?
- RQ4: does the method generalize across requirement types?

**Speaker script**
Our project is organized around four research questions. First, we test whether structured output is better than plain prompting. Second, we test whether contract checking reduces missing coverage. Third, we test whether reranking and repair improve the final suite. Finally, we test whether the method works across different requirement categories such as validation rules, business logic, and workflow transitions.

## Slide 6. ARG-Test Framework

**On-slide bullets**
- Requirement input
- Prompt builder
- Structured trace generator
- Parser and contract checker
- Reranker and repair module
- Final test exporter and evaluator

**Speaker script**
This slide shows the full pipeline. We start from a requirement document. The prompt builder asks the model for a structured testing trace. The parser extracts typed sections. The checker validates schema quality and technique-specific obligations. Then the reranker selects the best candidate, and the repair module fixes common omissions. Finally, the exporter produces test suites and evaluation artifacts.

## Slide 7. Structured Testing Trace Schema

**On-slide bullets**
- Analysis
- Pattern
- Steps
- Verification
- FinalAnswer

**Speaker script**
The trace has exactly five sections. Analysis extracts fields, constraints, rules, and states. Pattern explicitly selects testing techniques such as EP, BVA, Decision Table, or State Transition. Steps explains how the suite is derived. Verification checks whether earlier steps were covered. FinalAnswer exports the final normalized test table. This schema makes the generation process auditable instead of opaque.

## Slide 8. Technique-Specific Contracts

**On-slide bullets**
- EP: valid and invalid partitions
- BVA: below, on, and above boundaries
- Decision Table: rule-oriented mapping
- State Transition: legal and illegal transitions

**Speaker script**
A structured trace alone is not enough, so we add technique-specific contracts. If the trace claims to use Equivalence Partitioning, we expect representative valid and invalid classes. If it claims Boundary Value Analysis, we expect lower and upper boundary coverage. If it claims Decision Table or State Transition, we expect corresponding rule or transition coverage. This is how we translate testing theory into automatic checks.

## Slide 9. Baselines and Experimental Plan

**On-slide bullets**
- Traditional rule-based baseline
- Plain LLM baseline
- Structured-no-checker baseline
- Full ARG-Test

**Speaker script**
Our experiments are designed to test both effectiveness and causality. We compare against a traditional rule-based generator, a plain LLM baseline, and a structured-no-checker baseline. This lets us isolate the value of structure, checking, and control. We will use a small but diverse requirement set split into development and test subsets.

## Slide 10. Metrics

**On-slide bullets**
- Valid and invalid partition coverage
- Boundary coverage
- Decision-rule or transition coverage
- Redundancy and checker pass rate
- Optional executable usefulness

**Speaker script**
We will not use only one final score. Instead, we separate outcome metrics from process metrics. Outcome metrics include coverage and redundancy. Process metrics include schema validity, checker pass rate, and repair behavior. If time allows, we will also add executable usefulness by running generated tests on small reference implementations.

## Slide 11. Repository and Current Progress

**On-slide bullets**
- Project scaffold already implemented
- Sample requirements and gold specs prepared
- Parser, checker, baseline, and experiment scripts ready
- Mock end-to-end execution verified

**Speaker script**
We have already built the repository scaffold. It contains prompts, sample requirements, gold specifications, parser and checker modules, baseline scripts, experiment scripts, and report assets. The current version runs end-to-end in mock mode, which allows us to verify the structure before we plug in a real LLM provider.

## Slide 12. Deliverables and Risks

**On-slide bullets**
- Report PDF
- PPT PDF
- Zipped code and test scripts
- Prompts, raw outputs, parsed artifacts
- Main risk: semantic ambiguity in requirements

**Speaker script**
Our final deliverables match the assignment directly: a report, a presentation deck, a zipped codebase, prompts, raw model outputs, parsed traces, and final test suites. The main technical risk is semantic ambiguity in the requirement text, so we present checker success as contract consistency rather than full proof of semantic correctness.

## Slide 13. Conclusion

**On-slide bullets**
- Not just LLM-generated tests
- Structured, auditable, and repairable pipeline
- Strong fit for the assignment

**Speaker script**
To conclude, our project is not simply about using an LLM to generate test cases. It is about turning the test design process into a structured, auditable, and repairable pipeline. This makes the project well aligned with both the assignment requirements and the structured reasoning philosophy of the reference paper.

## Short Q&A Preparation

### Q1. What kind of testing does your project belong to?
It is requirement-driven black-box testing, mainly covering Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing, and optional State Transition Testing.

### Q2. What is the difference between your method and plain LLM prompting?
Plain prompting asks the model to directly output test cases. Our method first forces the model to produce a structured testing trace, then parses and checks that trace, and finally reranks or repairs the result.

### Q3. Does the checker prove the test suite is correct?
No. It validates trace-contract consistency and catches important omissions, but it does not provide full semantic proof.

### Q4. Why not choose static analysis instead?
Because this project is centered on requirement-to-test generation, which better matches the reference paper's structured reasoning idea and the assignment's black-box testing options.

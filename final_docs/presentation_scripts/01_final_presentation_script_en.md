# Final Presentation Script (English)

This script is based on the current final deck:

- `07_PPT_Assets_For_Luowu/final_ppt.pdf`

Recommended total length:

- about `15` minutes
- `5` speakers
- suggested pacing:
  - Speaker 1: `2.5` minutes
  - Speaker 2: `2.5` minutes
  - Speaker 3: `3.5` minutes
  - Speaker 4: `3.5` minutes
  - Speaker 5: `3.0` minutes

Recommended speaker split:

- Speaker 1: Slides `1` to `4`
- Speaker 2: Slides `5` to `7`
- Speaker 3: Slides `8` to `10`
- Speaker 4: Slides `11` to `16`
- Speaker 5: Slides `17` to `20`

You can replace `Speaker 1` to `Speaker 5` with real member names during rehearsal.

---

## Speaker 1

**Slides 1 to 4**

**Target time:** about `2.5 minutes`

Good morning everyone. We are Group 7, and our project is called ARG-Test, an auditable and risk-aware requirement-driven black-box test generation pipeline.

Our project contains three clearly separated parts. First, ARG-Test is the AutoTestDesign tool that we developed. Second, MiniShop Checkout is the independent target application under test. Third, coupon_discount_engine is the selected major module inside MiniShop Checkout that we use for detailed test design and execution.

This separation helps us keep the whole project easy to follow. It tells us what the tool is, what the application under test is, and where the strongest execution evidence comes from.

It also keeps the rest of our materials aligned, because the same structure is used in the reports, the PPT, and the demo.

MiniShop Checkout is a compact e-commerce checkout prototype adapted from a previous small course project and selected here as the independent target application. Its scope includes promotion and coupon handling, shipping-fee calculation, tax and order-total calculation, payment-card validation, pickup-contact validation, and checkout preview orchestration. At the same time, we keep refund workflows, inventory synchronization, and external gateway integration out of scope, so that the application remains small, concrete, and testable.

The motivation for ARG-Test comes from a simple observation. A plain LLM can produce fluent test suggestions, but fluent output is not the same as auditable test design. If the model only says "try a valid coupon" or "try an expired coupon," we still do not know whether invalid partitions are covered, whether boundary neighbors are covered, or whether the claimed testing technique is actually reflected in the final suite.

So the deeper issue is not only correctness. The deeper issue is auditability and traceability. We want a system that can explain how it moves from a natural-language requirement to a structured, reviewable, and exportable test suite.

That is the motivation for the rest of the presentation. We will show how ARG-Test turns plain generation into structured, checked, and traceable test design, and how we apply that tool to a concrete target application.

So the story of this project is not only about producing tests. It is about making the whole testing process more usable and more reviewable.

---

## Speaker 2

**Slides 5 to 7**

**Target time:** about `2.5 minutes`

I will explain how ARG-Test works as a system.

The key idea is that ARG-Test is a pipeline, not a single prompt. Instead of asking the model to directly output a final list of tests, we organize the workflow into several stages: structured generation, parser and schema gate, technique-aware checking, reranking and targeted repair, and finally export, evaluation, and reproducible reporting.

This design is important because each stage has a different responsibility. Generation produces candidate suites, checking verifies obligation coverage, and reranking plus repair help us select a stronger final result.

The structured trace is one of the most important parts. The model is guided to produce a typed trace with five parts: Analysis, Pattern, Steps, Verification, and FinalAnswer. This matters because it transforms the output into something that can be parsed and checked instead of something that only sounds reasonable to a human reader.

On top of that, we apply technique-aware contract checking. In our system, this includes an equivalence partition checker, a boundary value checker, a decision checker, and a state checker. These checkers do not claim full semantic proof, but they do verify whether the generated trace and final suite actually contain the obligations implied by the selected testing techniques.

So the model output is not treated as final truth. It becomes a typed artifact that can be parsed, checked, compared, reranked, and, when necessary, repaired.

The next slide connects this design to the course requirements. In terms of mandatory closure, our final system covers FR 1.0, FR 1.1, FR 2.0, FR 3.0, and FR 6.0. In addition, we also implemented the extra-credit parts FR 4.0, FR 5.0, and FR 7.0.

Another important requirement from the assignment is interactive review. Our system provides four practical review surfaces: Direct Input, CSV Batch, State Model, and Formal Evidence.

This gives the tester more than one way to work with the tool, depending on whether the task is single-case review, batch input, workflow inspection, or evidence presentation.

Most importantly, the tester is not passive. The tester can inspect outputs, revise review guidance, rerun the pipeline, and even edit generated test cases after generation and export a revised suite. This is how we make designer participation concrete in the final tool.

So at this point, our main message is that ARG-Test is not just generation. It is generation plus structure, checking, review, and controlled revision.

That combination is what makes the system closer to a practical AutoTestDesign workflow.

---

## Speaker 3

**Slides 8 to 10**

**Target time:** about `3.5 minutes`

I will focus on the application-facing planning artifacts: the risk analysis and the test plan.

Because our target application is MiniShop Checkout, the risk analysis is centered on MiniShop Checkout. We score risks with a simple formula: Risk Priority equals Impact times Likelihood times Detectability, and then divide the results into high, medium, and low priority bands.

These documents are built on structured evidence generated by ARG-Test, including requirement traces, technique selections, risk scores, recommended focus areas, checker diagnostics, and exported test suites.

From this analysis, the highest-risk areas are coupon and promotion logic, shipping and tax calculation, payment-card validation, and checkout orchestration. Pickup validation is still important, but its overall impact is narrower.

This prioritization directly shapes the test plan. The scope includes promotion and pricing, shipping and tax, payment validation, pickup validation, and checkout orchestration. Architecturally, the application is organized around a Checkout Service that coordinates Promotion, Shipping, Tax, Payment Validation, and Pickup Validation.

Based on this structure, we designed a promotion suite, a shipping and tax suite, a payment validation suite, a pickup validation suite, a checkout orchestration suite, and finally a detailed executable module suite focused on coupon_discount_engine.

In other words, the test plan is not a generic checklist. It is directly mapped to the architecture and the main risk clusters of the target application.

Our execution flow is also straightforward: freeze the application scope, finish the risk analysis, review generated suites, execute the detailed module tests, and package the final evidence. For execution, we chose pytest with coverage.py, because MiniShop Checkout is implemented in Python and this combination fits both black-box and white-box validation.

We also included cost estimation, as required by the assignment. Our estimate is about four and a half to seven person-days with ARG-Test, compared with roughly seven and a half to ten person-days for a manual baseline. So the tool does not remove human review, but it does reduce the cost of requirement decomposition, first-pass suite generation, prioritization, and traceability maintenance.

In other words, the plan is not only technically reasonable. It is also realistic in terms of team effort and project pacing.

So these two documents, the risk report and the test plan, explain how we systematically test the target application and how that plan is grounded in structured evidence.

They give the project a clear application-facing logic, from risk identification to suite execution.

---

## Speaker 4

**Slides 11 to 16**

**Target time:** about `3.5 minutes`

I will now present the experimental setup and the main tool-level results.

Our evaluation uses a frozen test split with sixteen requirements. Freezing the test set makes the final comparison stable and defensible. We compare ARG-Test against three baselines: a rule-based baseline, a plain LLM baseline, and a structured-no-checker baseline.

The main scorecard shows that on these sixteen frozen requirements, ARG-Test reaches an average checker score of 0.959, an average overall coverage of 0.615, and zero duplicate cases.

This matters because the full pipeline is stronger than all three weaker alternatives. Compared with the rule-based baseline, it shows better requirement understanding. Compared with plain LLM, it shows that prompting alone is not enough. Compared with structured no-checker, it shows that checker-guided control adds real value rather than only better formatting.

We also looked at generalization and ablation. The method generalizes across business-rule, input-validation, and workflow-state requirements. In the ablation view, the most honest interpretation is that checker-guided control greatly improves checker alignment while keeping coverage broadly comparable. So the checker layer is not decorative; it changes the quality of the final selected suite.

The representative cases page adds three concrete examples: business-rule logic, input validation, and payment validation. Together, these examples show that the method is not overfitted to one narrow requirement type.

They also make the evaluation more interpretable, because we can see the method working on different styles of rules instead of only looking at aggregate numbers.

So the tool-level evidence supports two clear claims. First, ARG-Test runs across a meaningful range of requirement styles. Second, the structured and checked pipeline is materially better than weaker baselines on the frozen evaluation setting.

That is why we treat these experiments as support for the tool design, not just as isolated benchmark numbers.

This prepares the transition to the last part of the talk, where we move from design-level evidence to executable evidence.

---

## Speaker 5

**Slides 17 to 20**

**Target time:** about `3.0 minutes`

I will conclude with the strongest execution evidence, as well as the final boundaries of the project.

Inside MiniShop Checkout, we selected coupon_discount_engine as the major module for detailed test design and execution. We chose it because it is a high-risk financial-rule component with thresholds, invalid cases, rule combinations, and clear expected results. So it is a strong place to prove that our requirement-driven design can become real executable tests.

This gives us more than design-level metrics. It gives us executable evidence. In the final version, the selected module is supported by black-box tests, white-box tests, full statement coverage, full branch coverage, and mutation-based usefulness evidence. At the repository level, our current regression suite also passes consistently.

That is an important step for the project, because it connects requirement-driven design with real test execution rather than stopping at generation quality alone.

We also paid close attention to reproducibility and practical validation. Under seeded mock control, the repository-level chain is deterministic. For live providers, we remain honest: variance still exists. That is why our submission-level reproducibility does not rely on overclaiming live determinism. Instead, we use frozen generations plus replay to guarantee that the formal examples shown in the demo and report can be reconstructed.

The limitations page is also important. We stay inside the requirement-driven branch. Our evaluation is course-scale rather than a large public benchmark. Coverage still depends on manually authored gold specifications. And live providers still show residual nondeterminism. We treat these as clear project boundaries.

Being explicit about these boundaries makes our final claims more credible, because we are clear about both strengths and limits.

So to conclude, our main message is this. Structured reasoning makes black-box test design auditable. The full ARG-Test pipeline beats both non-AI and weaker AI baselines. And the final submission is not just a prompt demo. It includes the tool itself, structured exported evidence, an application-facing risk report and test plan built on that evidence, a detailed execution document for a selected module, and reproducible final artifacts.

Thank you. We are ready for questions.

---

## Short Handoff Notes

### Recommended speaking order

1. Speaker 1: title, target application, project motivation
2. Speaker 2: architecture, structured trace, checker, interactive review
3. Speaker 3: risk report and test plan
4. Speaker 4: experiments and benchmark results
5. Speaker 5: executable evidence, reproducibility, limitations, conclusion

### Rehearsal tips

- Keep transitions short between speakers.
- Do not reread every bullet on the slide.
- Use the slide as visual support and let the script carry the story.
- The timing is intentionally rebalanced so Speakers 3 and 4 have more room.

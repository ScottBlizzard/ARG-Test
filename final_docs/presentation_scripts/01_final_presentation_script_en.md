# Final Presentation Script (English)

This script is based on the current final deck:

- `07_PPT_Assets_For_Luowu/final_ppt.pdf`

Recommended total length:

- about `15` minutes
- `5` speakers
- about `3` minutes per speaker

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

**Target time:** about `3 minutes`

Good morning everyone. We are Group 7, and our project is called ARG-Test, an auditable and risk-aware requirement-driven black-box test generation pipeline.

Our starting point was the final-project requirement itself. The assignment did not ask us to build only a prompt or only a benchmark. It asked us to build an AI-driven AutoTestDesign tool, and then use that tool to test an independent target application.

So in our final version, we clearly separate three things. First, ARG-Test is the tool. Second, MiniShop Checkout is the independent application under test. Third, coupon_discount_engine is the selected major module inside MiniShop Checkout that we use for detailed test design and execution.

This separation is important because it corrects the biggest issue in our earlier understanding. We are not testing our tool as if it were the target application. Instead, we use the tool to test a concrete checkout application.

MiniShop Checkout is a compact e-commerce checkout prototype built specifically for this final project. Its implemented scope includes promotion and coupon handling, shipping-fee calculation, tax and order-total calculation, payment-card validation, pickup-contact validation, and checkout preview orchestration. At the same time, we explicitly keep refund workflows, inventory synchronization, and external payment gateway integration out of scope, so that the application stays small but still concrete enough to be a real target.

Once we fixed the application boundary, the next question became: why is plain LLM prompting not enough? The short answer is that fluent output is not the same as auditable testing. A plain LLM may suggest a few reasonable-looking tests, such as trying a valid coupon or an expired coupon, but it often does not tell us whether the important invalid partitions are covered, whether the boundary neighbors are covered, or whether the claimed technique really matches the obligations in the requirement.

That is why the deeper issue is not only correctness. The deeper issue is auditability. We wanted a system that can explain how it got from a natural-language requirement to a structured and reviewable test suite.

So that is the motivation for the rest of the talk: we move from plain answers to structured, checked, and traceable test design.

---

## Speaker 2

**Slides 5 to 7**

**Target time:** about `3 minutes`

I will explain how ARG-Test works as a system.

The key idea is that ARG-Test is a pipeline, not a single prompt. Instead of asking the model to directly output a final list of tests, we organize the workflow into several stages: structured generation, parser and schema gate, technique-aware checking, reranking and targeted repair, and finally export, evaluation, and reproducible reporting.

The structured trace is one of the most important parts. The model is guided to produce a typed trace with five parts: Analysis, Pattern, Steps, Verification, and FinalAnswer. This matters because it turns the output into something that can be parsed and checked instead of something that only sounds good to a human reader.

On top of that, we apply technique-aware contract checking. In our system, this includes an equivalence partition checker, a boundary value checker, a decision checker, and a state checker. These checkers do not magically prove semantic correctness, but they do verify whether the generated trace and test suite actually contain the expected obligations implied by the chosen testing techniques.

So the model output is no longer treated as a final truth. It becomes a typed artifact that can be parsed, checked, compared, reranked, and, when necessary, repaired.

The next slide shows how this connects to the course requirements. In terms of mandatory closure, our final version covers FR 1.0, FR 1.1, FR 2.0, FR 3.0, and FR 6.0. In addition, we also closed the extra-credit parts FR 4.0, FR 5.0, and FR 7.0.

Another important requirement from the teacher is interactive review. Our final system provides four practical review surfaces: Direct Input, CSV Batch, State Model, and Formal Evidence.

Most importantly, the tester is not passive. The tester can inspect outputs, revise inputs or review guidance, rerun the pipeline, and in the final version even edit generated test cases and export a revised suite. This is how we make designer participation real, instead of only claiming that review is possible in theory.

So at this point, our main message is that ARG-Test is not just generation. It is generation plus structure, checking, review, and controlled revision.

---

## Speaker 3

**Slides 8 to 10**

**Target time:** about `3 minutes`

I will focus on the application-facing planning artifacts: the risk analysis and the test plan.

Because our target application is MiniShop Checkout, the risk analysis must also target MiniShop Checkout. We score risks using a simple but explicit formula: Risk Priority equals Impact times Likelihood times Detectability. We then divide the results into high, medium, and low priority bands.

From this analysis, the highest-risk areas in MiniShop Checkout are coupon and promotion logic, shipping and tax calculation, payment-card validation, and checkout orchestration. Pickup validation is still important, but compared with pricing, totals, and payment acceptance, its overall impact is somewhat narrower.

This prioritization directly shapes the test plan. The scope of the plan includes promotion and pricing, shipping and tax, payment validation, pickup validation, and checkout orchestration. Architecturally, the application is organized around a Checkout Service that coordinates Promotion, Shipping, Tax, Payment Validation, and Pickup Validation.

On top of this architecture, we designed a set of planned suites: a promotion suite, a shipping and tax suite, a payment validation suite, a pickup validation suite, a checkout orchestration suite, and finally a detailed executable module suite focused on coupon_discount_engine.

The next planning dimension is execution organization. Our schedule is straightforward: first freeze the target-application scope, then complete the risk analysis, then review generated suites, then execute the detailed module tests, and finally package the evidence and the final deliverables.

For execution, we chose pytest together with coverage.py. The reason is simple. MiniShop Checkout is implemented in Python, and pytest is a clean fit for both black-box and white-box assertions. It also integrates naturally with coverage collection, which is especially useful for the selected detailed module.

Finally, we also included cost estimation, because the assignment explicitly asks for it. Our estimate is that testing this target application with ARG-Test takes about four and a half to seven person-days, while a manual baseline without the tool would likely require around seven and a half to ten person-days. So the main gain is not that the tool removes human review, but that it reduces the cost of requirement decomposition, first-pass suite generation, prioritization, and traceability maintenance.

So these two documents, the risk report and the test plan, now consistently describe how we test the target application, not the tool itself.

---

## Speaker 4

**Slides 11 to 16**

**Target time:** about `3 minutes`

I will now present the experimental setup and the main tool-level results.

Our evaluation uses a frozen test split with sixteen requirements. The purpose of freezing the test set is to make the final comparison stable and defensible. We compare ARG-Test against three baselines: a rule-based baseline, a plain LLM baseline, and a structured-no-checker baseline.

The main result scorecard shows that on these sixteen frozen test requirements, ARG-Test reaches an average checker score of 0.959, an average overall coverage of 0.615, and zero duplicate cases.

Why does that matter? Because it shows that the full pipeline is stronger than all three weaker alternatives. Against the rule-based baseline, the gain shows better requirement understanding. Against plain LLM, the gain shows that prompting alone is not enough. And against structured no-checker, the gain shows that checker-guided control adds real value rather than just making the output look more organized.

We also looked at generalization and ablation. The method generalizes across business-rule requirements, input-validation requirements, and workflow-state requirements. And in the ablation view, the most honest interpretation is that checker-guided control greatly improves checker alignment while keeping coverage broadly comparable. In other words, the checker layer is not decorative. It changes the quality of the final selected suite.

The representative cases page gives three concrete examples of what the system handles: business-rule logic, input validation, and workflow-oriented cases. This is important because it shows that our method is not overfitted to only one kind of requirement.

At this point, the main takeaway is that the tool-level evidence supports two claims. First, ARG-Test runs on a meaningful range of requirement types. Second, the structured and checked pipeline is materially better than weaker baselines on the frozen evaluation setting.

This prepares the transition to the last part of the talk, where we move from design-level evidence to executable evidence.

---

## Speaker 5

**Slides 17 to 20**

**Target time:** about `3 minutes`

I will conclude with the strongest execution evidence, as well as the final boundaries of the project.

Inside MiniShop Checkout, we selected coupon_discount_engine as the major module for detailed test design and execution. We chose it because it is a high-risk financial-rule component with thresholds, invalid cases, rule combinations, and clear expected results. So it is a good place to prove that our requirement-driven design can become real executable tests.

This gives us more than design-level metrics. It gives us executable evidence. In the final version, the selected module is supported by black-box tests, white-box tests, full statement coverage, full branch coverage, and mutation-based usefulness evidence. At the repository level, our current regression suite also passes consistently.

We also paid close attention to reproducibility and practical validation. Under seeded mock control, the repository-level chain is deterministic. For live providers, we remain honest: variance still exists. That is why our submission-level reproducibility does not rely on overclaiming live determinism. Instead, we use frozen generations plus replay to guarantee that the formal examples shown in the demo and report can be reconstructed.

The limitations page is also important. We stay inside the requirement-driven branch. Our evaluation is course-scale rather than a large public benchmark. Coverage still depends on manually authored gold specifications. And live providers still show residual nondeterminism. We do not treat these as hidden weaknesses. We treat them as honest project boundaries.

So to conclude, our main message is this. Structured reasoning makes black-box test design auditable. The full ARG-Test pipeline beats both non-AI and weaker AI baselines. And the final submission is not just a demo of prompts. It includes the tool itself, an application-facing risk report, a target-application test plan, a detailed execution document for a selected module, and reproducible final artifacts.

Thank you. We are ready for questions.

---

## Short Handoff Notes

### Recommended speaking order

1. Speaker 1: title, scope separation, target application, motivation
2. Speaker 2: architecture, structured trace, checker, interactive review
3. Speaker 3: risk report and test plan
4. Speaker 4: experiments and benchmark results
5. Speaker 5: executable evidence, reproducibility, limitations, conclusion

### Rehearsal tips

- Keep transitions short between speakers.
- Do not reread every bullet on the slide.
- Use the slide as visual support and let the script carry the story.
- If time is short, compress Speaker 4 slightly, especially on Slides `11` and `12`.

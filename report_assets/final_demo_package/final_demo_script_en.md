# Final Demo Script

## Demo length

Recommended total length: `4 to 5 minutes`

## 0:00 - 0:20 Opening

Hello. This short demo shows the final-project tool itself rather than the full presentation deck.

We will use a stable mock run for live interaction, and then connect it to our frozen formal results and executable evidence. This way, the recording shows the real workflow without depending on a live API call.

## 0:20 - 1:10 Live command execution

First, we demonstrate direct text input. The tool accepts a requirement from standard input and produces a structured testing result together with risk and state-model metadata.

Second, we demonstrate CSV batch input. This shows that the system can ingest multiple requirements from a structured spreadsheet-like source and export separate artifacts for each one.

Third, we demonstrate state-model extraction on a workflow requirement. This is the final-project feature that closes the white-box modeling requirement at the system-behavior level.

At this stage, the point is not final benchmark quality yet. The point is to show that the tool really runs, accepts multiple input modes, and produces structured outputs automatically.

## 1:10 - 1:50 Inspect direct-text output

Now we open the direct-text summary.

Here we can see that the output is not just a free-form answer. It includes the selected candidate profile, a checker score, a risk assessment, and an explicit state model with legal transitions and coverage plans.

This is important because our final system is designed as an auditable testing pipeline rather than a one-shot prompt.

## 1:50 - 2:20 Inspect CSV output

Next, we open one result from the CSV batch run.

The key point here is that the tool exports a normalized test suite in structured formats such as Markdown, JSON, and CSV. This makes the result reusable for documentation and for downstream testing workflows.

## 2:20 - 2:50 Inspect workflow state-model output

Now we open the workflow state-model output.

This file shows extracted states, legal transitions, illegal transitions, and coverage plans such as All States and All Transitions. This is the part that moves the project beyond simple black-box case listing.

## 2:50 - 3:20 Connect to formal benchmark results

The live mock run demonstrates the tool interface, but our final project quality is represented by the frozen formal result bundle.

On the held-out test split, ARG-Test reaches an average checker score of 0.959 and an average overall coverage of 0.615, clearly outperforming the rule-based, plain-LLM, and structured-no-checker baselines.

This figure is the main evidence that our method is effective, not only operational.

## 3:20 - 3:45 Reproducibility note

We also distinguish pipeline-level reproducibility from provider-level nondeterminism.

Our local seeded pipeline is reproducible, and submission-level reproducibility is guaranteed through frozen generations plus replay. This is why we use frozen formal outputs for the final package instead of overclaiming live determinism.

## 3:45 - 4:15 Executable evidence

Finally, we show the detailed module evidence for coupon_discount_engine.

This part demonstrates that the final project is not limited to requirement-level design metrics. We also built executable black-box and white-box tests, achieved 100 percent statement and branch coverage on the selected reference module, and killed 4 out of 4 seeded mutants.

## 4:15 - 4:30 Closing

In summary, the demo shows three things:

the tool runs on multiple input modes,
the outputs are structured and auditable,
and the final project is backed by strong frozen results and executable evidence.

That is the core value of ARG-Test as a final-course project.

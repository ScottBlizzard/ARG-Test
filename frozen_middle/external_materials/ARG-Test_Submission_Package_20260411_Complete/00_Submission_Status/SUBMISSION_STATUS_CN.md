# Submission Status (CN)

## Overall Judgment

Against `Assignment1.md`, the project is already complete on the artifact / implementation / experiment side.
The only remaining work before email submission is:
1. Export the final report to PDF.
2. Export the final presentation to PDF.
3. Use the provided compressed test-scripts package in `03_Test_Scripts/ARG-Test_test_scripts.zip`.

## Requirement Mapping

- AI-based testing technique: completed.
  - The project implements requirement-driven AI black-box testing with structured reasoning, checker validation, reranking, and repair.
- Accepted input form: completed.
  - The assignment allows either `System Requirements` or `Testing Codebase`.
  - This project fully implements the `System Requirements` branch, which is compliant.
- Tool artifact (prompts / model / generated code): completed.
  - Prompts are in `03_Test_Scripts/ARG-Test_test_scripts/prompts/`.
  - Model configuration template is in `03_Test_Scripts/ARG-Test_test_scripts/.env.example`.
  - Source code is in `03_Test_Scripts/ARG-Test_test_scripts/src/` and `03_Test_Scripts/ARG-Test_test_scripts/experiments/`.
- Generated output (test cases): completed.
  - Official final test outputs are in `02_Experiment_Evidence/formal_final_tests_test/`.
- Experimental analysis (accuracy / coverage / generalizability / ablation / stability): completed.
  - Official result summaries are in `02_Experiment_Evidence/formal_reports_test/`.
  - Stability sanity check is in `02_Experiment_Evidence/stability_sanity_summary.json` and `.md`.
- Report / PPT source materials: prepared.
  - Editable materials and figures are in `01_Report_and_Presentation_Source/`.
  - Final PDF export is still required manually.

## Final Frozen Result Snapshot

- Formal main result: avg checker score = 0.959
- Formal main result: avg overall coverage = 0.615
- Remaining weak cases:
  - no case with score < 0.9
  - only one case with coverage < 0.4 (`address_international_format_validation = 0.392`)

## Folder Guide

- `00_Submission_Status/`: this status note
- `01_Report_and_Presentation_Source/`: report/PPT writing assets, figures, editable architecture PPTX
- `02_Experiment_Evidence/`: official experiment outputs and summaries used in the final write-up
- `03_Test_Scripts/`: clean scripts folder plus the compressed file to submit

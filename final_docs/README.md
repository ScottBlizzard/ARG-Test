# Final Docs

This directory is the working area for Final Project documents and planning assets.

Current structure:

- `course_brief/assignment2_final_project.md`: the official final-project assignment brief moved into the repository.
- `00_final_strategy_cn.md`: high-bar project positioning and priorities.
- `01_assignment_gap_map_cn.md`: mapping from assignment requirements to current repo assets and gaps.
- `risk_analysis_report/`: self-contained package for the finalized risk analysis report.
- `test_plan/`: self-contained package for the finalized test plan.
- `detailed_test_design_execution/`: self-contained package for the finalized detailed test design and execution document.
- `05_evidence_and_submission_checklist_cn.md`: evidence-source and submission checklist.
- `06_upgrade_backlog_cn.md`: high-impact upgrade backlog for the final phase.
- `07_final_upgrade_report_cn.md`: complete final-upgrade report with best-version recommendations.
- `08_upgrade_implementation_status_cn.md`: implementation-complete status after the core upgrade landed.
- `09_nfr_validation_report_cn.md`: formalized non-functional validation report.
- `10_feature_closure_status_cn.md`: closure report for the remaining strict-gap features and rerun policy.
- `11_reproducibility_and_stability_cn.md`: seeded reproducibility upgrade status, live evidence, and final reporting guidance.
- `execution_evidence/`: saved execution evidence for the selected detailed module.

Independent document package convention:

- each package keeps its own `.md`, `.pdf`, local `figures/`, and `generate_package.py`
- `experiments/generate_final_doc_figures.py` regenerates figures for all three packages
- `experiments/export_final_docs_pdf.py` regenerates PDFs for all three packages

Suggested next additions:

- final report source
- final PPT source
- presentation outline and demo checklist

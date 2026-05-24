# Final Demo Package

This package is the recording-ready bundle for the final project video demonstration.

Current primary demo path: use the Web UI at `http://127.0.0.1:8000/`. The older terminal scripts are retained as legacy archive/fallback material, not the recommended recording flow.

If you are the teammate responsible for the web demo UI, use:

- `frontend_focus/README.md`

first. It is the simplified frontend-only entry point.

Contents:

- `final_demo_plan_cn.md`: overall demo design and rationale
- `demo_handoff_cn.md`: recorder-facing handoff note
- `final_demo_script_cn.md`: Chinese narration script
- `final_demo_script_en.md`: time-coded English narration script
- `final_demo_recording_checklist_cn.md`: recording checklist and operator notes
- `demo_asset_map_cn.md`: exact files, figures, and output paths to open during recording
- `demo_ui_handoff_cn.md`: frontend/backend scope and stability guide for the demo teammate
- `run_demo_commands.ps1`: legacy one-click terminal script kept for fallback/archive
- `open_demo_assets.ps1`: open the key demo outputs and figures
- `prepare_demo_workspace.ps1`: run the demo and open the assets in one go
- `figures/`: copied figure assets used in the demo

Recommended use:

1. If you are the frontend/demo teammate, start from `frontend_focus/README.md`
2. Read `demo_handoff_cn.md`
3. Read `demo_ui_handoff_cn.md` if you are polishing the web UI
4. Read `final_demo_recording_checklist_cn.md`
5. Start the web backend and record the browser UI
6. Use `prepare_demo_workspace.ps1` only if you need the legacy terminal fallback
7. Follow `final_demo_recording_checklist_cn.md` while recording

Recommended demo style:

- use mock mode for live command execution
- use frozen formal outputs for polished result presentation
- do not rely on a live API call during recording

Web demo baseline:

- backend: `demo_web/app.py`
- frontend: `demo_web/static/`
- launcher: `demo_web/run_demo_ui.ps1`

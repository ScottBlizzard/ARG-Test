from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.export_final_docs_pdf import build_pdf, build_styles
from experiments.generate_final_doc_figures import copy_architecture_figure, ensure_dir


DOC_DIR = Path(__file__).resolve().parent
DOC_PATH = DOC_DIR / "03_test_plan_cn.md"
FIG_PATH = DOC_DIR / "figures" / "arg_test_architecture_final.png"


def main() -> None:
    ensure_dir(FIG_PATH.parent)
    copy_architecture_figure(FIG_PATH)
    print(build_pdf(DOC_PATH, build_styles()))


if __name__ == "__main__":
    main()

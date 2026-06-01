from __future__ import annotations

import re
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FINAL_DOCS = ROOT / "final_docs"
RISK_DIR = FINAL_DOCS / "risk_analysis_report"
TEST_PLAN_DIR = FINAL_DOCS / "test_plan"
DETAIL_DIR = FINAL_DOCS / "detailed_test_design_execution"

PALETTE = {
    "ink": "#132238",
    "muted": "#5B6677",
    "line": "#D8DCE3",
    "paper": "#FBFAF6",
    "white": "#FFFFFF",
    "red": "#D55C3A",
    "gold": "#D8A332",
    "teal": "#3B8C88",
    "purple": "#7C6BB0",
    "blue_soft": "#E8EEF5",
    "gold_soft": "#F5E3B5",
    "teal_soft": "#B9DDD8",
    "red_soft": "#F2C6B8",
}


RISK_ITEMS = [
    ("R1", 5, 4, 3, 60, "FR coverage exposition"),
    ("R2", 5, 5, 4, 100, "metric interpretation"),
    ("R3", 4, 4, 3, 48, "FR4/executable boundary"),
    ("R4", 5, 3, 4, 60, "demo UI interpretation"),
    ("R5", 5, 3, 5, 75, "provider latency wording"),
    ("R6", 4, 3, 3, 36, "traceability drift"),
    ("R7", 4, 3, 4, 48, "result-source policy"),
    ("R8", 3, 2, 2, 12, "ad-hoc mock confusion"),
    ("R9", 2, 3, 4, 24, "secret leakage"),
    ("R10", 3, 2, 5, 30, "maintainability chain"),
]


def configure() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": PALETTE["white"],
            "axes.facecolor": PALETTE["white"],
            "savefig.facecolor": PALETTE["white"],
            "font.family": ["DejaVu Sans", "Microsoft YaHei", "Segoe UI"],
            "font.size": 11.5,
            "axes.edgecolor": PALETTE["line"],
            "axes.labelcolor": PALETTE["ink"],
            "xtick.color": PALETTE["muted"],
            "ytick.color": PALETTE["muted"],
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save_fig(fig: plt.Figure, output_path: Path) -> None:
    fig.savefig(output_path, bbox_inches="tight", pad_inches=0.06)
    fig.savefig(output_path.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.06)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def count_repo_test_functions() -> int:
    pattern = re.compile(r"^\s*def\s+test_", re.MULTILINE)
    total = 0
    for path in (ROOT / "tests").glob("test_*.py"):
        total += len(pattern.findall(path.read_text(encoding="utf-8")))
    return total


def risk_color(priority: int) -> str:
    if priority >= 60:
        return PALETTE["red"]
    if priority >= 36:
        return PALETTE["gold"]
    return PALETTE["teal"]


def save_risk_heatmap(output_path: Path) -> None:
    configure()
    fig = plt.figure(figsize=(9.4, 5.8), dpi=220)
    ax = fig.add_axes([0.08, 0.12, 0.62, 0.78])
    legend_ax = fig.add_axes([0.74, 0.20, 0.22, 0.60])
    legend_ax.set_axis_off()

    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    ax.set_xlabel("Likelihood")
    ax.set_ylabel("Impact")
    ax.set_title("Risk priority map for the final ARG-Test submission", fontsize=15.5, color=PALETTE["ink"], pad=14)
    ax.grid(color=PALETTE["line"], linestyle="--", linewidth=0.8, alpha=0.8)

    display_positions = {
        "R1": (3.95, 4.98),
        "R2": (4.78, 5.02),
        "R3": (4.06, 4.03),
        "R4": (3.18, 4.86),
        "R5": (3.00, 5.00),
        "R6": (3.00, 4.03),
        "R7": (3.18, 3.88),
        "R8": (2.00, 3.00),
        "R9": (3.00, 2.00),
        "R10": (2.18, 3.10),
    }

    for risk_id, impact, likelihood, detectability, priority, label in RISK_ITEMS:
        plot_x, plot_y = display_positions[risk_id]
        ax.scatter(
            plot_x,
            plot_y,
            s=130 + priority * 5,
            color=risk_color(priority),
            alpha=0.88,
            edgecolor=PALETTE["white"],
            linewidth=1.3,
            zorder=3,
        )
        ax.text(
            plot_x + 0.06,
            plot_y + 0.06,
            risk_id,
            fontsize=9.6,
            color=PALETTE["ink"],
            zorder=4,
        )

    legend_specs = [
        ("High priority", "R1, R2, R4, R5", PALETTE["red_soft"], PALETTE["red"], 0.72),
        ("Medium priority", "R3, R6, R7", PALETTE["gold_soft"], PALETTE["gold"], 0.40),
        ("Low priority", "R8, R9, R10", PALETTE["teal_soft"], PALETTE["teal"], 0.08),
    ]
    for title, items, fill, edge, y0 in legend_specs:
        legend_ax.add_patch(
            FancyBboxPatch(
                (0.02, y0),
                0.96,
                0.22,
                boxstyle="round,pad=0.015,rounding_size=0.03",
                facecolor=fill,
                edgecolor=edge,
                linewidth=1.2,
                transform=legend_ax.transAxes,
            )
        )
        legend_ax.text(0.16, y0 + 0.14, title, fontsize=10.2, fontweight="bold", color=PALETTE["ink"], transform=legend_ax.transAxes)
        legend_ax.text(0.16, y0 + 0.06, items, fontsize=9.5, color=PALETTE["muted"], transform=legend_ax.transAxes)

    fig.text(
        0.08,
        0.04,
        "Bubble size reflects computed priority = Impact x Likelihood x Detectability.",
        fontsize=9.6,
        color=PALETTE["muted"],
    )
    save_fig(fig, output_path)
    plt.close(fig)


def save_coupon_scorecard(output_path: Path) -> None:
    repo_test_count = count_repo_test_functions()
    configure()
    fig = plt.figure(figsize=(8.8, 3.7), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    ax.text(0.04, 0.88, "Detailed module execution evidence", fontsize=16.2, fontweight="bold", color=PALETTE["ink"])
    ax.text(
        0.04,
        0.81,
        "coupon_discount_engine combines black-box design, white-box execution, and mutation usefulness evidence.",
        fontsize=10.3,
        color=PALETTE["muted"],
    )

    cards = [
        ("Executable tests", f"15 module tests\n{repo_test_count} repo tests", PALETTE["gold_soft"], PALETTE["gold"]),
        ("Coverage", "100% statement\n100% branch", PALETTE["teal_soft"], PALETTE["teal"]),
        ("Mutation result", "4 / 4 mutants killed", PALETTE["red_soft"], PALETTE["red"]),
    ]
    for idx, (title, value, fill, line) in enumerate(cards):
        x = 0.05 + idx * 0.305
        patch = FancyBboxPatch(
            (x, 0.19),
            0.26,
            0.48,
            boxstyle="round,pad=0.014,rounding_size=0.03",
            facecolor=fill,
            edgecolor=line,
            linewidth=1.5,
        )
        ax.add_patch(patch)
        ax.text(x + 0.02, 0.59, title, fontsize=12.4, fontweight="bold", color=PALETTE["ink"])
        ax.text(x + 0.13, 0.37, value, fontsize=15.6, fontweight="bold", color=PALETTE["ink"], ha="center", va="center")

    ax.text(
        0.05,
        0.08,
        "Evidence sources: tests/test_coupon_discount_engine_blackbox.py, tests/test_coupon_discount_engine_whitebox.py, coverage XML, and coupon_discount_engine_mutation_demo.md.",
        fontsize=9.2,
        color=PALETTE["muted"],
    )
    save_fig(fig, output_path)
    plt.close(fig)


def copy_architecture_figure(output_path: Path) -> None:
    source = ROOT / "report_assets" / "final_latex_report" / "figures" / "arg_test_architecture_final.png"
    if source.exists():
        ensure_dir(output_path.parent)
        shutil.copy2(source, output_path)


def build_all_doc_figures() -> list[Path]:
    risk_fig = RISK_DIR / "figures" / "risk_priority_heatmap.png"
    plan_fig = TEST_PLAN_DIR / "figures" / "arg_test_architecture_final.png"
    detail_fig = DETAIL_DIR / "figures" / "coupon_module_evidence_scorecard.png"

    ensure_dir(risk_fig.parent)
    ensure_dir(plan_fig.parent)
    ensure_dir(detail_fig.parent)

    save_risk_heatmap(risk_fig)
    copy_architecture_figure(plan_fig)
    save_coupon_scorecard(detail_fig)

    return [plan_fig, risk_fig, detail_fig]


def main() -> None:
    print("\n".join(str(path) for path in build_all_doc_figures()))


if __name__ == "__main__":
    main()

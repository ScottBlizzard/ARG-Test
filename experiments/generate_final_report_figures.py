from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]

PALETTE = {
    "ink": "#17261F",
    "muted": "#64736B",
    "line": "#D8DDD5",
    "panel": "#F3F0E8",
    "white": "#FFFFFF",
    "teal": "#0B6B5F",
    "teal_soft": "#D7EDE8",
    "orange": "#D56A32",
    "orange_soft": "#F5D9C8",
    "gold": "#C99A2D",
    "gold_soft": "#F3E4B5",
    "blue": "#476A92",
    "blue_soft": "#DBE7F2",
    "red": "#B64E3B",
    "purple": "#7862A8",
    "purple_soft": "#E5DFF2",
}


def configure() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": PALETTE["white"],
            "axes.facecolor": PALETTE["white"],
            "savefig.facecolor": PALETTE["white"],
            "font.family": ["Times New Roman", "DejaVu Serif"],
            "font.size": 8.5,
            "axes.titlesize": 9.8,
            "axes.titleweight": "bold",
            "axes.labelsize": 7.7,
            "xtick.labelsize": 7.2,
            "ytick.labelsize": 7.2,
            "axes.labelcolor": PALETTE["ink"],
            "xtick.color": PALETTE["muted"],
            "ytick.color": PALETTE["muted"],
            "axes.edgecolor": PALETTE["line"],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def avg(values: list[float]) -> float:
    return round(mean(values), 3) if values else 0.0


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, output: Path) -> None:
    ensure_dir(output.parent)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.04)
    fig.savefig(output.with_suffix(".png"), dpi=320, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def card(ax, x: float, y: float, w: float, h: float, title: str, value: str, note: str, fill: str, edge: str) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            facecolor=fill,
            edgecolor=edge,
            linewidth=1.1,
        )
    )
    ax.text(x + 0.045 * w, y + h - 0.022, title, fontsize=6.4, fontweight="bold", color=PALETTE["muted"], va="top")
    ax.text(x + 0.045 * w, y + 0.43 * h, value, fontsize=11.8, fontweight="bold", color=PALETTE["ink"], va="center")
    ax.text(x + 0.045 * w, y + 0.028, note, fontsize=5.7, color=PALETTE["muted"], va="bottom")


def aggregate(run_main: list[dict], baseline: list[dict], ablation: list[dict]) -> dict:
    return {
        "main": {
            "count": len(run_main),
            "score": avg([float(x["score"]) for x in run_main]),
            "coverage": avg([float(x["metrics"]["overall_coverage"]) for x in run_main]),
            "tests": avg([float(x["metrics"]["test_count"]) for x in run_main]),
            "duplicates": avg([float(x["metrics"]["duplicate_count"]) for x in run_main]),
            "repaired": sum(1 for x in run_main if x.get("repaired")),
            "high_risk": sum(1 for x in run_main if x.get("risk_assessment", {}).get("level") == "High"),
        },
        "baseline": {
            name: {
                "score": avg([float(x["baselines"][name]["checker_score"]) for x in baseline]),
                "coverage": avg([float(x["baselines"][name]["overall_coverage"]) for x in baseline]),
                "tests": avg([float(x["baselines"][name]["test_count"]) for x in baseline]),
            }
            for name in ["rule_based", "plain_llm", "structured_no_checker"]
        },
        "ablation": {
            name: {
                "score": avg([float(x[name]["checker_score"]) for x in ablation]),
                "coverage": avg([float(x[name]["overall_coverage"]) for x in ablation]),
                "tests": avg([float(x[name]["test_count"]) for x in ablation]),
            }
            for name in ["structured_no_checker", "full_pipeline"]
        },
    }


def fig_scorecard(output: Path, stats: dict, categories: list[dict]) -> None:
    configure()
    fig, ax = plt.subplots(figsize=(3.35, 2.35))
    ax.set_axis_off()
    ax.text(0.02, 0.965, "Frozen Test Split Summary", fontsize=10.2, fontweight="bold", color=PALETTE["ink"], va="top")
    ax.text(0.02, 0.902, "16 held-out requirements; formal replay snapshot", fontsize=7.2, color=PALETTE["muted"], va="top")

    cards = [
        ("Checker", f"{stats['main']['score']:.3f}", "contract consistency", PALETTE["orange_soft"], PALETTE["orange"]),
        ("Coverage", f"{stats['main']['coverage']:.3f}", "gold obligations", PALETTE["teal_soft"], PALETTE["teal"]),
        ("Avg tests", f"{stats['main']['tests']:.3f}", "per requirement", PALETTE["gold_soft"], PALETTE["gold"]),
        ("Duplicates", f"{stats['main']['duplicates']:.1f}", "after cleanup", PALETTE["blue_soft"], PALETTE["blue"]),
        ("High risk", f"{stats['main']['high_risk']}/16", "prioritized", PALETTE["purple_soft"], PALETTE["purple"]),
        ("Repaired", f"{stats['main']['repaired']}/16", "selective repair", PALETTE["panel"], PALETTE["line"]),
    ]
    for (x, y), c in zip([(0.02, 0.60), (0.35, 0.60), (0.68, 0.60), (0.02, 0.32), (0.35, 0.32), (0.68, 0.32)], cards):
        card(ax, x, y, 0.29, 0.23, *c)

    ax.text(0.02, 0.220, "Coverage by category", fontsize=8.2, fontweight="bold", color=PALETTE["ink"])
    label_map = {"business_rules": "Business", "input_validation": "Input", "workflow_state": "Workflow"}
    colors = [PALETTE["orange"], PALETTE["gold"], PALETTE["teal"]]
    for i, (item, color) in enumerate(zip(categories, colors)):
        y = 0.150 - i * 0.052
        ax.text(0.02, y + 0.014, label_map[item["category"]], fontsize=7.0, color=PALETTE["ink"], va="center")
        ax.add_patch(
            FancyBboxPatch((0.24, y), 0.52, 0.023, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["panel"], edgecolor="none")
        )
        ax.add_patch(
            FancyBboxPatch(
                (0.24, y),
                0.52 * float(item["avg_overall_coverage"]),
                0.023,
                boxstyle="round,pad=0.001,rounding_size=0.008",
                facecolor=color,
                edgecolor="none",
            )
        )
        ax.text(0.82, y + 0.014, f"{item['avg_overall_coverage']:.3f}", fontsize=6.8, color=PALETTE["muted"], va="center", ha="right")
    save(fig, output)


def fig_baselines(output: Path, stats: dict) -> None:
    configure()
    rows = [
        ("ARG-Test", stats["main"]["coverage"], stats["main"]["score"], PALETTE["teal"]),
        ("Structured", stats["baseline"]["structured_no_checker"]["coverage"], stats["baseline"]["structured_no_checker"]["score"], PALETTE["gold"]),
        ("Rule-based", stats["baseline"]["rule_based"]["coverage"], stats["baseline"]["rule_based"]["score"], PALETTE["orange"]),
        ("Plain LLM", stats["baseline"]["plain_llm"]["coverage"], stats["baseline"]["plain_llm"]["score"], PALETTE["purple"]),
    ]
    fig, ax = plt.subplots(figsize=(3.35, 2.45))
    y = list(range(len(rows)))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.5, len(rows) - 0.5)
    ax.grid(axis="x", color=PALETTE["line"], linestyle="--", linewidth=0.55, alpha=0.8)
    for i, (name, coverage, score, color) in enumerate(rows):
        ax.barh(i, coverage, height=0.40, color=color, edgecolor="none", alpha=0.94)
        ax.plot(score, i, "o", color=PALETTE["ink"], markersize=4.8, zorder=4)
        ax.text(min(coverage + 0.025, 0.86), i, f"{coverage:.3f}", fontsize=7.1, color=PALETTE["ink"], va="center")
        ax.text(min(score + 0.025, 0.93), i - 0.22, f"score {score:.3f}", fontsize=6.2, color=PALETTE["muted"], va="center")
    ax.set_yticks(y, [r[0] for r in rows])
    ax.set_xlabel("Average overall coverage; dot = checker score")
    ax.set_title("Full Pipeline vs. Baselines", loc="left", pad=4)
    ax.invert_yaxis()
    fig.tight_layout(pad=0.45)
    save(fig, output)


def fig_generalization(output: Path, categories: list[dict]) -> None:
    configure()
    labels = ["Business", "Input", "Workflow"]
    coverage = [float(c["avg_overall_coverage"]) for c in categories]
    scores = [float(c["avg_checker_score"]) for c in categories]
    counts = [int(c["requirement_count"]) for c in categories]
    risks = [float(c["avg_risk_score"]) for c in categories]
    colors = [PALETTE["orange"], PALETTE["gold"], PALETTE["teal"]]

    fig, ax = plt.subplots(figsize=(3.35, 2.35))
    bars = ax.bar(range(3), coverage, color=colors, width=0.55, edgecolor="none", alpha=0.94)
    ax.plot(range(3), scores, color=PALETTE["ink"], marker="o", linewidth=1.35, markersize=4.7)
    ax.set_ylim(0, 1.04)
    ax.set_xticks(range(3), labels)
    ax.set_ylabel("Metric value")
    ax.grid(axis="y", color=PALETTE["line"], linestyle="--", linewidth=0.55, alpha=0.8)
    ax.set_title("Generalization by Requirement Category", loc="left", pad=4)
    for bar, cov, score, n, risk in zip(bars, coverage, scores, counts, risks):
        cx = bar.get_x() + bar.get_width() / 2
        ax.text(cx, cov + 0.025, f"{cov:.3f}", ha="center", fontsize=7.0, color=PALETTE["ink"])
        ax.text(cx, 0.055, f"n={n}\nrisk {risk:.1f}", ha="center", va="bottom", fontsize=6.0, color=PALETTE["muted"])
        ax.text(cx + 0.08, min(score + 0.035, 1.0), f"{score:.3f}", ha="left", fontsize=6.2, color=PALETTE["muted"])
    fig.tight_layout(pad=0.45)
    save(fig, output)


def fig_ablation(output: Path, stats: dict) -> None:
    configure()
    old = stats["ablation"]["structured_no_checker"]
    new = stats["ablation"]["full_pipeline"]
    metrics = [
        ("Checker score", old["score"], new["score"], PALETTE["orange"], 1.0),
        ("Coverage", old["coverage"], new["coverage"], PALETTE["teal"], 1.0),
        ("Test count", old["tests"], new["tests"], PALETTE["gold"], 8.0),
    ]

    fig, ax = plt.subplots(figsize=(3.35, 2.15))
    ax.set_axis_off()
    ax.text(0.02, 0.94, "Checker-Guided Control Ablation", fontsize=9.4, fontweight="bold", color=PALETTE["ink"], va="top")
    ax.text(0.02, 0.87, "Gray = structured only; color = full pipeline", fontsize=7.0, color=PALETTE["muted"], va="top")
    for i, (label, before, after, color, scale) in enumerate(metrics):
        y = 0.67 - i * 0.22
        ax.text(0.02, y + 0.045, label, fontsize=7.6, fontweight="bold", color=PALETTE["ink"], va="center")
        ax.add_patch(FancyBboxPatch((0.36, y), 0.40, 0.032, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["panel"], edgecolor="none"))
        ax.add_patch(FancyBboxPatch((0.36, y), 0.40 * before / scale, 0.032, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["line"], edgecolor="none"))
        ax.add_patch(FancyBboxPatch((0.36, y + 0.052), 0.40, 0.032, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["panel"], edgecolor="none"))
        ax.add_patch(FancyBboxPatch((0.36, y + 0.052), 0.40 * after / scale, 0.032, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=color, edgecolor="none"))
        ax.text(0.80, y + 0.016, f"{before:.3f}", fontsize=6.3, color=PALETTE["muted"], va="center")
        ax.text(0.80, y + 0.068, f"{after:.3f}", fontsize=6.8, fontweight="bold", color=PALETTE["ink"], va="center")
        ax.text(0.96, y + 0.112, f"gain {after - before:+.3f}", fontsize=5.8, color=color, va="center", ha="right")
    save(fig, output)


def fig_repro(output: Path, summaries: list[dict]) -> None:
    configure()
    fig, ax = plt.subplots(figsize=(6.9, 2.75))
    ax.set_axis_off()
    ax.text(0.02, 0.96, "Reproducibility Evidence", fontsize=11.0, fontweight="bold", color=PALETTE["ink"], va="top")
    ax.text(0.02, 0.89, "Local mock runs are stable; live-provider variance is disclosed and contained by replay.", fontsize=7.6, color=PALETTE["muted"], va="top")

    rows = [
        ("Mock 3-seed", summaries[0], PALETTE["teal"], "local deterministic chain"),
        ("Live multi-seed", summaries[1], PALETTE["gold"], "usable, not deterministic"),
        ("Live same-seed", summaries[2], PALETTE["orange"], "provider variance remains"),
    ]
    for i, (name, item, color, note) in enumerate(rows):
        x = 0.03 + i * 0.32
        ax.add_patch(FancyBboxPatch((x, 0.62), 0.29, 0.18, boxstyle="round,pad=0.012,rounding_size=0.022", facecolor=PALETTE["white"], edgecolor=color, linewidth=1.1))
        rate = item["stable_case_count"] / item["requirement_count"] if item["requirement_count"] else 0.0
        ax.text(x + 0.018, 0.75, name, fontsize=8.7, fontweight="bold", color=PALETTE["ink"])
        ax.text(x + 0.018, 0.70, f"{item['stable_case_count']}/{item['requirement_count']} stable ({rate:.0%})", fontsize=7.6, fontweight="bold", color=color)
        ax.text(x + 0.018, 0.655, note, fontsize=6.4, color=PALETTE["muted"])

    ax.text(0.04, 0.50, "Stable-case ratio", fontsize=8.6, fontweight="bold", color=PALETTE["ink"])
    ax.text(0.55, 0.50, "Average max drift", fontsize=8.6, fontweight="bold", color=PALETTE["ink"])
    for i, (name, item, color, _) in enumerate(rows):
        y = 0.39 - i * 0.105
        rate = item["stable_case_count"] / item["requirement_count"] if item["requirement_count"] else 0.0
        ax.text(0.04, y + 0.018, name, fontsize=7.0, color=PALETTE["ink"], va="center")
        ax.add_patch(FancyBboxPatch((0.22, y), 0.25, 0.030, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["panel"], edgecolor="none"))
        ax.add_patch(FancyBboxPatch((0.22, y), 0.25 * rate, 0.030, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=color, edgecolor="none"))
        ax.text(0.49, y + 0.017, f"{rate:.0%}", fontsize=6.8, color=PALETTE["muted"], va="center", ha="right")
        sd = float(item["avg_max_score_delta"])
        cd = float(item["avg_max_coverage_delta"])
        ax.text(0.55, y + 0.018, f"score {sd:.2f}", fontsize=7.0, color=PALETTE["ink"], va="center")
        ax.add_patch(FancyBboxPatch((0.68, y), 0.10, 0.030, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["panel"], edgecolor="none"))
        ax.add_patch(FancyBboxPatch((0.68, y), 0.10 * min(sd / 0.25, 1.0), 0.030, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["purple"], edgecolor="none"))
        ax.text(0.81, y + 0.018, f"cov {cd:.2f}", fontsize=7.0, color=PALETTE["ink"], va="center")
        ax.add_patch(FancyBboxPatch((0.91, y), 0.07, 0.030, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=PALETTE["panel"], edgecolor="none"))
        ax.add_patch(FancyBboxPatch((0.91, y), 0.07 * min(cd / 0.25, 1.0), 0.030, boxstyle="round,pad=0.001,rounding_size=0.008", facecolor=color, edgecolor="none"))
    save(fig, output)


def pretty_name(requirement_id: str) -> str:
    return requirement_id.replace("_", " ").title()


def fig_cases(output: Path, run_main: list[dict]) -> None:
    configure()
    by_id = {x["requirement_id"]: x for x in run_main}
    selected = [
        ("coupon_discount_engine", "Business rule", "Coupon Discount\nEngine", PALETTE["orange"]),
        ("payment_card_expiry_and_cvv_validation", "Input validation", "Card Expiry +\nCVV Validation", PALETTE["gold"]),
        ("payment_3ds_authentication_flow", "Workflow state", "3DS Authentication\nFlow", PALETTE["teal"]),
    ]
    fig, ax = plt.subplots(figsize=(6.9, 2.55))
    ax.set_axis_off()
    for i, (rid, title, display_name, color) in enumerate(selected):
        item = by_id[rid]
        x = 0.025 + i * 0.325
        ax.add_patch(FancyBboxPatch((x, 0.10), 0.295, 0.78, boxstyle="round,pad=0.014,rounding_size=0.026", facecolor=PALETTE["white"], edgecolor=PALETTE["line"], linewidth=1.0))
        ax.add_patch(FancyBboxPatch((x, 0.74), 0.295, 0.14, boxstyle="round,pad=0.014,rounding_size=0.026", facecolor=color, edgecolor=color, linewidth=0))
        ax.text(x + 0.018, 0.805, title, fontsize=8.7, fontweight="bold", color=PALETTE["white"], va="center")
        ax.text(x + 0.018, 0.665, display_name, fontsize=8.0, fontweight="bold", color=PALETTE["ink"], va="top")
        metrics = [
            ("score", f"{float(item['score']):.3f}"),
            ("coverage", f"{float(item['metrics']['overall_coverage']):.3f}"),
            ("tests", f"{int(item['metrics']['test_count'])}"),
            ("risk", f"{float(item.get('risk_assessment', {}).get('score', 0.0)):.2f}"),
        ]
        for j, (label, value) in enumerate(metrics):
            y = 0.47 - j * 0.082
            ax.text(x + 0.025, y, label, fontsize=7.0, color=PALETTE["muted"], va="center")
            ax.text(x + 0.260, y, value, fontsize=8.5, fontweight="bold", color=PALETTE["ink"], va="center", ha="right")
        ax.text(x + 0.025, 0.135, f"{item.get('risk_assessment', {}).get('level', 'n/a')} risk formal output", fontsize=6.3, color=PALETTE["muted"])
    save(fig, output)


def build_all(out_dir: Path) -> None:
    report_root = ROOT / ".local_runs" / "formal_qwen_novpn" / "outputs" / "reports" / "test"
    run_main = read_json(report_root / "run_main_summary.json")
    baseline = read_json(report_root / "baseline_summary.json")
    ablation = read_json(report_root / "ablation_summary.json")
    categories = read_json(report_root / "generalization_by_category.json")["categories"]
    stats = aggregate(run_main, baseline, ablation)

    repro_roots = [
        ROOT / ".local_runs" / "repro_multi_seed_mock" / "outputs" / "reports" / "test" / "repeatability_summary.json",
        ROOT / ".local_runs" / "repro_live_qwen_5case" / "outputs" / "reports" / "test" / "repeatability_summary.json",
        ROOT / ".local_runs" / "repro_live_same_seed_3case" / "outputs" / "reports" / "test" / "repeatability_summary.json",
    ]
    repro = [read_json(p) for p in repro_roots]

    fig_scorecard(out_dir / "final_result_scorecard.pdf", stats, categories)
    fig_baselines(out_dir / "main_vs_baselines.pdf", stats)
    fig_generalization(out_dir / "generalization_by_category.pdf", categories)
    fig_ablation(out_dir / "ablation_gain.pdf", stats)
    fig_cases(out_dir / "case_study_snapshots.pdf", run_main)
    fig_repro(out_dir / "reproducibility_stability_overview.pdf", repro)


def main() -> None:
    targets = [
        ROOT / "report_assets" / "final_latex_report" / "figures",
        ROOT / "report_assets" / "figures",
    ]
    for target in targets:
        build_all(target)
    print(json.dumps({"updated_dirs": [str(t) for t in targets]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

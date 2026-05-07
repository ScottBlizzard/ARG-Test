from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]

PALETTE = {
    'ink': '#132238',
    'muted': '#5B6677',
    'paper': '#FBFAF6',
    'panel': '#F7F5EF',
    'panel_alt': '#EEF3F7',
    'accent': '#D55C3A',
    'accent_soft': '#F2C6B8',
    'teal': '#3B8C88',
    'teal_soft': '#B9DDD8',
    'gold': '#D8A332',
    'gold_soft': '#F5E3B5',
    'line': '#D8DCE3',
    'purple': '#7C6BB0',
    'purple_soft': '#E2DAF3',
    'white': '#FFFFFF',
}


def hex_rgb(value: str) -> RGBColor:
    value = value.lstrip('#')
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def avg(values: list[float]) -> float:
    return round(sum(values) / len(values), 3) if values else 0.0


def configure_matplotlib() -> None:
    plt.rcParams.update({
        'figure.facecolor': PALETTE['paper'],
        'axes.facecolor': PALETTE['paper'],
        'savefig.facecolor': PALETTE['paper'],
        'font.family': ['DejaVu Sans', 'Microsoft YaHei', 'Segoe UI'],
        'axes.titleweight': 'bold',
        'axes.labelcolor': PALETTE['ink'],
        'xtick.color': PALETTE['muted'],
        'ytick.color': PALETTE['muted'],
        'axes.edgecolor': PALETTE['line'],
    })


def save_fig(fig, output_path: Path) -> None:
    fig.savefig(output_path, bbox_inches='tight')
    if output_path.suffix.lower() != '.pdf':
        fig.savefig(output_path.with_suffix('.pdf'), bbox_inches='tight')


def aggregate_payload(run_main: list[dict], baseline: list[dict], ablation: list[dict]) -> dict:
    payload = {
        'main': {
            'avg_checker_score': avg([float(item['score']) for item in run_main]),
            'avg_overall_coverage': avg([float(item['metrics']['overall_coverage']) for item in run_main]),
            'avg_test_count': avg([float(item['metrics']['test_count']) for item in run_main]),
            'count': len(run_main),
        },
        'baseline': {},
        'ablation': {},
    }
    for method in ('rule_based', 'plain_llm', 'structured_no_checker'):
        payload['baseline'][method] = {
            'avg_checker_score': avg([float(item['baselines'][method]['checker_score']) for item in baseline]),
            'avg_overall_coverage': avg([float(item['baselines'][method]['overall_coverage']) for item in baseline]),
            'avg_test_count': avg([float(item['baselines'][method]['test_count']) for item in baseline]),
        }
    for method in ('structured_no_checker', 'full_pipeline'):
        payload['ablation'][method] = {
            'avg_checker_score': avg([float(item[method]['checker_score']) for item in ablation]),
            'avg_overall_coverage': avg([float(item[method]['overall_coverage']) for item in ablation]),
            'avg_test_count': avg([float(item[method]['test_count']) for item in ablation]),
        }
    return payload


def add_box(slide, left, top, width, height, fill, line, title, body_lines, title_size=18, body_size=11):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_rgb(fill)
    shape.line.color.rgb = hex_rgb(line)
    shape.line.width = Pt(1.4)
    text_frame = shape.text_frame
    text_frame.clear()
    text_frame.margin_left = Pt(12)
    text_frame.margin_right = Pt(12)
    text_frame.margin_top = Pt(10)
    text_frame.margin_bottom = Pt(10)
    text_frame.vertical_anchor = MSO_ANCHOR.TOP

    p = text_frame.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(title_size)
    p.font.color.rgb = hex_rgb(PALETTE['ink'])
    p.alignment = PP_ALIGN.LEFT
    for line_text in body_lines:
        p = text_frame.add_paragraph()
        p.text = line_text
        p.level = 0
        p.font.size = Pt(body_size)
        p.font.color.rgb = hex_rgb(PALETTE['muted'])
        p.alignment = PP_ALIGN.LEFT
    return shape


def add_label(slide, left, top, width, height, text_value, fill, font_size=11):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_rgb(fill)
    shape.fill.transparency = 0.1
    shape.line.color.rgb = hex_rgb(fill)
    shape.line.width = Pt(0.8)
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text_value
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = hex_rgb(PALETTE['ink'])
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return shape


def connect(slide, x1, y1, x2, y2, color=PALETTE['muted']):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    line.line.color.rgb = hex_rgb(color)
    line.line.width = Pt(2.2)
    return line


def build_architecture_pptx(output_path: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = hex_rgb(PALETTE['paper'])

    title = slide.shapes.add_textbox(Inches(0.65), Inches(0.35), Inches(8.8), Inches(0.55))
    tf = title.text_frame
    p = tf.paragraphs[0]
    p.text = 'ARG-Test Architecture'
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = hex_rgb(PALETTE['ink'])

    sub = slide.shapes.add_textbox(Inches(0.67), Inches(0.78), Inches(9.5), Inches(0.4))
    sp = sub.text_frame.paragraphs[0]
    sp.text = 'Requirement-driven black-box test generation with structured reasoning, checker validation, reranking, and repair.'
    sp.font.size = Pt(12.5)
    sp.font.color.rgb = hex_rgb(PALETTE['muted'])

    add_label(slide, Inches(0.72), Inches(1.15), Inches(1.65), Inches(0.34), 'Model: Qwen3.5-Flash', PALETTE['accent_soft'])
    add_label(slide, Inches(2.5), Inches(1.15), Inches(1.2), Inches(0.34), 'Candidates: 3', PALETTE['teal_soft'])
    add_label(slide, Inches(3.82), Inches(1.15), Inches(1.8), Inches(0.34), 'Output: JSON / CSV / MD', PALETTE['gold_soft'])

    top_y = Inches(1.7)
    h = Inches(1.15)
    box1 = add_box(slide, Inches(0.75), top_y, Inches(2.05), h, PALETTE['gold_soft'], PALETTE['gold'], 'Requirement Dataset', ['dev/test requirements', 'gold specs + manifest'])
    box2 = add_box(slide, Inches(3.15), top_y, Inches(2.25), h, PALETTE['panel_alt'], PALETTE['teal'], 'Prompt Composer', ['system prompt + task prompt', 'provider = openai-compatible'])
    box3 = add_box(slide, Inches(5.85), top_y, Inches(2.2), h, PALETTE['accent_soft'], PALETTE['accent'], 'Structured Trace', ['analysis / pattern / steps', 'verification / final answer'])
    box4 = add_box(slide, Inches(8.45), top_y, Inches(2.55), h, PALETTE['teal_soft'], PALETTE['teal'], 'Parser + Schema Gate', ['typed trace parsing', 'suite export preparation'])

    mid_y = Inches(3.6)
    box5 = add_box(slide, Inches(1.0), mid_y, Inches(2.15), Inches(1.25), PALETTE['gold_soft'], PALETTE['gold'], 'EP / BVA Contract', ['partitions, invalid inputs,', 'boundaries and edge cases'])
    box6 = add_box(slide, Inches(3.65), mid_y, Inches(2.25), Inches(1.25), PALETTE['panel_alt'], PALETTE['teal'], 'Decision Contract', ['rule combinations, priorities,', 'conflicts and exceptions'])
    box7 = add_box(slide, Inches(6.35), mid_y, Inches(2.25), Inches(1.25), PALETTE['accent_soft'], PALETTE['accent'], 'State Contract', ['states, transitions, retries,', 'exceptional paths'])
    box8 = add_box(slide, Inches(9.0), mid_y, Inches(2.35), Inches(1.25), PALETTE['purple_soft'], PALETTE['purple'], 'Rerank + Repair', ['aggregate checker score,', 'local repair, best candidate'])

    bot_y = Inches(5.85)
    box9 = add_box(slide, Inches(2.55), bot_y, Inches(3.2), Inches(1.08), PALETTE['teal_soft'], PALETTE['teal'], 'Final Test Suite', ['JSON + CSV + markdown test cases', 'chosen candidate after checker validation'], title_size=20)
    box10 = add_box(slide, Inches(6.2), bot_y, Inches(4.0), Inches(1.08), PALETTE['accent_soft'], PALETTE['accent'], 'Evaluation and Reports', ['run_main / baselines / ablation / generalization', 'coverage, checker score, category breakdown'], title_size=20)

    connect(slide, box1.left + box1.width, box1.top + box1.height / 2, box2.left, box2.top + box2.height / 2)
    connect(slide, box2.left + box2.width, box2.top + box2.height / 2, box3.left, box3.top + box3.height / 2)
    connect(slide, box3.left + box3.width, box3.top + box3.height / 2, box4.left, box4.top + box4.height / 2)
    connect(slide, box4.left + box4.width / 2, box4.top + box4.height, box8.left + box8.width / 2, box8.top)
    connect(slide, box5.left + box5.width, box5.top + box5.height / 2, box6.left, box6.top + box6.height / 2)
    connect(slide, box6.left + box6.width, box6.top + box6.height / 2, box7.left, box7.top + box7.height / 2)
    connect(slide, box7.left + box7.width, box7.top + box7.height / 2, box8.left, box8.top + box8.height / 2)
    connect(slide, box8.left + box8.width / 2, box8.top + box8.height, box10.left + Inches(1.0), box10.top)
    connect(slide, box8.left + Inches(0.4), box8.top + box8.height, box9.left + Inches(0.9), box9.top)

    prs.save(output_path)



def save_main_vs_baselines(output_path: Path, payload: dict) -> None:
    configure_matplotlib()
    methods = ['Rule-based', 'Plain LLM', 'Structured No Checker', 'ARG-Test Full Pipeline']
    coverage = [
        payload['baseline']['rule_based']['avg_overall_coverage'],
        payload['baseline']['plain_llm']['avg_overall_coverage'],
        payload['baseline']['structured_no_checker']['avg_overall_coverage'],
        payload['main']['avg_overall_coverage'],
    ]
    scores = [
        payload['baseline']['rule_based']['avg_checker_score'],
        payload['baseline']['plain_llm']['avg_checker_score'],
        payload['baseline']['structured_no_checker']['avg_checker_score'],
        payload['main']['avg_checker_score'],
    ]
    colors = [PALETTE['gold'], PALETTE['accent'], PALETTE['teal'], PALETTE['purple']]
    fig, ax = plt.subplots(figsize=(11.0, 5.8), dpi=180)
    ax.barh(methods, coverage, color=colors, edgecolor='none', height=0.58)
    ax.set_xlim(0, 0.75)
    ax.set_xlabel('Average Overall Coverage')
    ax.grid(axis='x', color=PALETTE['line'], linestyle='--', alpha=0.7)
    ax.spines[['top', 'right']].set_visible(False)
    for idx, (cov, score) in enumerate(zip(coverage, scores)):
        ax.text(cov + 0.012, idx, f'cov {cov:.3f} | score {score:.3f}', va='center', ha='left', fontsize=11, color=PALETTE['ink'])
    fig.tight_layout()
    save_fig(fig, output_path)
    plt.close(fig)



def save_ablation(output_path: Path, payload: dict) -> None:
    configure_matplotlib()
    labels = ['Structured No Checker', 'Full Pipeline']
    coverage = [payload['ablation']['structured_no_checker']['avg_overall_coverage'], payload['ablation']['full_pipeline']['avg_overall_coverage']]
    scores = [payload['ablation']['structured_no_checker']['avg_checker_score'], payload['ablation']['full_pipeline']['avg_checker_score']]
    x = list(range(len(labels)))
    fig, ax = plt.subplots(figsize=(8.8, 5.5), dpi=180)
    width = 0.34
    ax.bar([i - width/2 for i in x], coverage, width=width, color=PALETTE['teal'], label='Coverage')
    ax.bar([i + width/2 for i in x], scores, width=width, color=PALETTE['accent'], label='Checker Score')
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 1.05)
    ax.grid(axis='y', color=PALETTE['line'], linestyle='--', alpha=0.7)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(frameon=False, loc='upper left')
    for i, (cov, score) in enumerate(zip(coverage, scores)):
        ax.text(i - width/2, cov + 0.03, f'{cov:.3f}', ha='center', fontsize=10.5, color=PALETTE['ink'])
        ax.text(i + width/2, score + 0.03, f'{score:.3f}', ha='center', fontsize=10.5, color=PALETTE['ink'])
    fig.tight_layout()
    save_fig(fig, output_path)
    plt.close(fig)



def save_generalization(output_path: Path, categories: list[dict]) -> None:
    configure_matplotlib()
    label_map = {
        'business_rules': 'Business Rules',
        'input_validation': 'Input Validation',
        'workflow_state': 'Workflow State',
    }
    labels = [label_map[item['category']] for item in categories]
    coverage = [item['avg_overall_coverage'] for item in categories]
    scores = [item['avg_checker_score'] for item in categories]
    colors = [PALETTE['accent'], PALETTE['gold'], PALETTE['teal']]
    fig, ax = plt.subplots(figsize=(8.8, 5.6), dpi=180)
    bars = ax.bar(labels, coverage, color=colors, width=0.58)
    ax.plot(labels, scores, color=PALETTE['ink'], marker='o', linewidth=2.5, markersize=7, label='Checker Score')
    ax.set_ylim(0, 1.02)
    ax.grid(axis='y', color=PALETTE['line'], linestyle='--', alpha=0.7)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(frameon=False, loc='upper left')
    for bar, cov, score in zip(bars, coverage, scores):
        ax.text(bar.get_x() + bar.get_width()/2, cov + 0.03, f'cov {cov:.3f}', ha='center', fontsize=10.5, color=PALETTE['ink'])
        ax.text(bar.get_x() + bar.get_width()/2, score + 0.03, f'score {score:.3f}', ha='center', fontsize=10.5, color=PALETTE['ink'])
    fig.tight_layout()
    save_fig(fig, output_path)
    plt.close(fig)



def save_stability(output_path: Path, stability: dict) -> None:
    configure_matplotlib()
    labels = [
        'Bundle\ndiscount',
        'Refund\nmethod',
        'Pickup\ncontact',
        'Card expiry\nand CVV',
        '3DS\nauthentication',
    ]
    formal = [item['formal_coverage'] for item in stability['comparisons']]
    rerun = [item['rerun_coverage'] for item in stability['comparisons']]
    score_formal = [item['formal_score'] for item in stability['comparisons']]
    score_rerun = [item['rerun_score'] for item in stability['comparisons']]
    x = range(len(labels))
    fig, axes = plt.subplots(2, 1, figsize=(10.4, 6.8), dpi=180, sharex=True)
    width = 0.36
    axes[0].bar([i - width/2 for i in x], formal, width=width, color=PALETTE['teal'], label='Formal')
    axes[0].bar([i + width/2 for i in x], rerun, width=width, color=PALETTE['gold'], label='Sanity Rerun')
    axes[0].set_ylim(0, 1.02)
    axes[0].set_ylabel('Coverage')
    axes[0].legend(frameon=False, loc='upper left')
    axes[0].grid(axis='y', color=PALETTE['line'], linestyle='--', alpha=0.7)
    axes[0].spines[['top', 'right']].set_visible(False)

    axes[1].plot(labels, score_formal, color=PALETTE['accent'], marker='o', linewidth=2.2, label='Formal score')
    axes[1].plot(labels, score_rerun, color=PALETTE['purple'], marker='o', linewidth=2.2, label='Rerun score')
    axes[1].set_ylim(0.7, 1.02)
    axes[1].set_ylabel('Checker Score')
    axes[1].grid(axis='y', color=PALETTE['line'], linestyle='--', alpha=0.7)
    axes[1].spines[['top', 'right']].set_visible(False)
    axes[1].legend(frameon=False, loc='upper left')
    axes[1].set_xticks(list(x), labels, rotation=0, ha='center')
    fig.tight_layout()
    save_fig(fig, output_path)
    plt.close(fig)



def save_scorecard(output_path: Path, payload: dict, categories: list[dict]) -> None:
    configure_matplotlib()
    fig = plt.figure(figsize=(12.5, 6.4), dpi=180)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    cards = [
        ('Test Split', f"{payload['main']['count']} requirements", PALETTE['gold_soft'], PALETTE['gold']),
        ('Avg Checker Score', f"{payload['main']['avg_checker_score']:.3f}", PALETTE['accent_soft'], PALETTE['accent']),
        ('Avg Coverage', f"{payload['main']['avg_overall_coverage']:.3f}", PALETTE['teal_soft'], PALETTE['teal']),
        ('Avg Test Count', f"{payload['main']['avg_test_count']:.3f}", PALETTE['purple_soft'], PALETTE['purple']),
    ]
    for idx, (label, value, fill, line) in enumerate(cards):
        x = 0.04 + idx * 0.236
        patch = FancyBboxPatch((x, 0.62), 0.205, 0.2, boxstyle='round,pad=0.012,rounding_size=0.025', facecolor=fill, edgecolor=line, linewidth=1.8)
        ax.add_patch(patch)
        ax.text(x + 0.02, 0.745, label, fontsize=11.2, color=PALETTE['muted'])
        ax.text(x + 0.1025, 0.67, value, fontsize=18.5, fontweight='bold', color=PALETTE['ink'], ha='center')
    ax.text(0.05, 0.50, 'Category Coverage', fontsize=15, fontweight='bold', color=PALETTE['ink'])
    y = 0.40
    label_map = {'business_rules': 'Business Rules', 'input_validation': 'Input Validation', 'workflow_state': 'Workflow State'}
    colors = [PALETTE['accent'], PALETTE['gold'], PALETTE['teal']]
    for idx, item in enumerate(categories):
        ax.add_patch(FancyBboxPatch((0.05, y - idx * 0.11), 0.64, 0.07, boxstyle='round,pad=0.008,rounding_size=0.02', facecolor=PALETTE['white'], edgecolor=PALETTE['line'], linewidth=1.1))
        ax.text(0.07, y + 0.022 - idx * 0.11, label_map[item['category']], fontsize=12.5, fontweight='bold', color=PALETTE['ink'])
        ax.add_patch(FancyBboxPatch((0.28, y - idx * 0.11 + 0.012), 0.3, 0.028, boxstyle='round,pad=0.002,rounding_size=0.01', facecolor=PALETTE['panel'], edgecolor='none'))
        ax.add_patch(FancyBboxPatch((0.28, y - idx * 0.11 + 0.012), 0.3 * item['avg_overall_coverage'], 0.028, boxstyle='round,pad=0.002,rounding_size=0.01', facecolor=colors[idx], edgecolor='none'))
        ax.text(0.60, y + 0.022 - idx * 0.11, f"cov {item['avg_overall_coverage']:.3f} | score {item['avg_checker_score']:.3f}", fontsize=11.5, color=PALETTE['muted'])
    save_fig(fig, output_path)
    plt.close(fig)



def save_case_study(output_path: Path, run_main: list[dict]) -> None:
    configure_matplotlib()
    selected = [
        'checkout_promo_stack_and_priority',
        'payment_card_expiry_and_cvv_validation',
        'payment_3ds_authentication_flow',
    ]
    by_id = {item['requirement_id']: item for item in run_main}
    label_map = {
        'checkout_promo_stack_and_priority': 'Business-rule case',
        'payment_card_expiry_and_cvv_validation': 'Input-validation case',
        'payment_3ds_authentication_flow': 'Workflow case',
    }
    fig, axes = plt.subplots(1, 3, figsize=(14.6, 5.3), dpi=180)
    for ax, rid, color in zip(axes, selected, [PALETTE['accent'], PALETTE['gold'], PALETTE['teal']]):
        item = by_id[rid]
        ax.set_axis_off()
        ax.add_patch(FancyBboxPatch((0.02, 0.05), 0.96, 0.9, boxstyle='round,pad=0.018,rounding_size=0.04', facecolor=PALETTE['white'], edgecolor=color, linewidth=2.0))
        ax.text(0.07, 0.86, label_map[rid], fontsize=15, fontweight='bold', color=PALETTE['ink'])
        ax.text(0.07, 0.76, textwrap.fill(rid.replace('_', ' '), width=26), fontsize=10.0, color=PALETTE['muted'])
        ax.text(0.07, 0.59, f"checker score: {float(item['score']):.3f}", fontsize=13, color=PALETTE['ink'])
        ax.text(0.07, 0.49, f"overall coverage: {float(item['metrics']['overall_coverage']):.3f}", fontsize=13, color=PALETTE['ink'])
        ax.text(0.07, 0.39, f"test cases: {int(item['metrics']['test_count'])}", fontsize=13, color=PALETTE['ink'])
        diags = item.get('diagnostics', [])[:1]
        ax.text(0.07, 0.20, 'diagnostics snapshot:', fontsize=11.5, color=PALETTE['muted'])
        y = 0.11
        for diag in diags:
            wrapped = textwrap.fill(textwrap.shorten(diag, width=52, placeholder='...'), width=32)
            ax.text(0.08, y, f"• {wrapped}", fontsize=9.2, color=PALETTE['muted'], va='top')
            y -= 0.09
    fig.tight_layout()
    save_fig(fig, output_path)
    plt.close(fig)



def write_readme(output_dir: Path) -> None:
    content = '''# Figure Assets

Generated by `experiments/generate_presentation_assets.py`.

Editable architecture:
- `arg_test_architecture_editable.pptx`

PNG figures:
- `final_result_scorecard.png`
- `main_vs_baselines.png`
- `ablation_gain.png`
- `generalization_by_category.png`
- `stability_sanity_check.png`
- `case_study_snapshots.png`

PDF figures:
- `final_result_scorecard.pdf`
- `main_vs_baselines.pdf`
- `ablation_gain.pdf`
- `generalization_by_category.pdf`
- `stability_sanity_check.pdf`
- `case_study_snapshots.pdf`

If you edit the architecture PPTX and want a PNG export, run:
`powershell -ExecutionPolicy Bypass -File experiments/export_architecture_slide.ps1 -PptxPath report_assets/figures/arg_test_architecture_editable.pptx -OutputDir report_assets/figures/architecture_png`
'''
    (output_dir / 'README.md').write_text(content, encoding='utf-8')



def main() -> None:
    parser = argparse.ArgumentParser(description='Generate PPTX and PNG presentation assets from final experiment results.')
    parser.add_argument('--output-root', default='.local_runs/formal_qwen_novpn')
    parser.add_argument('--stability-root', default='.local_runs/stability_qwen_20260411')
    parser.add_argument('--figure-dir', default='report_assets/figures')
    args = parser.parse_args()

    report_root = ROOT / args.output_root / 'outputs' / 'reports' / 'test'
    stability_root = ROOT / args.stability_root / 'outputs' / 'reports' / 'test'
    figure_dir = ROOT / args.figure_dir
    ensure_dir(figure_dir)

    run_main = read_json(report_root / 'run_main_summary.json')
    baseline = read_json(report_root / 'baseline_summary.json')
    ablation = read_json(report_root / 'ablation_summary.json')
    categories = read_json(report_root / 'generalization_by_category.json')['categories']
    stability = read_json(stability_root / 'stability_sanity_summary.json')
    payload = aggregate_payload(run_main, baseline, ablation)

    build_architecture_pptx(figure_dir / 'arg_test_architecture_editable.pptx')
    save_scorecard(figure_dir / 'final_result_scorecard.png', payload, categories)
    save_main_vs_baselines(figure_dir / 'main_vs_baselines.png', payload)
    save_ablation(figure_dir / 'ablation_gain.png', payload)
    save_generalization(figure_dir / 'generalization_by_category.png', categories)
    save_stability(figure_dir / 'stability_sanity_check.png', stability)
    save_case_study(figure_dir / 'case_study_snapshots.png', run_main)
    write_readme(figure_dir)

    print(json.dumps({
        'figure_dir': str(figure_dir),
        'generated': [
            'arg_test_architecture_editable.pptx',
            'final_result_scorecard.png',
            'final_result_scorecard.pdf',
            'main_vs_baselines.png',
            'main_vs_baselines.pdf',
            'ablation_gain.png',
            'ablation_gain.pdf',
            'generalization_by_category.png',
            'generalization_by_category.pdf',
            'stability_sanity_check.png',
            'stability_sanity_check.pdf',
            'case_study_snapshots.png',
            'case_study_snapshots.pdf',
            'README.md',
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

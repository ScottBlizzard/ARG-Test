from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

PALETTE = {
    'ink': '#132238',
    'muted': '#5B6677',
    'panel': '#F7F5EF',
    'panel_alt': '#EEF3F7',
    'accent': '#D55C3A',
    'accent_soft': '#F2C6B8',
    'teal': '#3B8C88',
    'teal_soft': '#B9DDD8',
    'gold': '#D8A332',
    'gold_soft': '#F5E3B5',
    'line': '#D8DCE3',
    'white': '#FFFFFF',
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs>',
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0%" stop-color="{PALETTE["white"]}"/>',
        f'<stop offset="100%" stop-color="{PALETTE["panel"]}"/>',
        '</linearGradient>',
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
        '<feDropShadow dx="0" dy="8" stdDeviation="12" flood-opacity="0.10"/>',
        '</filter>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="url(#bg)" rx="24"/>',
    ]


def svg_footer(parts: list[str]) -> str:
    return '\n'.join(parts + ['</svg>'])


def text(x: float, y: float, value: str, size: int = 18, weight: int = 400, fill: str | None = None, anchor: str = 'start') -> str:
    fill = fill or PALETTE['ink']
    safe = value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return (
        f'<text x="{x}" y="{y}" font-family="Segoe UI, Microsoft YaHei, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{safe}</text>'
    )


def rect(x: float, y: float, w: float, h: float, fill: str, rx: int = 18, stroke: str | None = None) -> str:
    stroke_attr = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{stroke_attr} filter="url(#shadow)"/>'


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = '#556070') -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
        f'<polygon points="{x2},{y2} {x2 - 12},{y2 - 6} {x2 - 12},{y2 + 6}" fill="{color}"/>'
    )


def metric_chip(x: float, y: float, label: str, value: str, color: str) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="150" height="34" rx="17" fill="{color}" opacity="0.14"/>'
        + text(x + 16, y + 22, f'{label}: {value}', size=14, weight=600, fill=PALETTE['ink'])
    )


def write_architecture_figure(output_path: Path) -> None:
    width, height = 1560, 880
    parts = svg_header(width, height)
    parts.extend([
        text(84, 92, 'ARG-Test Architecture', size=34, weight=700),
        text(84, 130, 'Requirement-driven black-box test generation with structured reasoning, checker validation, and repair.', size=18, fill=PALETTE['muted']),
        rect(90, 190, 250, 120, PALETTE['gold_soft'], stroke=PALETTE['gold']),
        text(125, 236, 'Requirement Dataset', size=24, weight=700),
        text(125, 272, 'dev/test requirements', size=18, fill=PALETTE['muted']),
        text(125, 298, 'gold specs + manifest', size=18, fill=PALETTE['muted']),
        rect(420, 190, 280, 120, PALETTE['panel_alt'], stroke=PALETTE['teal']),
        text(455, 236, 'Prompt Composer', size=24, weight=700),
        text(455, 272, 'system prompt + task prompt', size=18, fill=PALETTE['muted']),
        text(455, 298, 'Qwen3.5-Flash, 3 candidates', size=18, fill=PALETTE['muted']),
        rect(790, 190, 270, 120, '#FDEEEA', stroke=PALETTE['accent']),
        text(825, 236, 'Structured Trace', size=24, weight=700),
        text(825, 272, 'analysis / pattern / steps', size=18, fill=PALETTE['muted']),
        text(825, 298, 'verification / final answer', size=18, fill=PALETTE['muted']),
        rect(1145, 190, 310, 120, PALETTE['teal_soft'], stroke=PALETTE['teal']),
        text(1180, 236, 'Parser + Schema Gate', size=24, weight=700),
        text(1180, 272, 'parse trace to test cases', size=18, fill=PALETTE['muted']),
        text(1180, 298, 'typed JSON / CSV / markdown', size=18, fill=PALETTE['muted']),
        arrow(340, 250, 420, 250),
        arrow(700, 250, 790, 250),
        arrow(1060, 250, 1145, 250),
        rect(145, 420, 260, 134, '#FFF8E8', stroke=PALETTE['gold']),
        text(180, 466, 'EP/BVA Contract', size=24, weight=700),
        text(180, 502, 'partitions, invalid inputs,', size=18, fill=PALETTE['muted']),
        text(180, 528, 'boundaries and edge cases', size=18, fill=PALETTE['muted']),
        rect(470, 420, 280, 134, '#F2F7FB', stroke=PALETTE['teal']),
        text(505, 466, 'Decision Contract', size=24, weight=700),
        text(505, 502, 'rule combinations, priorities,', size=18, fill=PALETTE['muted']),
        text(505, 528, 'illegal rule interactions', size=18, fill=PALETTE['muted']),
        rect(825, 420, 280, 134, '#FDEEEA', stroke=PALETTE['accent']),
        text(860, 466, 'State Contract', size=24, weight=700),
        text(860, 502, 'states, transitions, retries,', size=18, fill=PALETTE['muted']),
        text(860, 528, 'exceptional paths', size=18, fill=PALETTE['muted']),
        rect(1170, 420, 225, 134, '#F4F0FA', stroke='#8366B2'),
        text(1205, 466, 'Rerank + Repair', size=24, weight=700),
        text(1205, 502, 'aggregate score, local repair,', size=18, fill=PALETTE['muted']),
        text(1205, 528, 'best candidate selection', size=18, fill=PALETTE['muted']),
        arrow(1300, 310, 1300, 420),
        arrow(1145, 487, 1105, 487),
        arrow(825, 487, 750, 487),
        arrow(470, 487, 405, 487),
        rect(350, 650, 380, 140, PALETTE['teal_soft'], stroke=PALETTE['teal']),
        text(385, 698, 'Final Test Suite', size=28, weight=700),
        text(385, 736, 'JSON + CSV + markdown test cases', size=18, fill=PALETTE['muted']),
        text(385, 764, 'chosen candidate after checker-guided selection', size=18, fill=PALETTE['muted']),
        rect(835, 650, 420, 140, '#FFF2EB', stroke=PALETTE['accent']),
        text(870, 698, 'Evaluation and Reports', size=28, weight=700),
        text(870, 736, 'run_main / baselines / ablation / generalization', size=18, fill=PALETTE['muted']),
        text(870, 764, 'coverage, checker score, category breakdown', size=18, fill=PALETTE['muted']),
        arrow(1282, 554, 1120, 650),
        arrow(1180, 554, 635, 650),
        metric_chip(98, 98, 'Model', 'Qwen3.5-Flash', PALETTE['accent']),
        metric_chip(258, 98, 'Candidates', '3', PALETTE['teal']),
        metric_chip(378, 98, 'Output', 'JSON / CSV / MD', PALETTE['gold']),
    ])
    output_path.write_text(svg_footer(parts), encoding='utf-8')


def draw_horizontal_bars(title: str, subtitle: str, items: Iterable[dict], output_path: Path) -> None:
    items = list(items)
    width, height = 1180, 720
    left, top = 130, 180
    row_h = 110
    bar_x = 400
    bar_w = 620
    parts = svg_header(width, height)
    parts.extend([
        text(76, 88, title, size=32, weight=700),
        text(76, 126, subtitle, size=17, fill=PALETTE['muted']),
        f'<line x1="{bar_x}" y1="145" x2="{bar_x + bar_w}" y2="145" stroke="{PALETTE["line"]}" stroke-width="1.5"/>',
    ])
    for tick in range(6):
        x = bar_x + bar_w * tick / 5
        parts.append(f'<line x1="{x}" y1="145" x2="{x}" y2="640" stroke="{PALETTE["line"]}" stroke-width="1" stroke-dasharray="4 8"/>')
        parts.append(text(x, 166, f'{tick/5:.1f}', size=14, fill=PALETTE['muted'], anchor='middle'))
    colors = [PALETTE['gold'], PALETTE['accent'], PALETTE['teal'], '#7C6BB0']
    softs = [PALETTE['gold_soft'], PALETTE['accent_soft'], PALETTE['teal_soft'], '#E2DAF3']
    for idx, item in enumerate(items):
        y = top + idx * row_h
        parts.append(rect(74, y - 36, 1030, 84, PALETTE['white'], rx=20, stroke=PALETTE['line']))
        parts.append(text(left, y, item['label'], size=22, weight=700))
        parts.append(text(left, y + 28, item['caption'], size=16, fill=PALETTE['muted']))
        bar_len = bar_w * item['coverage']
        parts.append(f'<rect x="{bar_x}" y="{y - 18}" width="{bar_w}" height="28" rx="14" fill="{softs[idx % len(softs)]}"/>')
        parts.append(f'<rect x="{bar_x}" y="{y - 18}" width="{bar_len}" height="28" rx="14" fill="{colors[idx % len(colors)]}"/>')
        parts.append(text(bar_x + bar_len + 12, y + 3, f"coverage {item['coverage']:.3f}", size=16, weight=600))
        parts.append(metric_chip(875, y - 30, 'score', f"{item['score']:.3f}", colors[idx % len(colors)]))
    output_path.write_text(svg_footer(parts), encoding='utf-8')


def write_main_vs_baselines(output_path: Path, payload: dict) -> None:
    baseline = payload['baseline']
    items = [
        {'label': 'Rule-based', 'caption': 'Traditional heuristic baseline', 'coverage': baseline['rule_based']['avg_overall_coverage'], 'score': baseline['rule_based']['avg_checker_score']},
        {'label': 'Plain LLM', 'caption': 'Single-pass prompting without ARG structure', 'coverage': baseline['plain_llm']['avg_overall_coverage'], 'score': baseline['plain_llm']['avg_checker_score']},
        {'label': 'Structured No Checker', 'caption': 'Structured generation without checker-guided selection', 'coverage': baseline['structured_no_checker']['avg_overall_coverage'], 'score': baseline['structured_no_checker']['avg_checker_score']},
        {'label': 'ARG-Test Full Pipeline', 'caption': 'Structured generation + checker + rerank + repair', 'coverage': payload['main']['avg_overall_coverage'], 'score': payload['main']['avg_checker_score']},
    ]
    draw_horizontal_bars('Main Comparison Against Baselines', 'Average overall coverage on the 16-case test split.', items, output_path)


def write_ablation(output_path: Path, payload: dict) -> None:
    items = [
        {'label': 'Structured No Checker', 'caption': 'Remove checker-guided reranking and repair', 'coverage': payload['ablation']['structured_no_checker']['avg_overall_coverage'], 'score': payload['ablation']['structured_no_checker']['avg_checker_score']},
        {'label': 'Full Pipeline', 'caption': 'ARG-Test with checker-guided selection and repair enabled', 'coverage': payload['ablation']['full_pipeline']['avg_overall_coverage'], 'score': payload['ablation']['full_pipeline']['avg_checker_score']},
    ]
    draw_horizontal_bars('Ablation Gain', 'Checker-guided selection and repair improve both coverage and quality.', items, output_path)


def write_category_figure(output_path: Path, categories: list[dict]) -> None:
    width, height = 1180, 760
    parts = svg_header(width, height)
    parts.extend([
        text(78, 88, 'Generalization by Requirement Category', size=32, weight=700),
        text(78, 126, 'Coverage bars with checker-score markers on the refreshed formal test results.', size=17, fill=PALETTE['muted']),
    ])
    chart_x, chart_y, chart_w, chart_h = 160, 180, 900, 470
    parts.append(f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="26" fill="{PALETTE["white"]}" stroke="{PALETTE["line"]}" filter="url(#shadow)"/>')
    for tick in range(6):
        y = chart_y + chart_h - (chart_h - 70) * tick / 5 - 36
        parts.append(f'<line x1="{chart_x + 90}" y1="{y}" x2="{chart_x + chart_w - 40}" y2="{y}" stroke="{PALETTE["line"]}" stroke-width="1" stroke-dasharray="4 8"/>')
        parts.append(text(chart_x + 68, y + 6, f'{tick/5:.1f}', size=14, fill=PALETTE['muted'], anchor='end'))
    labels = {
        'business_rules': 'Business Rules',
        'input_validation': 'Input Validation',
        'workflow_state': 'Workflow State',
    }
    bar_colors = [PALETTE['accent'], PALETTE['gold'], PALETTE['teal']]
    for idx, item in enumerate(categories):
        x = chart_x + 160 + idx * 250
        h = (chart_h - 90) * item['avg_overall_coverage']
        y = chart_y + chart_h - h - 36
        parts.append(f'<rect x="{x}" y="{y}" width="96" height="{h}" rx="18" fill="{bar_colors[idx]}" opacity="0.88"/>')
        dot_y = chart_y + chart_h - (chart_h - 90) * item['avg_checker_score'] - 36
        parts.append(f'<circle cx="{x + 48}" cy="{dot_y}" r="10" fill="{PALETTE["ink"]}"/>')
        parts.append(text(x + 48, chart_y + chart_h + 18, labels[item['category']], size=18, weight=700, anchor='middle'))
        parts.append(text(x + 48, chart_y + chart_h + 46, f"coverage {item['avg_overall_coverage']:.3f}", size=15, fill=PALETTE['muted'], anchor='middle'))
        parts.append(text(x + 48, chart_y + chart_h + 70, f"score {item['avg_checker_score']:.3f}", size=15, fill=PALETTE['muted'], anchor='middle'))
    parts.append(metric_chip(826, 98, 'Marker', 'checker score', PALETTE['ink']))
    output_path.write_text(svg_footer(parts), encoding='utf-8')


def aggregate_payload(run_main: list[dict], baseline: list[dict], ablation: list[dict]) -> dict:
    def avg(values: list[float]) -> float:
        return round(sum(values) / len(values), 3) if values else 0.0

    payload = {
        'main': {
            'avg_checker_score': avg([float(item['score']) for item in run_main]),
            'avg_overall_coverage': avg([float(item['metrics']['overall_coverage']) for item in run_main]),
        },
        'baseline': {},
        'ablation': {},
    }
    for method in ('rule_based', 'plain_llm', 'structured_no_checker'):
        payload['baseline'][method] = {
            'avg_checker_score': avg([float(item['baselines'][method]['checker_score']) for item in baseline]),
            'avg_overall_coverage': avg([float(item['baselines'][method]['overall_coverage']) for item in baseline]),
        }
    for method in ('structured_no_checker', 'full_pipeline'):
        payload['ablation'][method] = {
            'avg_checker_score': avg([float(item[method]['checker_score']) for item in ablation]),
            'avg_overall_coverage': avg([float(item[method]['overall_coverage']) for item in ablation]),
        }
    return payload


def write_readme(output_dir: Path) -> None:
    content = '''# Figures

Generated by `experiments/generate_report_figures.py`.

Files:
- `arg_test_architecture.svg`: system architecture / pipeline figure
- `main_vs_baselines.svg`: main result against baselines
- `ablation_gain.svg`: checker/repair ablation comparison
- `generalization_by_category.svg`: category-level performance

These SVG files are intended for direct insertion into the final report or PPT.
'''
    (output_dir / 'README.md').write_text(content, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate report-ready SVG figures from formal experiment results.')
    parser.add_argument('--output-root', default='.local_runs/formal_qwen_novpn', help='Runtime root containing formal outputs.')
    parser.add_argument('--figure-dir', default='report_assets/figures', help='Directory to place generated SVG figures.')
    args = parser.parse_args()

    report_root = ROOT / args.output_root / 'outputs' / 'reports' / 'test'
    figure_dir = ROOT / args.figure_dir
    ensure_dir(figure_dir)

    run_main = read_json(report_root / 'run_main_summary.json')
    baseline = read_json(report_root / 'baseline_summary.json')
    ablation = read_json(report_root / 'ablation_summary.json')
    generalization = read_json(report_root / 'generalization_by_category.json')['categories']
    payload = aggregate_payload(run_main, baseline, ablation)

    write_architecture_figure(figure_dir / 'arg_test_architecture.svg')
    write_main_vs_baselines(figure_dir / 'main_vs_baselines.svg', payload)
    write_ablation(figure_dir / 'ablation_gain.svg', payload)
    write_category_figure(figure_dir / 'generalization_by_category.svg', generalization)
    write_readme(figure_dir)

    print(json.dumps({
        'figure_dir': str(figure_dir),
        'generated': [
            'arg_test_architecture.svg',
            'main_vs_baselines.svg',
            'ablation_gain.svg',
            'generalization_by_category.svg',
            'README.md',
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()


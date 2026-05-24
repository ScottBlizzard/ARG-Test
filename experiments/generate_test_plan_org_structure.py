from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "final_docs" / "test_plan" / "figures" / "test_plan_org_structure.png"

PALETTE = {
    "ink": (19, 34, 56),
    "muted": (91, 102, 119),
    "line": (165, 175, 190),
    "blue": (232, 238, 245),
    "gold": (245, 227, 181),
    "teal": (185, 221, 216),
    "red": (242, 198, 184),
    "purple": (244, 240, 250),
    "border": (80, 115, 150),
}


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = Path("C:/Windows/Fonts") / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def _connector(draw: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int) -> None:
    draw.line((x1, y1, x2, y2), fill=PALETTE["line"], width=4)


def _box(
    draw: ImageDraw.ImageDraw,
    xywh: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    title: str,
    subtitle: str,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
) -> None:
    x, y, width, height = xywh
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=18,
        fill=fill,
        outline=PALETTE["border"],
        width=3,
    )
    draw.text((x + 28, y + 22), title, font=title_font, fill=PALETTE["ink"])
    line_y = y + 76
    for line in _wrap(draw, subtitle, body_font, width - 56):
        draw.text((x + 28, line_y), line, font=body_font, fill=PALETTE["muted"])
        line_y += 30


def save_test_plan_org_structure(output_path: Path = DEFAULT_OUTPUT) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1800, 1050
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    title_font = _font("arialbd.ttf", 36)
    body_font = _font("arial.ttf", 24)
    box_body_font = _font("arial.ttf", 22)
    note_font = _font("arialbd.ttf", 23)

    draw.text(
        (70, 55),
        "Test Activity Organization for AutoTestDesign AI App",
        font=title_font,
        fill=PALETTE["ink"],
    )
    draw.text(
        (70, 105),
        "Responsibilities are organized around evidence, experiments, evaluation, and final reporting.",
        font=body_font,
        fill=PALETTE["muted"],
    )

    leader = (590, 170, 620, 160)
    _box(
        draw,
        leader,
        PALETTE["blue"],
        "Yi Xu",
        "Team leader; pipeline control, formal result root, evidence consistency",
        title_font,
        body_font,
    )
    center_x = leader[0] + leader[2] // 2
    base_y = leader[1] + leader[3]
    _connector(draw, center_x, base_y, center_x, 420)
    _connector(draw, 275, 420, 1530, 420)

    members = [
        (
            (90, 495, 365, 230),
            PALETTE["gold"],
            "Xiang Wang",
            "Data assets and main experiment support; requirement data and gold spec evaluation materials",
        ),
        (
            (500, 495, 365, 230),
            PALETTE["teal"],
            "Fengxuan Kang",
            "Baseline and detailed execution support; rule-based, plain-LLM, and structured-no-checker comparison",
        ),
        (
            (910, 495, 365, 230),
            PALETTE["red"],
            "Yiwei Chen",
            "Evaluation and verification materials; coverage, ablation, generalization interpretation",
        ),
        (
            (1320, 495, 365, 230),
            PALETTE["purple"],
            "Luowu Zhang",
            "Report, test plan, PPT, demo assets, and wording synchronization",
        ),
    ]
    for xywh, fill, title, subtitle in members:
        x, y, box_width, _ = xywh
        _connector(draw, x + box_width // 2, 420, x + box_width // 2, y)
        _box(draw, xywh, fill, title, subtitle, title_font, box_body_font)

    note_x, note_y, note_width, note_height = 250, 845, 1300, 120
    draw.rounded_rectangle(
        (note_x, note_y, note_x + note_width, note_y + note_height),
        radius=16,
        fill=(250, 250, 250),
        outline=PALETTE["line"],
        width=2,
    )
    note = "Evidence flow: requirements -> pipeline outputs -> evaluation summaries -> final documents and demo package"
    for index, line in enumerate(_wrap(draw, note, note_font, note_width - 60)):
        draw.text((note_x + 30, note_y + 24 + index * 28), line, font=note_font, fill=PALETTE["ink"])
    draw.text(
        (note_x + 30, note_y + 82),
        "The structure supports traceable testing activities for the selected target application.",
        font=box_body_font,
        fill=PALETTE["muted"],
    )

    image.save(output_path)
    return output_path


def main() -> None:
    print(save_test_plan_org_structure())


if __name__ == "__main__":
    main()

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import KeepTogether


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "final_docs" / "risk_analysis_report" / "02_risk_analysis_report_cn.md",
    ROOT / "final_docs" / "test_plan" / "03_test_plan_cn.md",
    ROOT / "final_docs" / "detailed_test_design_execution" / "04_detailed_test_design_execution_cn.md",
]

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 1.7 * cm
RIGHT_MARGIN = 1.7 * cm
TOP_MARGIN = 1.6 * cm
BOTTOM_MARGIN = 1.5 * cm
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

COLORS = {
    "ink": colors.HexColor("#132238"),
    "muted": colors.HexColor("#5B6677"),
    "line": colors.HexColor("#D8DCE3"),
    "paper": colors.HexColor("#FBFAF6"),
    "white": colors.white,
    "gold_soft": colors.HexColor("#F5E3B5"),
    "teal_soft": colors.HexColor("#B9DDD8"),
}


def build_styles() -> StyleSheet1:
    styles = getSampleStyleSheet()
    styles["BodyText"].fontName = "Helvetica"
    styles["BodyText"].fontSize = 10.2
    styles["BodyText"].leading = 14
    styles["BodyText"].textColor = COLORS["ink"]
    styles["BodyText"].spaceAfter = 6

    styles["Title"].fontName = "Helvetica-Bold"
    styles["Title"].fontSize = 18
    styles["Title"].leading = 22
    styles["Title"].textColor = COLORS["ink"]
    styles["Title"].alignment = TA_CENTER
    styles["Title"].spaceAfter = 14

    styles.add(
        ParagraphStyle(
            name="Heading1Final",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=COLORS["ink"],
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading2Final",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=COLORS["ink"],
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading3Final",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.8,
            leading=13.5,
            textColor=COLORS["ink"],
            spaceBefore=6,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletFinal",
            parent=styles["BodyText"],
            leftIndent=14,
            firstLineIndent=0,
            bulletIndent=4,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeFinal",
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            backColor=COLORS["paper"],
            borderColor=COLORS["line"],
            borderWidth=0.5,
            borderPadding=6,
            borderRadius=4,
            spaceBefore=4,
            spaceAfter=8,
            textColor=COLORS["ink"],
        )
    )
    styles.add(
        ParagraphStyle(
            name="CaptionFinal",
            parent=styles["BodyText"],
            fontSize=8.8,
            leading=11,
            textColor=COLORS["muted"],
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterFinal",
            parent=styles["BodyText"],
            fontSize=8.2,
            leading=10,
            textColor=COLORS["muted"],
            alignment=TA_CENTER,
        )
    )
    return styles


INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def inline_to_para(text: str) -> str:
    escaped = html.escape(text)
    escaped = BOLD_RE.sub(r"<b>\1</b>", escaped)
    escaped = ITALIC_RE.sub(r"<i>\1</i>", escaped)
    escaped = INLINE_CODE_RE.sub(
        r'<font name="Courier" backcolor="#FBFAF6">\1</font>', escaped
    )
    return escaped


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def is_table_row(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped.replace("|", "").replace(" ", "")) <= {"-"}


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def image_flow(path: Path, alt_text: str, styles: StyleSheet1) -> list:
    story: list = []
    if not path.exists():
        story.append(Paragraph(inline_to_para(f"[Missing image: {path.name}]"), styles["BodyText"]))
        return story
    img = Image(str(path))
    max_width = CONTENT_WIDTH
    img.drawWidth, img.drawHeight = scale_dimensions(img.drawWidth, img.drawHeight, max_width, 16.0 * cm)
    story.append(Spacer(1, 4))
    story.append(KeepTogether([img, Spacer(1, 2), Paragraph(inline_to_para(alt_text), styles["CaptionFinal"])]))
    return story


def scale_dimensions(width: float, height: float, max_width: float, max_height: float) -> tuple[float, float]:
    ratio = min(max_width / width, max_height / height, 1.0)
    return width * ratio, height * ratio


def parse_markdown(path: Path, styles: StyleSheet1) -> list:
    lines = read_lines(path)
    story: list = []
    idx = 0

    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 4))
            idx += 1
            continue

        if stripped.startswith("```"):
            code_lines = []
            idx += 1
            while idx < len(lines) and not lines[idx].strip().startswith("```"):
                code_lines.append(lines[idx])
                idx += 1
            story.append(Preformatted("\n".join(code_lines), styles["CodeFinal"]))
            idx += 1
            continue

        image_match = IMAGE_RE.fullmatch(stripped)
        if image_match:
            alt_text, rel_path = image_match.groups()
            story.extend(image_flow((path.parent / rel_path).resolve(), alt_text, styles))
            idx += 1
            continue

        if is_table_row(stripped) and idx + 1 < len(lines) and is_table_separator(lines[idx + 1]):
            table_lines = [lines[idx]]
            idx += 2
            while idx < len(lines) and is_table_row(lines[idx]):
                table_lines.append(lines[idx])
                idx += 1
            story.append(build_table(table_lines, styles))
            story.append(Spacer(1, 6))
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            heading = stripped[level:].strip()
            if level == 1:
                story.append(Paragraph(inline_to_para(heading), styles["Title"]))
            elif level == 2:
                story.append(Paragraph(inline_to_para(heading), styles["Heading1Final"]))
            elif level == 3:
                story.append(Paragraph(inline_to_para(heading), styles["Heading2Final"]))
            else:
                story.append(Paragraph(inline_to_para(heading), styles["Heading3Final"]))
            idx += 1
            continue

        if stripped.startswith("- "):
            items = []
            while idx < len(lines) and lines[idx].strip().startswith("- "):
                content = lines[idx].strip()[2:].strip()
                items.append(ListItem(Paragraph(inline_to_para(content), styles["BodyText"])))
                idx += 1
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=16))
            story.append(Spacer(1, 4))
            continue

        if re.match(r"^\d+\.\s", stripped):
            items = []
            while idx < len(lines) and re.match(r"^\d+\.\s", lines[idx].strip()):
                content = re.sub(r"^\d+\.\s+", "", lines[idx].strip())
                items.append(ListItem(Paragraph(inline_to_para(content), styles["BodyText"])))
                idx += 1
            story.append(ListFlowable(items, bulletType="1", leftIndent=16))
            story.append(Spacer(1, 4))
            continue

        paragraph_lines = [stripped]
        idx += 1
        while idx < len(lines):
            peek = lines[idx].strip()
            if (
                not peek
                or peek.startswith("#")
                or peek.startswith("```")
                or peek.startswith("- ")
                or re.match(r"^\d+\.\s", peek)
                or is_table_row(peek)
                or IMAGE_RE.fullmatch(peek)
            ):
                break
            paragraph_lines.append(peek)
            idx += 1
        story.append(Paragraph(inline_to_para(" ".join(paragraph_lines)), styles["BodyText"]))
    return story


def build_table(table_lines: list[str], styles: StyleSheet1) -> Table:
    rows = [split_table_row(line) for line in table_lines]
    paragraphs = [
        [Paragraph(inline_to_para(cell), styles["BodyText"]) for cell in row]
        for row in rows
    ]
    col_count = len(paragraphs[0])
    col_width = CONTENT_WIDTH / col_count
    table = Table(paragraphs, colWidths=[col_width] * col_count, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COLORS["gold_soft"]),
                ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["ink"]),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, COLORS["line"]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), COLORS["white"]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8.2)
    canvas.setFillColor(COLORS["muted"])
    canvas.drawCentredString(PAGE_WIDTH / 2, 0.8 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(md_path: Path, styles: StyleSheet1) -> Path:
    pdf_path = md_path.with_suffix(".pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=md_path.stem,
    )
    story = parse_markdown(md_path, styles)
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return pdf_path


def main() -> None:
    styles = build_styles()
    outputs = [build_pdf(path, styles) for path in DOCS]
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()

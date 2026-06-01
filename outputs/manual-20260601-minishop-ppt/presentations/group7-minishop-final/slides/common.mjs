import path from "node:path";

export const THEME = {
  bg: "#FFFDFC",
  paper: "#FFF7F6",
  card: "#FFFFFF",
  blush: "#F6DAD7",
  blushDark: "#E7B9B4",
  rose: "#D88F88",
  ink: "#253042",
  body: "#5C6470",
  muted: "#8A9098",
  green: "#2E8B73",
  gold: "#D2A63E",
  blue: "#7FA9C9",
  line: "#E8CECA",
};

export const REPO_ROOT = process.cwd();
export const PPT_ASSET_ROOT = path.join(REPO_ROOT, "07_PPT_Assets_For_Luowu");

export function assetPath(...parts) {
  return path.join(PPT_ASSET_ROOT, ...parts);
}

export function bg(slide, ctx) {
  ctx.addShape(slide, {
    left: 0,
    top: 0,
    width: ctx.W,
    height: ctx.H,
    fill: THEME.bg,
    line: ctx.line(THEME.bg, 0),
    name: "bg",
  });
  ctx.addShape(slide, {
    left: 0,
    top: 0,
    width: 28,
    height: ctx.H,
    fill: THEME.blush,
    line: ctx.line(THEME.blush, 0),
    name: "left-accent",
  });
  ctx.addShape(slide, {
    left: 0,
    top: ctx.H - 18,
    width: ctx.W,
    height: 18,
    fill: "#F6E4E2",
    line: ctx.line("#F6E4E2", 0),
    name: "bottom-accent",
  });
}

export function title(slide, ctx, kicker, claim) {
  if (kicker) {
    ctx.addText(slide, {
      text: kicker,
      left: 60,
      top: 34,
      width: 260,
      height: 22,
      fontSize: 12,
      color: THEME.rose,
      bold: true,
      typeface: "Aptos",
      name: "kicker-label",
    });
  }
  ctx.addText(slide, {
    text: claim,
    left: 60,
    top: kicker ? 52 : 42,
    width: 1120,
    height: 70,
    fontSize: 31,
    color: THEME.rose,
    typeface: "Georgia",
    name: "title",
  });
}

export function bodyText(slide, ctx, text, x, y, w, h, opts = {}) {
  return ctx.addText(slide, {
    text,
    left: x,
    top: y,
    width: w,
    height: h,
    fontSize: opts.size ?? 20,
    color: opts.color ?? THEME.body,
    bold: Boolean(opts.bold),
    typeface: opts.face ?? "Aptos",
    align: opts.align ?? "left",
    valign: opts.valign ?? "top",
    fill: opts.fill ?? "#00000000",
    line: opts.line ?? ctx.line("#00000000", 0),
    insets: opts.insets ?? { left: 0, right: 0, top: 0, bottom: 0 },
    name: opts.name,
  });
}

export function card(slide, ctx, x, y, w, h, opts = {}) {
  ctx.addShape(slide, {
    left: x,
    top: y,
    width: w,
    height: h,
    geometry: "rect",
    fill: opts.fill ?? THEME.card,
    line: ctx.line(opts.lineColor ?? THEME.line, opts.lineWidth ?? 1.5),
    name: opts.name,
  });
  if (opts.band) {
    ctx.addShape(slide, {
      left: x,
      top: y,
      width: w,
      height: opts.bandHeight ?? 10,
      geometry: "rect",
      fill: opts.band,
      line: ctx.line(opts.band, 0),
      name: `${opts.name || "card"}-band`,
    });
  }
}

export function labelChip(slide, ctx, text, x, y, w = 190) {
  card(slide, ctx, x, y, w, 28, {
    fill: THEME.paper,
    lineColor: THEME.line,
    lineWidth: 1,
    name: `chip-${text}`,
  });
  bodyText(slide, ctx, text, x + 10, y + 6, w - 20, 18, {
    size: 11,
    color: THEME.ink,
    bold: true,
    name: `chip-text-${text}`,
  });
}

export function bulletList(slide, ctx, items, x, y, w, opts = {}) {
  const lineHeight = opts.lineHeight ?? 26;
  items.forEach((item, index) => {
    bodyText(slide, ctx, "•", x, y + index * lineHeight, 16, 20, {
      size: opts.size ?? 18,
      color: opts.bulletColor ?? THEME.rose,
      bold: true,
      name: `bullet-dot-${index}`,
    });
    bodyText(slide, ctx, item, x + 18, y + index * lineHeight, w - 18, lineHeight + 10, {
      size: opts.size ?? 18,
      color: opts.color ?? THEME.body,
      bold: false,
      name: `bullet-text-${index}`,
    });
  });
}

export async function image(slide, ctx, imagePath, x, y, w, h, fit = "contain", name = "image") {
  return ctx.addImage(slide, {
    path: imagePath,
    left: x,
    top: y,
    width: w,
    height: h,
    fit,
    name,
  });
}

export function divider(slide, ctx, x, y, w) {
  ctx.addShape(slide, {
    left: x,
    top: y,
    width: w,
    height: 1.5,
    fill: THEME.line,
    line: ctx.line(THEME.line, 0),
    name: `divider-${x}-${y}`,
  });
}

export function metricCard(slide, ctx, x, y, w, h, label, value, note, accent) {
  card(slide, ctx, x, y, w, h, {
    fill: "#FFFBFA",
    lineColor: accent,
    lineWidth: 2,
    name: `metric-${label}`,
  });
  bodyText(slide, ctx, label, x + 18, y + 18, w - 36, 24, {
    size: 14,
    color: THEME.body,
    bold: true,
    name: `metric-label-${label}`,
  });
  bodyText(slide, ctx, value, x + 18, y + 54, w - 36, 44, {
    size: 30,
    color: THEME.ink,
    bold: true,
    face: "Georgia",
    name: `metric-value-${label}`,
  });
  if (note) {
    bodyText(slide, ctx, note, x + 18, y + h - 34, w - 36, 20, {
      size: 13,
      color: THEME.muted,
      name: `metric-note-${label}`,
    });
  }
}

export function trioArrow(slide, ctx, x1, x2, y) {
  ctx.addShape(slide, {
    left: x1,
    top: y,
    width: x2 - x1,
    height: 2,
    fill: THEME.line,
    line: ctx.line(THEME.line, 0),
    name: `arrow-line-${x1}-${x2}`,
  });
  ctx.addShape(slide, {
    left: x2 - 10,
    top: y - 5,
    width: 10,
    height: 12,
    geometry: "chevron",
    fill: THEME.line,
    line: ctx.line(THEME.line, 0),
    name: `arrow-head-${x2}`,
  });
}

import {
  THEME,
  assetPath,
  bg,
  title,
  bodyText,
  bulletList,
  card,
  labelChip,
  image,
  divider,
  metricCard,
} from "./common.mjs";

const members = [
  "Yi Xu 2351441",
  "Xiang Wang 2351039",
  "Fengxuan Kang 2350283",
  "Luowu Zhang 2352746",
  "Yiwei Chen 2350217",
];

export async function buildSlide01(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  bodyText(slide, ctx, "Software Testing 42036101 Final Project", 360, 212, 560, 28, {
    size: 16,
    color: THEME.muted,
    align: "center",
    name: "course",
  });
  bodyText(slide, ctx, "ARG-Test", 220, 110, 840, 70, {
    size: 42,
    color: THEME.ink,
    bold: true,
    face: "Georgia",
    align: "center",
    name: "main-title",
  });
  bodyText(slide, ctx, "Auditable and Risk-Aware\nRequirement-Driven Black-Box Test Generation", 180, 154, 920, 70, {
    size: 22,
    color: THEME.body,
    align: "center",
    name: "subtitle",
  });
  card(slide, ctx, 420, 260, 440, 34, { fill: "#FFF9F8", lineColor: THEME.line, lineWidth: 1.2, name: "team-pill" });
  bodyText(slide, ctx, "Team ID: Group 7", 420, 268, 440, 18, {
    size: 15,
    color: THEME.ink,
    bold: true,
    align: "center",
    name: "teamid",
  });
  card(slide, ctx, 205, 355, 870, 210, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1, name: "member-card" });
  bodyText(slide, ctx, "Members", 255, 385, 160, 22, { size: 16, color: THEME.rose, bold: true, name: "members-kicker" });
  members.forEach((member, index) => {
    bodyText(slide, ctx, member, 255 + (index > 1 ? 360 : 0), 430 + (index % 3) * 34, 300, 22, {
      size: 18,
      color: THEME.body,
      name: `member-${index}`,
    });
  });
  bodyText(slide, ctx, "Tool: ARG-Test | Target application: MiniShop Checkout", 205, 592, 870, 20, {
    size: 14,
    color: THEME.muted,
    align: "center",
    name: "cover-note",
  });
  return slide;
}

export async function buildSlide02(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Assignment Goal and Final Object Separation");
  card(slide, ctx, 82, 160, 1116, 110, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1, name: "goal-card" });
  bodyText(slide, ctx, "Assignment goal: build an AI-driven AutoTestDesign tool and use it to test an independent target application.", 110, 195, 1060, 50, {
    size: 24,
    color: THEME.ink,
    align: "center",
    name: "goal-line",
  });
  const boxes = [
    { x: 96, label: "Tool", title: "ARG-Test", note: "Requirement analysis\nRisk scoring\nSystematic test design", color: THEME.blush },
    { x: 454, label: "Target Application", title: "MiniShop Checkout", note: "Promotion\nShipping / Tax\nPayment / Pickup\nCheckout orchestration", color: "#EAF5F1" },
    { x: 812, label: "Selected Module", title: "coupon_discount_engine", note: "Promotion service coupon engine\nDetailed executable evidence", color: "#FFF5E8" },
  ];
  for (const box of boxes) {
    card(slide, ctx, box.x, 320, 292, 220, { fill: box.color, lineColor: THEME.line, lineWidth: 1.4, name: `${box.title}-card` });
    labelChip(slide, ctx, box.label.toUpperCase(), box.x + 16, 338, 120);
    bodyText(slide, ctx, box.title, box.x + 18, 390, 256, 52, {
      size: 22,
      color: THEME.ink,
      bold: true,
      face: "Georgia",
      name: `${box.title}-title`,
    });
    bodyText(slide, ctx, box.note, box.x + 18, 456, 250, 70, {
      size: 16,
      color: THEME.body,
      name: `${box.title}-note`,
    });
  }
  bodyText(slide, ctx, "This separation is the key correction from the earlier version.", 82, 590, 1116, 24, {
    size: 17,
    color: THEME.rose,
    bold: true,
    align: "center",
    name: "correction-note",
  });
  return slide;
}

export async function buildSlide03(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "MiniShop Checkout: Target Application Scope");
  card(slide, ctx, 84, 142, 430, 430, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "scope-left" });
  bodyText(slide, ctx, "MiniShop Checkout is a compact e-commerce checkout prototype built specifically for this final project.", 114, 185, 370, 70, {
    size: 23,
    color: THEME.ink,
    face: "Georgia",
    name: "scope-summary",
  });
  divider(slide, ctx, 114, 272, 360);
  bodyText(slide, ctx, "Implemented scope", 114, 292, 180, 24, { size: 16, color: THEME.rose, bold: true, name: "implemented-kicker" });
  bulletList(slide, ctx, [
    "Promotion and coupon handling",
    "Shipping-fee calculation",
    "Tax and order-total calculation",
    "Payment-card validation",
    "Pickup-contact validation",
    "Checkout preview orchestration",
  ], 114, 330, 360, { size: 18, lineHeight: 34 });
  card(slide, ctx, 550, 142, 648, 430, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "scope-right" });
  bodyText(slide, ctx, "Component map", 580, 175, 200, 24, { size: 16, color: THEME.rose, bold: true, name: "component-kicker" });
  const comps = [
    ["Promotion Service", "coupon rules and restrictions"],
    ["Shipping Service", "fee tiers and shipping thresholds"],
    ["Tax Service", "taxable amount and order total"],
    ["Payment Validation", "card number, expiry, CVV, brand rules"],
    ["Pickup Validation", "station ID, phone, pickup code"],
    ["Checkout Service", "end-to-end preview orchestration"],
  ];
  comps.forEach((comp, index) => {
    const row = Math.floor(index / 2);
    const col = index % 2;
    const x = 580 + col * 300;
    const y = 218 + row * 110;
    card(slide, ctx, x, y, 260, 88, { fill: index % 2 === 0 ? "#FFF7F6" : "#F7FBFA", lineColor: THEME.line, lineWidth: 1, name: `comp-${index}` });
    bodyText(slide, ctx, comp[0], x + 16, y + 14, 228, 24, { size: 16, color: THEME.ink, bold: true, name: `comp-title-${index}` });
    bodyText(slide, ctx, comp[1], x + 16, y + 42, 228, 28, { size: 13, color: THEME.body, name: `comp-note-${index}` });
  });
  bodyText(slide, ctx, "Out of scope: refund workflows, inventory sync, external payment gateway integration", 84, 610, 1116, 20, {
    size: 16,
    color: THEME.muted,
    align: "center",
    name: "scope-boundary",
  });
  return slide;
}

export async function buildSlide04(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Why Plain LLM Is Not Enough");
  bodyText(slide, ctx, "Plain LLM outputs can be fluent, but they are not reliably auditable.", 82, 128, 1110, 24, {
    size: 20,
    color: THEME.body,
    name: "why-lead",
  });
  card(slide, ctx, 88, 176, 500, 360, { fill: "#FFF9F8", lineColor: THEME.line, lineWidth: 1.3, name: "plain-card" });
  card(slide, ctx, 692, 176, 500, 360, { fill: "#F9FCFB", lineColor: THEME.line, lineWidth: 1.3, name: "arg-card" });
  labelChip(slide, ctx, "PLAIN LLM OUTPUT", 108, 196, 150);
  labelChip(slide, ctx, "ARG-TEST STRUCTURED TRACE", 712, 196, 210);
  bodyText(slide, ctx, "Try SAVE10 on a valid order.\nTry an expired coupon.\nCheck that the discount is correct.\n\nLooks fluent, but gives no clear\nboundary, conflict, or traceability plan.", 116, 244, 438, 220, {
    size: 22,
    color: THEME.body,
    name: "plain-text",
  });
  bodyText(slide, ctx, "Analysis: thresholds 30 / 50 / 100,\npremium-only SAVE20, expiry, sale-item conflict\n\nPattern: EP + BVA + Decision Table\n\nVerification: boundary, invalid, and exclusivity\nobligations are explicitly checked\n\nFinal tests: subtotal=50, expired coupon,\nSAVE20 + sale items, coupon stacking rejected", 720, 244, 438, 230, {
    size: 18,
    color: THEME.body,
    name: "arg-text",
  });
  bodyText(slide, ctx, "The problem is not only correctness. The deeper issue is auditability.", 120, 585, 1040, 30, {
    size: 22,
    color: THEME.rose,
    bold: true,
    align: "center",
    name: "bottom-takeaway",
  });
  return slide;
}

export async function buildSlide05(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "ARG-Test Final System Overview");
  await image(slide, ctx, assetPath("figures_png", "arg_test_architecture_final.png"), 84, 132, 760, 500, "contain", "architecture");
  card(slide, ctx, 882, 150, 280, 444, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "architecture-notes" });
  labelChip(slide, ctx, "PIPELINE", 902, 172, 86);
  bulletList(slide, ctx, [
    "ARG-Test is a pipeline, not a single prompt",
    "Structured generation",
    "Parser and schema gate",
    "Technique-aware checker",
    "Rerank and targeted repair",
    "Export, evaluation, and reproducible reporting",
  ], 904, 216, 232, { size: 18, lineHeight: 48 });
  return slide;
}

export async function buildSlide06(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Structured Trace and Contract Checking");
  await image(slide, ctx, assetPath("slide5_trace_checker_schematic.svg"), 96, 154, 1088, 270, "contain", "trace-schematic");
  card(slide, ctx, 96, 468, 1088, 126, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.1, name: "trace-caption-card" });
  bodyText(slide, ctx, "Typed trace: Analysis -> Pattern -> Steps -> Verification -> FinalAnswer", 128, 498, 980, 26, {
    size: 22,
    color: THEME.ink,
    bold: true,
    name: "trace-line",
  });
  bodyText(slide, ctx, "The model output becomes a typed artifact that can be parsed, checked, and repaired.", 128, 540, 980, 24, {
    size: 18,
    color: THEME.body,
    name: "trace-body",
  });
  return slide;
}

export async function buildSlide07(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Requirement Closure and Interactive Review");
  card(slide, ctx, 86, 144, 510, 462, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "closure-card" });
  bodyText(slide, ctx, "Mandatory requirement closure", 114, 176, 300, 22, { size: 16, color: THEME.rose, bold: true, name: "closure-k1" });
  bodyText(slide, ctx, "FR 1.0, FR 1.1, FR 2.0, FR 3.0, FR 6.0", 114, 208, 430, 30, { size: 24, color: THEME.ink, bold: true, name: "closure-main" });
  bodyText(slide, ctx, "Extra-credit closure", 114, 258, 250, 22, { size: 16, color: THEME.rose, bold: true, name: "closure-k2" });
  bodyText(slide, ctx, "FR 4.0, FR 5.0, FR 7.0", 114, 290, 430, 30, { size: 24, color: THEME.ink, bold: true, name: "closure-extra" });
  bodyText(slide, ctx, "Interactive review surface", 114, 342, 260, 22, { size: 16, color: THEME.rose, bold: true, name: "closure-k3" });
  bulletList(slide, ctx, [
    "Direct Input",
    "CSV Batch",
    "State Model",
    "Formal Evidence",
    "Inspect outputs, revise guidance, rerun the pipeline",
  ], 114, 378, 430, { size: 18, lineHeight: 36 });
  await image(slide, ctx, assetPath("frontend_screenshots", "web_demo_direct_frozen_replay.png"), 634, 164, 500, 344, "contain", "review-screenshot");
  bodyText(slide, ctx, "The tester remains in the loop through inspection, revision, and rerun.", 640, 542, 490, 26, {
    size: 18,
    color: THEME.body,
    align: "center",
    name: "review-note",
  });
  return slide;
}

export async function buildSlide08(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Risk Analysis for MiniShop Checkout");
  card(slide, ctx, 88, 150, 350, 426, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "risk-method" });
  bodyText(slide, ctx, "Risk scoring method", 116, 178, 240, 22, { size: 16, color: THEME.rose, bold: true, name: "risk-k1" });
  bodyText(slide, ctx, "Risk Priority =\nImpact × Likelihood × Detectability", 116, 220, 290, 86, {
    size: 26,
    color: THEME.ink,
    bold: true,
    face: "Georgia",
    name: "risk-formula",
  });
  divider(slide, ctx, 116, 328, 290);
  bodyText(slide, ctx, "Priority bands", 116, 350, 180, 20, { size: 16, color: THEME.rose, bold: true, name: "risk-k2" });
  bulletList(slide, ctx, [
    "High >= 60",
    "Medium = 36 to 59",
    "Low <= 35",
  ], 116, 382, 260, { size: 19, lineHeight: 42 });
  card(slide, ctx, 478, 150, 710, 426, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "risk-priority" });
  bodyText(slide, ctx, "Highest-risk areas", 510, 178, 220, 22, { size: 16, color: THEME.rose, bold: true, name: "risk-k3" });
  const risks = [
    ["coupon and promotion logic", THEME.blush],
    ["shipping and tax calculation", "#FDEFCF"],
    ["payment-card validation", "#E2F2ED"],
    ["checkout orchestration", "#EDF3FB"],
    ["pickup validation", "#F8F1FF"],
  ];
  risks.forEach((risk, index) => {
    card(slide, ctx, 510, 216 + index * 62, 640, 46, { fill: risk[1], lineColor: THEME.line, lineWidth: 1, name: `risk-row-${index}` });
    bodyText(slide, ctx, risk[0], 528, 228 + index * 62, 606, 20, { size: 19, color: THEME.ink, bold: index < 4, name: `risk-text-${index}` });
  });
  bodyText(slide, ctx, "High risk drives the most detailed test effort and the selected executable module.", 88, 610, 1100, 22, {
    size: 17,
    color: THEME.body,
    align: "center",
    name: "risk-bottom",
  });
  return slide;
}

export async function buildSlide09(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Test Plan: Scope, Architecture, and Test Suites");
  const widths = [326, 326, 326];
  const starts = [88, 477, 866];
  const headings = ["Scope", "Architecture", "Planned Suites"];
  const fills = ["#FFF7F6", "#F9FCFB", "#FFFBF4"];
  const bodies = [
    "Promotion and pricing\nShipping and tax\nPayment validation\nPickup validation\nCheckout orchestration",
    "Checkout Service\nPromotion Service\nShipping Service\nTax Service\nPayment Validation\nPickup Validation",
    "Promotion suite\nShipping and tax suite\nPayment validation suite\nPickup validation suite\nCheckout orchestration suite\nDetailed module suite",
  ];
  headings.forEach((heading, index) => {
    card(slide, ctx, starts[index], 164, widths[index], 404, { fill: fills[index], lineColor: THEME.line, lineWidth: 1.2, name: `plan-card-${index}` });
    bodyText(slide, ctx, heading, starts[index] + 22, 194, 200, 24, { size: 18, color: THEME.rose, bold: true, name: `plan-heading-${index}` });
    bodyText(slide, ctx, bodies[index], starts[index] + 22, 242, widths[index] - 44, 290, {
      size: 22,
      color: THEME.ink,
      name: `plan-body-${index}`,
    });
  });
  bodyText(slide, ctx, "The test plan covers the target application, not the AutoTestDesign tool itself.", 88, 610, 1100, 20, {
    size: 17,
    color: THEME.body,
    align: "center",
    name: "plan-foot",
  });
  return slide;
}

export async function buildSlide10(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Test Plan: Schedule, Team, Framework, and Cost");
  const quads = [
    { x: 88, y: 166, label: "Schedule", fill: "#FFF7F6", body: "freeze target-application scope\ncomplete risk analysis\nreview generated suites\nexecute coupon_discount_engine in detail\npackage evidence and final deliverables" },
    { x: 652, y: 166, label: "Team", fill: "#F9FCFB", body: "integration\ndocument and PPT\nrequirement assets\nmodule execution support\nevaluation and reproducibility" },
    { x: 88, y: 390, label: "Framework", fill: "#FFFBF4", body: "pytest + coverage.py\n\nPython-native\nclear black-box and white-box assertions\neasy integration with coverage" },
    { x: 652, y: 390, label: "Cost", fill: "#F8F3FF", body: "With ARG-Test:\n4.5 to 7.0 person-days\n\nManual baseline:\n7.5 to 10.0 person-days" },
  ];
  quads.forEach((quad, index) => {
    card(slide, ctx, quad.x, quad.y, 460, 180, { fill: quad.fill, lineColor: THEME.line, lineWidth: 1.2, name: `quad-${index}` });
    bodyText(slide, ctx, quad.label, quad.x + 20, quad.y + 18, 180, 22, { size: 18, color: THEME.rose, bold: true, name: `quad-label-${index}` });
    bodyText(slide, ctx, quad.body, quad.x + 20, quad.y + 52, 420, 110, { size: quad.label === "Framework" || quad.label === "Cost" ? 20 : 18, color: THEME.ink, name: `quad-body-${index}` });
  });
  bodyText(slide, ctx, "This slide closes the teacher-required plan items: schedule, team, framework, and cost.", 88, 610, 1100, 20, {
    size: 16,
    color: THEME.muted,
    align: "center",
    name: "plan-reminder",
  });
  return slide;
}

export async function buildSlide11(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Experimental Setup and Evaluation Protocol");
  bodyText(slide, ctx, "Tool-level evaluation on the broader requirement corpus", 88, 116, 1100, 20, {
    size: 16,
    color: THEME.body,
    name: "protocol-note",
  });
  await image(slide, ctx, assetPath("slide_experiment_assets", "slide_experimental_setup_protocol.png"), 72, 146, 1136, 520, "contain", "protocol-image");
  return slide;
}

export async function buildSlide12(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Baselines and Fair Comparison");
  await image(slide, ctx, assetPath("slide_experiment_assets", "slide_baselines_fair_comparison.png"), 72, 140, 1136, 520, "contain", "baseline-fairness");
  bodyText(slide, ctx, "The rule-based baseline is our own deterministic heuristic non-AI baseline.", 88, 612, 1100, 18, {
    size: 16,
    color: THEME.body,
    align: "center",
    name: "baseline-note",
  });
  return slide;
}

export async function buildSlide13(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Main Result Scorecard");
  await image(slide, ctx, assetPath("figures_png", "final_result_scorecard.png"), 84, 146, 790, 500, "contain", "scorecard");
  card(slide, ctx, 914, 206, 232, 286, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "score-side" });
  bodyText(slide, ctx, "Frozen test split summary", 934, 236, 190, 22, { size: 16, color: THEME.rose, bold: true, name: "score-side-kicker" });
  bulletList(slide, ctx, [
    "16 held-out requirements",
    "Avg checker score: 0.959",
    "Avg overall coverage: 0.615",
    "Avg tests: 7.312",
    "0 duplicate cases",
    "9 / 16 high-risk requirements prioritized",
  ], 934, 276, 180, { size: 16, lineHeight: 34 });
  return slide;
}

export async function buildSlide14(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Main Comparison Against Baselines");
  await image(slide, ctx, assetPath("figures_png", "main_vs_baselines.png"), 82, 150, 760, 500, "contain", "baseline-chart");
  card(slide, ctx, 876, 188, 282, 378, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "baseline-summary" });
  bodyText(slide, ctx, "Full ARG-Test outperforms all three baselines on the frozen test split.", 900, 224, 234, 84, {
    size: 22,
    color: THEME.ink,
    face: "Georgia",
    bold: true,
    name: "baseline-lead",
  });
  bulletList(slide, ctx, [
    "Against rule-based: better requirement understanding",
    "Against plain LLM: prompting alone is not enough",
    "Against structured no-checker: checker-guided control adds real value",
  ], 900, 334, 236, { size: 17, lineHeight: 58 });
  return slide;
}

export async function buildSlide15(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Generalization and Ablation");
  await image(slide, ctx, assetPath("figures_png", "generalization_by_category.png"), 78, 154, 520, 350, "contain", "generalization");
  await image(slide, ctx, assetPath("figures_png", "ablation_gain.png"), 654, 154, 530, 350, "contain", "ablation");
  card(slide, ctx, 78, 534, 1106, 84, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.1, name: "gen-bottom" });
  bodyText(slide, ctx, "The method generalizes across business rules, input validation, and workflow-state requirements.", 108, 554, 1000, 24, {
    size: 19,
    color: THEME.ink,
    name: "gen-line-1",
  });
  bodyText(slide, ctx, "Checker-guided control greatly improves checker alignment while keeping coverage and test count comparable.", 108, 582, 1000, 22, {
    size: 18,
    color: THEME.body,
    name: "gen-line-2",
  });
  return slide;
}

export async function buildSlide16(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Representative MiniShop Cases");
  const starts = [74, 452, 830];
  const widths = [338, 338, 378];
  const titles = ["coupon_discount_engine", "pickup_station_contact_validation", "payment_card_expiry_and_cvv_validation"];
  for (let i = 0; i < 3; i += 1) {
    card(slide, ctx, starts[i], 136, widths[i], 500, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.1, name: `case-${i}` });
    bodyText(slide, ctx, titles[i], starts[i] + 16, 164, widths[i] - 32, 44, {
      size: i === 2 ? 20 : 22,
      color: THEME.ink,
      bold: true,
      face: "Georgia",
      name: `case-title-${i}`,
    });
  }
  await image(slide, ctx, assetPath("slide12_case_images", "01_coupon_discount_engine_panel.png"), 88, 214, 308, 388, "contain", "case-img-1");
  await image(slide, ctx, assetPath("slide12_case_images", "02_pickup_station_contact_validation_panel.png"), 466, 214, 308, 388, "contain", "case-img-2");
  labelChip(slide, ctx, "PAYMENT VALIDATION", 850, 214, 154);
  bodyText(slide, ctx, "Core rules", 854, 258, 120, 20, { size: 15, color: THEME.rose, bold: true, name: "payment-core-kicker" });
  bulletList(slide, ctx, [
    "card_number: 13 to 19 digits",
    "expiry_month: 1 to 12",
    "expiry_year: current year to current year + 15",
    "Visa/Mastercard: 3-digit CVV",
    "Amex: 4-digit CVV",
    "Masked numbers are rejected",
  ], 854, 288, 318, { size: 15, lineHeight: 34 });
  divider(slide, ctx, 854, 508, 320);
  bodyText(slide, ctx, "Techniques", 854, 524, 120, 18, { size: 15, color: THEME.rose, bold: true, name: "payment-tech-kicker" });
  bodyText(slide, ctx, "EP + BVA", 854, 552, 200, 24, { size: 20, color: THEME.ink, bold: true, name: "payment-tech" });
  bodyText(slide, ctx, "These cases show that the target application covers business rules and input validation with concrete module boundaries.", 86, 650, 1100, 18, {
    size: 16,
    color: THEME.muted,
    align: "center",
    name: "cases-bottom",
  });
  return slide;
}

export async function buildSlide17(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Detailed Executable Evidence for coupon_discount_engine");
  await image(slide, ctx, assetPath("frontend_screenshots", "coupon_module_evidence_scorecard.png"), 88, 160, 760, 430, "contain", "module-evidence");
  card(slide, ctx, 882, 174, 284, 396, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.2, name: "module-side" });
  bodyText(slide, ctx, "Selected major module of MiniShop Checkout", 906, 204, 236, 42, { size: 18, color: THEME.rose, bold: true, name: "module-kicker" });
  bodyText(slide, ctx, "coupon_discount_engine", 906, 254, 236, 44, { size: 24, color: THEME.ink, face: "Georgia", bold: true, name: "module-name" });
  bulletList(slide, ctx, [
    "15 module tests passed",
    "100% statement coverage",
    "100% branch coverage",
    "4 / 4 mutants killed",
    "Black-box design + white-box execution + mutation usefulness",
  ], 906, 318, 236, { size: 17, lineHeight: 42 });
  bodyText(slide, ctx, "This gives us executable evidence, not only design-level metrics.", 88, 620, 1100, 22, {
    size: 18,
    color: THEME.body,
    align: "center",
    name: "module-foot",
  });
  return slide;
}

export async function buildSlide18(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "", "Reproducibility, NFR, Limitations, and Conclusion");
  await image(slide, ctx, assetPath("figures_png", "reproducibility_stability_overview.png"), 76, 142, 610, 350, "contain", "repro");
  card(slide, ctx, 720, 152, 456, 176, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.1, name: "nfr-card" });
  bodyText(slide, ctx, "NFR snapshot", 744, 174, 160, 22, { size: 16, color: THEME.rose, bold: true, name: "nfr-kicker" });
  bulletList(slide, ctx, [
    "Usability: Direct Input, CSV Batch, State Model, Formal Evidence",
    "Security: no secret leak found in exported artifacts",
    "Maintainability: modular codebase and rerunnable tests",
  ], 744, 206, 396, { size: 15, lineHeight: 42 });
  card(slide, ctx, 720, 346, 456, 132, { fill: "#FFF9F8", lineColor: THEME.line, lineWidth: 1.1, name: "limit-card" });
  bodyText(slide, ctx, "Limitations", 744, 366, 140, 22, { size: 16, color: THEME.rose, bold: true, name: "limit-kicker" });
  bulletList(slide, ctx, [
    "MiniShop Checkout is a compact course-project prototype",
    "Only coupon_discount_engine has full white-box execution evidence",
    "Live providers still show residual nondeterminism",
  ], 744, 398, 394, { size: 14, lineHeight: 30 });
  card(slide, ctx, 76, 520, 1100, 112, { fill: "#FFFFFF", lineColor: THEME.line, lineWidth: 1.1, name: "conclusion-card" });
  bodyText(slide, ctx, "ARG-Test enables auditable, checked, and reproducible requirement-driven testing for a concrete target application.", 104, 548, 1040, 28, {
    size: 23,
    color: THEME.ink,
    face: "Georgia",
    bold: true,
    align: "center",
    name: "conclusion-main",
  });
  bodyText(slide, ctx, "Tool: ARG-Test | Target application: MiniShop Checkout | Selected module: coupon_discount_engine", 104, 588, 1040, 18, {
    size: 15,
    color: THEME.muted,
    align: "center",
    name: "conclusion-sub",
  });
  return slide;
}

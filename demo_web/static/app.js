const textForm = document.getElementById("text-form");
const csvForm = document.getElementById("csv-form");
const stateForm = document.getElementById("state-form");
const formalSummary = document.getElementById("formal-summary");
const textResult = document.getElementById("text-result");
const csvResult = document.getElementById("csv-result");
const stateResult = document.getElementById("state-result");
let requirementCatalog = {
  direct_requirements: [],
  state_requirements: [],
  byId: new Map(),
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function pct(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "n/a";
  }
  return `${(Number(value) * 100).toFixed(1)}%`;
}

function pctOrUnknown(value) {
  return value === null || value === undefined || Number.isNaN(Number(value)) ? "coverage n/a" : pct(value);
}

function num(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "n/a";
  }
  return Number(value).toFixed(3);
}

function titleCase(value) {
  return String(value || "n/a")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function activateTab(panelId) {
  document.querySelectorAll(".nav-tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.tabTarget === panelId);
  });
  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === panelId);
  });
}

document.querySelectorAll(".nav-tab").forEach((button) => {
  button.addEventListener("click", () => activateTab(button.dataset.tabTarget));
});

document.getElementById("text-requirement-id").addEventListener("change", () => {
  applyRequirementSelection("text-requirement-id", "text-requirement", "text-split");
  setStatus("text-status", "Selected requirement loaded.");
  resetDirectPreview();
});

document.getElementById("state-requirement-id").addEventListener("change", () => {
  applyRequirementSelection("state-requirement-id", "state-requirement", "state-split");
  setStatus("state-status", "Selected workflow loaded.");
  resetStatePreview();
});

function setStatus(id, message) {
  document.getElementById(id).textContent = message;
}

function resetDirectPreview() {
  textResult.classList.add("empty-state");
  textResult.innerHTML = `
    <h3>Run the direct input demo</h3>
    <p>The selected frozen requirement has been loaded. Generate to inspect checker score, coverage, risk, cases, and artifacts.</p>
  `;
}

function resetStatePreview() {
  stateResult.classList.add("empty-state");
  stateResult.innerHTML = `
    <h3>Build the workflow model</h3>
    <p>The selected workflow requirement has been loaded. Build to inspect states, transitions, coverage plans, and artifacts.</p>
  `;
}

function buildRequirementLabel(item) {
  const category = item.category ? titleCase(item.category) : "Unknown";
  return `${item.requirement_id} | ${category} | ${pctOrUnknown(item.overall_coverage)}`;
}

function populateRequirementSelect(selectId, items, preferredId) {
  const select = document.getElementById(selectId);
  const selectedId = items.some((item) => item.requirement_id === preferredId)
    ? preferredId
    : items[0]?.requirement_id;
  select.innerHTML = "";
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.requirement_id;
    option.textContent = buildRequirementLabel(item);
    option.selected = item.requirement_id === selectedId;
    select.appendChild(option);
  });
}

function applyRequirementSelection(selectId, textareaId, splitId) {
  const select = document.getElementById(selectId);
  const item = requirementCatalog.byId.get(select.value);
  if (!item) {
    return;
  }
  document.getElementById(textareaId).value = item.requirement_text || "";
  document.getElementById(splitId).value = item.split || "test";
}

async function loadDemoRequirements() {
  try {
    const response = await fetch("/api/demo-requirements");
    if (!response.ok) {
      throw new Error("Failed to load demo requirement catalog.");
    }
    const payload = await response.json();
    const directRequirements = payload.direct_requirements || [];
    const stateRequirements = payload.state_requirements || [];
    requirementCatalog = {
      direct_requirements: directRequirements,
      state_requirements: stateRequirements,
      byId: new Map([...directRequirements, ...stateRequirements].map((item) => [item.requirement_id, item])),
    };
    if (directRequirements.length) {
      populateRequirementSelect("text-requirement-id", directRequirements, "pickup_station_contact_validation");
      applyRequirementSelection("text-requirement-id", "text-requirement", "text-split");
    }
    if (stateRequirements.length) {
      populateRequirementSelect("state-requirement-id", stateRequirements, "warehouse_pickup_order_workflow");
      applyRequirementSelection("state-requirement-id", "state-requirement", "state-split");
    }
  } catch (error) {
    setStatus("text-status", "Catalog fallback loaded.");
    setStatus("state-status", "Catalog fallback loaded.");
  }
}

function renderMetricGrid(items, primaryIndex = -1) {
  return `
    <div class="metric-grid">
      ${items.map((item, index) => {
        const rawValue = String(item.value ?? "");
        const denseValue = rawValue.length > 18 || rawValue.includes("\\") || rawValue.includes("/");
        return `
        <div class="metric-card ${index === primaryIndex ? "primary" : ""} ${denseValue ? "dense" : ""}">
          <span class="metric-label">${escapeHtml(item.label)}</span>
          <strong class="metric-value">${escapeHtml(item.value)}</strong>
          <small class="metric-footnote">${escapeHtml(item.note || "")}</small>
        </div>
      `;
      }).join("")}
    </div>
  `;
}

function renderRiskBlock(risk) {
  if (!risk) {
    return "";
  }
  return `
    <div class="panel-card">
      <h3>Risk Assessment</h3>
      ${renderMetricGrid([
        { label: "Risk Level", value: risk.level, note: "Priority signal for generated cases" },
        { label: "Risk Score", value: num(risk.score), note: `${risk.rule_count} rules, ${risk.numeric_constraint_count} numeric constraints` },
      ])}
      <div class="two-column">
        <div class="panel-card">
          <h3>Drivers</h3>
          <div class="chip-row">${(risk.drivers || []).map((item) => `<span class="chip signal">${escapeHtml(item)}</span>`).join("")}</div>
        </div>
        <div class="panel-card">
          <h3>Recommended Focus</h3>
          <div class="chip-row">${(risk.recommended_focus || []).map((item) => `<span class="chip">${escapeHtml(item)}</span>`).join("")}</div>
        </div>
      </div>
    </div>
  `;
}

function renderTestCases(testCases) {
  if (!testCases || !testCases.length) {
    return "";
  }
  return `
    <div class="table-card">
      <h3>Generated Test Cases</h3>
      <div class="case-grid">
        ${testCases.map((item) => `
          <article class="case-card">
            <div class="case-meta">
              <span class="chip">${escapeHtml(item.test_id)}</span>
              <span class="chip">${escapeHtml(item.technique)}</span>
              ${item.priority ? `<span class="chip signal">${escapeHtml(item.priority)}</span>` : ""}
            </div>
            <p><strong>Input:</strong> ${escapeHtml(item.input)}</p>
            <p><strong>Expected:</strong> ${escapeHtml(item.expected_output)}</p>
          </article>
        `).join("")}
      </div>
    </div>
  `;
}

function renderArtifactPaths(paths) {
  const entries = Object.entries(paths || {}).filter(([, value]) => value);
  if (!entries.length) {
    return "";
  }
  return `
    <div class="panel-card">
      <h3>Artifact Paths</h3>
      <ul class="artifact-list">
        ${entries.map(([key, value]) => `<li><strong>${escapeHtml(key)}:</strong> <code>${escapeHtml(value)}</code></li>`).join("")}
      </ul>
    </div>
  `;
}

function renderDirectResult(payload) {
  const summary = payload.summary || {};
  const parsed = payload.parsed_trace || {};
  const metrics = summary.metrics || {};
  const goldSpecFound = Boolean(metrics.gold_spec_found);
  const categoryLabel = summary.category || (summary.split === "adhoc" ? "adhoc demo input" : "dataset category unavailable");
  const frozenReplay = payload.replay_source === "frozen_formal_run" || summary.demo_mode === "frozen_formal_replay";
  const modeMetric = frozenReplay
    ? { label: "Run Mode", value: "Replay", note: "Frozen formal output" }
    : { label: "Selected Candidate", value: summary.candidate_index || "n/a", note: summary.repaired ? "Repaired version accepted" : "Original candidate kept" };
  textResult.classList.remove("empty-state");
  textResult.innerHTML = `
    ${renderMetricGrid([
      { label: "Structural Checker", value: num(summary.score), note: `Contract checks; category: ${categoryLabel}` },
      { label: "Overall Coverage", value: goldSpecFound ? pct(metrics.overall_coverage) : "N/A", note: frozenReplay ? `${metrics.test_count || 0} frozen test cases` : goldSpecFound ? `${metrics.test_count || 0} generated test cases` : "No gold spec for this live input" },
      modeMetric,
      { label: "Requirement", value: summary.requirement_id || "n/a", note: summary.split || "n/a" },
    ], 0)}
    ${frozenReplay ? `
      <div class="panel-card">
        <h3>Result Source</h3>
        <div class="chip-row">
          <span class="chip signal">Frozen formal replay</span>
          <span class="chip">Matches Formal Evidence coverage</span>
          <span class="chip">No live API call</span>
        </div>
      </div>
    ` : ""}
    ${renderRiskBlock(summary.risk_assessment)}
    <div class="panel-card">
      <h3>Diagnostics</h3>
      <ul class="plain-list">${(summary.diagnostics || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </div>
    ${renderTestCases(parsed.test_cases || [])}
    ${renderArtifactPaths(payload.artifact_paths || {})}
  `;
}

function renderTransitionTable(title, rows) {
  return `
    <div class="table-card">
      <h3>${escapeHtml(title)}</h3>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Source</th><th>Trigger</th><th>Target</th></tr></thead>
          <tbody>
            ${(rows || []).map((item) => `
              <tr>
                <td>${escapeHtml(item.source_state)}</td>
                <td>${escapeHtml(item.trigger)}</td>
                <td>${escapeHtml(item.target_state)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderStateModel(payload) {
  const summary = payload.summary || {};
  const stateModel = payload.state_model_only || summary.state_model || {};
  const legalTransitions = stateModel.legal_transitions || [];
  const illegalTransitions = stateModel.illegal_transitions || [];
  const coveragePlans = stateModel.coverage_plans || [];
  stateResult.classList.remove("empty-state");
  stateResult.innerHTML = `
    ${renderMetricGrid([
      { label: "States", value: (stateModel.states || []).length, note: (stateModel.states || []).join(", ") || "n/a" },
      { label: "Legal Transitions", value: legalTransitions.length, note: legalTransitions.length ? "Derived from requirement rules" : "No legal transition extracted" },
      { label: "Illegal Transitions", value: illegalTransitions.length, note: illegalTransitions.length ? "Negative workflow tests" : "No explicit illegal rule" },
      { label: "Coverage Plans", value: coveragePlans.length, note: "All-states / all-transitions" },
    ], 0)}
    ${renderRiskBlock(summary.risk_assessment)}
    <div class="two-column">
      ${renderTransitionTable("Legal Transitions", legalTransitions)}
      ${renderTransitionTable("Illegal Transitions", illegalTransitions)}
    </div>
    <div class="result-list">
      ${coveragePlans.map((plan) => `
        <div class="result-card">
          <h3>${escapeHtml(plan.coverage_goal)}</h3>
          <p>${escapeHtml(String(plan.sequence_count))} sequences. Fully covered: ${escapeHtml(String(plan.fully_covered))}</p>
        </div>
      `).join("")}
    </div>
    ${renderArtifactPaths(payload.artifact_paths || {})}
  `;
}

function renderCsvBatch(payload) {
  const records = payload.records || [];
  csvResult.classList.remove("empty-state");
  csvResult.innerHTML = `
    ${renderMetricGrid([
      { label: "Batch Size", value: payload.batch_size || 0, note: "Requirements processed from CSV upload" },
      { label: "Artifact Root", value: payload.artifact_root || "n/a", note: payload.uploaded_file || "" },
    ], 0)}
    <div class="result-list">
      ${records.map((record) => {
        const summary = record.summary || {};
        const metrics = summary.metrics || {};
        const goldSpecFound = Boolean(metrics.gold_spec_found);
        const frozenReplay = record.replay_source === "frozen_formal_run" || summary.demo_mode === "frozen_formal_replay";
        return `
          <div class="result-card">
            <h3>${escapeHtml(summary.requirement_id || "unknown requirement")}</h3>
            <div class="chip-row">
              <span class="chip">${escapeHtml(summary.category || "n/a")}</span>
              <span class="chip">Structural ${escapeHtml(num(summary.score))}</span>
              <span class="chip">${escapeHtml(goldSpecFound ? pct(metrics.overall_coverage) : "N/A coverage")}</span>
              ${frozenReplay ? `<span class="chip signal">Frozen replay</span>` : `<span class="chip">Mock generated</span>`}
              <span class="chip signal">Risk ${(escapeHtml((summary.risk_assessment || {}).level || "n/a"))}</span>
            </div>
            ${goldSpecFound ? "" : "<p>This row has no gold spec. Official coverage should be interpreted from the frozen dashboard, not from an ad hoc live input.</p>"}
          </div>
        `;
      }).join("")}
    </div>
  `;
}

function renderSmallTable(title, headers, rows) {
  return `
    <div class="table-card">
      <h3>${escapeHtml(title)}</h3>
      <div class="table-wrap">
        <table>
          <thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr></thead>
          <tbody>${rows.join("")}</tbody>
        </table>
      </div>
    </div>
  `;
}

function renderFormalEvidence(payload) {
  const official = payload.official_run || {};
  const baselineRows = Object.entries(payload.baseline_averages || {}).map(([name, value]) => `
    <tr>
      <td>${escapeHtml(titleCase(name))}</td>
      <td>${escapeHtml(num(value.avg_checker_score))}</td>
      <td>${escapeHtml(pct(value.avg_overall_coverage))}</td>
      <td>${escapeHtml(num(value.avg_test_count))}</td>
    </tr>
  `);
  const categoryRows = (payload.generalization || []).map((row) => `
    <tr>
      <td>${escapeHtml(row.category)}</td>
      <td>${escapeHtml(row.requirement_count)}</td>
      <td>${escapeHtml(num(row.avg_checker_score))}</td>
      <td>${escapeHtml(pct(row.avg_overall_coverage))}</td>
    </tr>
  `);
  const reproducibilityRows = (payload.reproducibility || []).map((row) => `
    <tr>
      <td>${escapeHtml(row.label)}</td>
      <td>${escapeHtml(pct(row.stable_rate))}</td>
      <td>${escapeHtml(num(row.avg_max_score_delta))}</td>
      <td>${escapeHtml(num(row.avg_max_coverage_delta))}</td>
    </tr>
  `);

  formalSummary.classList.remove("loading-block");
  formalSummary.innerHTML = `
    <div class="dashboard-grid">
      <div class="panel-card">
        <h3>Tracked Formal Data Source</h3>
        <p><code>${escapeHtml(payload.formal_report_source || "n/a")}</code></p>
      </div>
      ${renderMetricGrid([
        { label: "Official Test Requirements", value: official.requirement_count, note: "Frozen held-out split" },
        { label: "Avg Structural Checker", value: num(official.avg_checker_score), note: "Contract-level checks" },
        { label: "Avg Overall Coverage", value: pct(official.avg_overall_coverage), note: "Against gold specs" },
        { label: "Avg Test Count", value: num(official.avg_test_count), note: `${official.high_risk_count} high-risk requirements` },
      ], 2)}
    </div>

    <div class="two-column">
      ${renderSmallTable("Baselines", ["Method", "Structural", "Coverage", "Tests"], baselineRows)}
      ${renderSmallTable("Category Generalization", ["Category", "Count", "Structural", "Coverage"], categoryRows)}
    </div>

    <div class="two-column">
      ${renderSmallTable("Reproducibility Snapshot", ["Run", "Stable Rate", "Score Delta", "Coverage Delta"], reproducibilityRows)}
      <div class="panel-card">
        <h3>Recommended Cases for PPT and Demo</h3>
        <div class="chip-row">
          ${(payload.recommended_cases || []).map((row) => `<span class="chip">${escapeHtml(row.requirement_id)} - ${escapeHtml(row.category)} - ${escapeHtml(pct(row.overall_coverage))}</span>`).join("")}
        </div>
      </div>
    </div>

    <div class="figure-grid">
      ${(payload.figure_gallery || []).map((figure) => `
        <div class="figure-card">
          <img src="${escapeHtml(figure.url)}" alt="${escapeHtml(figure.title)}">
          <h3>${escapeHtml(figure.title)}</h3>
          <p>${escapeHtml(figure.caption)}</p>
        </div>
      `).join("")}
    </div>
  `;
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: "Request failed." }));
    throw new Error(payload.detail || "Request failed.");
  }
  return response.json();
}

async function runDirectAnalysis() {
  setStatus("text-status", "Running...");
  textResult.classList.remove("empty-state");
  textResult.innerHTML = `<div class="loading-block">Generating structured test suite...</div>`;
  try {
    const payload = await postJson("/api/analyze-text", {
      requirement_id: document.getElementById("text-requirement-id").value,
      split: document.getElementById("text-split").value,
      provider: document.getElementById("text-provider").value,
      model: document.getElementById("text-model").value,
      candidates: Number(document.getElementById("text-candidates").value),
      seed: Number(document.getElementById("text-seed").value),
      requirement_text: document.getElementById("text-requirement").value,
    });
    renderDirectResult(payload);
    setStatus("text-status", "Completed.");
  } catch (error) {
    textResult.innerHTML = `<div class="panel-card"><p>${escapeHtml(error.message)}</p></div>`;
    setStatus("text-status", "Failed.");
  }
}

async function runStateModelAnalysis() {
  setStatus("state-status", "Running...");
  stateResult.classList.remove("empty-state");
  stateResult.innerHTML = `<div class="loading-block">Building state model...</div>`;
  try {
    const payload = await postJson("/api/state-model", {
      requirement_id: document.getElementById("state-requirement-id").value,
      split: document.getElementById("state-split").value,
      provider: document.getElementById("state-provider").value,
      model: document.getElementById("state-model-name").value,
      requirement_text: document.getElementById("state-requirement").value,
      candidates: 3,
      seed: 202601,
    });
    renderStateModel(payload);
    setStatus("state-status", "Completed.");
  } catch (error) {
    stateResult.innerHTML = `<div class="panel-card"><p>${escapeHtml(error.message)}</p></div>`;
    setStatus("state-status", "Failed.");
  }
}

async function runCsvAnalysis() {
  setStatus("csv-status", "Running...");
  csvResult.classList.remove("empty-state");
  csvResult.innerHTML = `<div class="loading-block">Running CSV batch...</div>`;
  const fileInput = document.getElementById("csv-file");
  if (!fileInput.files.length) {
    csvResult.innerHTML = `<div class="panel-card"><p>Please choose a CSV file first.</p></div>`;
    setStatus("csv-status", "Please choose a CSV file.");
    return;
  }
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("provider", document.getElementById("csv-provider").value);
  formData.append("model", document.getElementById("csv-model").value);
  formData.append("candidates", document.getElementById("csv-candidates").value);
  try {
    const response = await fetch("/api/analyze-csv", { method: "POST", body: formData });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({ detail: "Request failed." }));
      throw new Error(payload.detail || "Request failed.");
    }
    const payload = await response.json();
    renderCsvBatch(payload);
    setStatus("csv-status", "Completed.");
  } catch (error) {
    csvResult.innerHTML = `<div class="panel-card"><p>${escapeHtml(error.message)}</p></div>`;
    setStatus("csv-status", "Failed.");
  }
}

textForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await runDirectAnalysis();
});

stateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await runStateModelAnalysis();
});

csvForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  await runCsvAnalysis();
});

document.getElementById("download-sample-csv").addEventListener("click", () => {
  window.open("/api/sample-csv", "_blank");
});

async function loadFormalSummary() {
  try {
    const response = await fetch("/api/formal-summary");
    const payload = await response.json();
    renderFormalEvidence(payload);
  } catch (error) {
    formalSummary.innerHTML = `<div class="panel-card"><p>${escapeHtml(error.message)}</p></div>`;
  }
}

async function maybeAutorun() {
  const params = new URLSearchParams(window.location.search);
  const autorun = params.get("autorun");
  const focus = params.get("focus");
  const focusMap = {
    direct: "direct-panel",
    csv: "csv-panel",
    state: "state-panel",
    formal: "formal-panel",
  };

  if (focusMap[focus]) {
    activateTab(focusMap[focus]);
  }

  if (autorun === "direct") {
    activateTab("direct-panel");
    setStatus("text-status", "Auto-running...");
    await runDirectAnalysis();
  } else if (autorun === "state") {
    activateTab("state-panel");
    setStatus("state-status", "Auto-running...");
    await runStateModelAnalysis();
  } else if (autorun === "csv") {
    activateTab("csv-panel");
    setStatus("csv-status", "Choose a CSV file to continue.");
  }
}

async function initializePage() {
  await Promise.all([loadFormalSummary(), loadDemoRequirements()]);
  await maybeAutorun();
}

initializePage();

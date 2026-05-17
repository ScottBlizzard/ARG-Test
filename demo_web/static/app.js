const textForm = document.getElementById("text-form");
const csvForm = document.getElementById("csv-form");
const stateForm = document.getElementById("state-form");
const formalSummary = document.getElementById("formal-summary");
const textResult = document.getElementById("text-result");
const csvResult = document.getElementById("csv-result");
const stateResult = document.getElementById("state-result");

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

function num(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "n/a";
  }
  return Number(value).toFixed(3);
}

function setStatus(id, message) {
  document.getElementById(id).textContent = message;
}

function renderMetricGrid(items) {
  return `
    <div class="metric-grid">
      ${items.map((item) => `
        <div class="metric-card">
          <span class="metric-label">${escapeHtml(item.label)}</span>
          <strong class="metric-value">${escapeHtml(item.value)}</strong>
          <small class="metric-footnote">${escapeHtml(item.note || "")}</small>
        </div>
      `).join("")}
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

function renderTestCaseTable(testCases) {
  if (!testCases || !testCases.length) {
    return "";
  }
  return `
    <div class="table-card">
      <h3>Generated Test Cases</h3>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Test ID</th>
              <th>Technique</th>
              <th>Input</th>
              <th>Expected Output</th>
              <th>Priority</th>
            </tr>
          </thead>
          <tbody>
            ${testCases.map((item) => `
              <tr>
                <td>${escapeHtml(item.test_id)}</td>
                <td>${escapeHtml(item.technique)}</td>
                <td>${escapeHtml(item.input)}</td>
                <td>${escapeHtml(item.expected_output)}</td>
                <td>${escapeHtml(item.priority || "")}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderArtifactPaths(paths) {
  return `
    <div class="panel-card">
      <h3>Artifact Paths</h3>
      <ul class="artifact-list">
        ${Object.entries(paths || {})
          .filter(([, value]) => value)
          .map(([key, value]) => `<li><strong>${escapeHtml(key)}:</strong> <code>${escapeHtml(value)}</code></li>`)
          .join("")}
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
  textResult.innerHTML = `
    ${renderMetricGrid([
      { label: "Checker Score", value: num(summary.score), note: `Category: ${categoryLabel}` },
      { label: "Overall Coverage", value: goldSpecFound ? pct(metrics.overall_coverage) : "N/A", note: goldSpecFound ? `${metrics.test_count || 0} test cases` : "No gold spec for this live input. Use the Formal Evidence Dashboard for official coverage." },
      { label: "Selected Candidate", value: summary.candidate_index || "n/a", note: summary.repaired ? "Repaired version accepted" : "Original candidate kept" },
    ])}
    ${renderRiskBlock(summary.risk_assessment)}
    <div class="panel-card">
      <h3>Diagnostics</h3>
      <ul class="plain-list">${(summary.diagnostics || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </div>
    ${renderTestCaseTable(parsed.test_cases || [])}
    ${renderArtifactPaths(payload.artifact_paths || {})}
  `;
}

function renderStateModel(payload) {
  const summary = payload.summary || {};
  const stateModel = payload.state_model_only || summary.state_model || {};
  const legalTransitions = stateModel.legal_transitions || [];
  const illegalTransitions = stateModel.illegal_transitions || [];
  const coveragePlans = stateModel.coverage_plans || [];
  stateResult.innerHTML = `
    ${renderMetricGrid([
      { label: "States", value: (stateModel.states || []).length, note: (stateModel.states || []).join(", ") || "n/a" },
      { label: "Legal Transitions", value: legalTransitions.length, note: "Derived from requirement rules" },
      { label: "Illegal Transitions", value: illegalTransitions.length, note: "Useful for negative workflow tests" },
    ])}
    ${renderRiskBlock(summary.risk_assessment)}
    <div class="two-column">
      <div class="table-card">
        <h3>Legal Transitions</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Source</th><th>Trigger</th><th>Target</th></tr></thead>
            <tbody>
              ${legalTransitions.map((item) => `<tr><td>${escapeHtml(item.source_state)}</td><td>${escapeHtml(item.trigger)}</td><td>${escapeHtml(item.target_state)}</td></tr>`).join("")}
            </tbody>
          </table>
        </div>
      </div>
      <div class="table-card">
        <h3>Illegal Transitions</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Source</th><th>Trigger</th><th>Target</th></tr></thead>
            <tbody>
              ${illegalTransitions.map((item) => `<tr><td>${escapeHtml(item.source_state)}</td><td>${escapeHtml(item.trigger)}</td><td>${escapeHtml(item.target_state)}</td></tr>`).join("")}
            </tbody>
          </table>
        </div>
      </div>
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
  csvResult.innerHTML = `
    ${renderMetricGrid([
      { label: "Batch Size", value: payload.batch_size || 0, note: "Requirements processed from CSV upload" },
      { label: "Artifact Root", value: payload.artifact_root || "n/a", note: payload.uploaded_file || "" },
    ])}
    <div class="result-list">
      ${records.map((record) => {
        const summary = record.summary || {};
        const metrics = summary.metrics || {};
        const goldSpecFound = Boolean(metrics.gold_spec_found);
        return `
          <div class="result-card">
            <h3>${escapeHtml(summary.requirement_id || "unknown requirement")}</h3>
            <p>
              Category: <strong>${escapeHtml(summary.category || "n/a")}</strong> |
              Checker: <strong>${escapeHtml(num(summary.score))}</strong> |
              Coverage: <strong>${escapeHtml(goldSpecFound ? pct(metrics.overall_coverage) : "N/A")}</strong> |
              Risk: <strong>${escapeHtml((summary.risk_assessment || {}).level || "n/a")}</strong>
            </p>
            ${goldSpecFound ? "" : "<p>This row has no gold spec. Official coverage should be interpreted from the frozen dashboard, not from an adhoc live input.</p>"}
          </div>
        `;
      }).join("")}
    </div>
  `;
}

function renderFormalEvidence(payload) {
  formalSummary.innerHTML = `
    <div class="panel-card">
      <h3>Tracked Formal Data Source</h3>
      <p><code>${escapeHtml(payload.formal_report_source || "n/a")}</code></p>
    </div>
    ${renderMetricGrid([
      { label: "Official Test Requirements", value: payload.official_run.requirement_count, note: "Frozen held-out split" },
      { label: "Avg Checker Score", value: num(payload.official_run.avg_checker_score), note: "Main pipeline" },
      { label: "Avg Overall Coverage", value: pct(payload.official_run.avg_overall_coverage), note: "Against gold specs" },
      { label: "Avg Test Count", value: num(payload.official_run.avg_test_count), note: `${payload.official_run.high_risk_count} high-risk requirements` },
    ])}
    <div class="compact-grid">
      ${Object.entries(payload.baseline_averages || {}).map(([name, value]) => `
        <div class="panel-card">
          <h3>${escapeHtml(name)}</h3>
          <p>Checker: <strong>${escapeHtml(num(value.avg_checker_score))}</strong></p>
          <p>Coverage: <strong>${escapeHtml(pct(value.avg_overall_coverage))}</strong></p>
          <p>Avg tests: <strong>${escapeHtml(num(value.avg_test_count))}</strong></p>
        </div>
      `).join("")}
    </div>
    <div class="two-column">
      <div class="table-card">
        <h3>Category Generalization</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Category</th><th>Count</th><th>Checker</th><th>Coverage</th></tr></thead>
            <tbody>
              ${(payload.generalization || []).map((row) => `
                <tr>
                  <td>${escapeHtml(row.category)}</td>
                  <td>${escapeHtml(row.requirement_count)}</td>
                  <td>${escapeHtml(num(row.avg_checker_score))}</td>
                  <td>${escapeHtml(pct(row.avg_overall_coverage))}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
      <div class="table-card">
        <h3>Reproducibility Snapshot</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Run</th><th>Stable Rate</th><th>Score Delta</th><th>Coverage Delta</th></tr></thead>
            <tbody>
              ${(payload.reproducibility || []).map((row) => `
                <tr>
                  <td>${escapeHtml(row.label)}</td>
                  <td>${escapeHtml(pct(row.stable_rate))}</td>
                  <td>${escapeHtml(num(row.avg_max_score_delta))}</td>
                  <td>${escapeHtml(num(row.avg_max_coverage_delta))}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="panel-card">
      <h3>Recommended Cases for PPT and Demo</h3>
      <div class="chip-row">${(payload.recommended_cases || []).map((row) => `<span class="chip">${escapeHtml(row.requirement_id)} · ${escapeHtml(row.category)} · ${escapeHtml(pct(row.overall_coverage))}</span>`).join("")}</div>
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

textForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("text-status", "Running...");
  textResult.innerHTML = "";
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
});

stateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("state-status", "Running...");
  stateResult.innerHTML = "";
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
});

csvForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("csv-status", "Running...");
  csvResult.innerHTML = "";
  const fileInput = document.getElementById("csv-file");
  if (!fileInput.files.length) {
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

loadFormalSummary();

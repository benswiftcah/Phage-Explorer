const STAGE_LABELS = {
  queued: "Queued",
  fetching_genome: "Fetching genome",
  qc: "Quality checks",
  gene_calling: "Calling genes",
  functional_annotation: "Functional annotation",
  taxonomy_classification: "Taxonomy classification",
  host_prediction: "Host prediction",
  lifestyle_prediction: "Lifestyle prediction",
  done: "Done",
};

let selectedFile = null;
let pollTimer = null;

// ---------- Tabs (input panel) ----------
document.querySelectorAll(".sidebar .tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".sidebar .tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".sidebar .tab-panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    document.querySelector(`.tab-panel[data-panel="${tab.dataset.tab}"]`).classList.add("active");
  });
});

// ---------- Tabs (results panel) ----------
document.querySelectorAll(".results-tabs .tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".results-tabs .tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".result-panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    document.querySelector(`.result-panel[data-rpanel="${tab.dataset.rtab}"]`).classList.add("active");
  });
});

// ---------- Dropzone ----------
const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fasta-file");
const filenameLabel = document.getElementById("dropzone-filename");

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) {
    selectedFile = fileInput.files[0];
    filenameLabel.textContent = selectedFile.name;
  }
});

["dragover", "dragleave", "drop"].forEach((evt) => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.toggle("drag-over", evt === "dragover");
  });
});

dropzone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) {
    selectedFile = file;
    filenameLabel.textContent = file.name;
  }
});

document.getElementById("use-sample").addEventListener("click", () => {
  // Enterobacteria phage lambda (NC_001416.1) -- the classic, best-studied
  // temperate phage. Fetched live from NCBI via the existing accession
  // path rather than bundling a static sequence, so it's always the real,
  // authoritative record.
  document.querySelector('.sidebar .tab[data-tab="accession"]').click();
  const input = document.getElementById("accession-input");
  input.value = "NC_001416.1";
  document.getElementById("accession-form").requestSubmit();
});

// ---------- Form submission ----------
document.getElementById("upload-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!selectedFile) {
    alert("Choose a FASTA file first (or click 'Use sample genome instead').");
    return;
  }
  const formData = new FormData();
  formData.append("file", selectedFile);
  await startJob(formData, selectedFile.name);
});

document.getElementById("accession-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const accession = document.getElementById("accession-input").value.trim();
  if (!accession) return;
  const formData = new FormData();
  formData.append("accession", accession);
  await startJob(formData, accession);
});

document.getElementById("error-dismiss").addEventListener("click", () => {
  showState("empty");
});

async function startJob(formData, label) {
  showState("progress");
  document.getElementById("progress-genome-name").textContent = `Processing — ${label}`;
  buildStageList("queued");

  const resp = await fetch("/api/jobs", { method: "POST", body: formData });
  const data = await resp.json();
  if (!data.job_id) {
    showError("Could not start the job.");
    return;
  }
  pollJob(data.job_id);
}

function pollJob(jobId) {
  clearInterval(pollTimer);
  pollTimer = setInterval(async () => {
    const resp = await fetch(`/api/jobs/${jobId}`);
    if (!resp.ok) {
      clearInterval(pollTimer);
      showError("Lost track of the job.");
      return;
    }
    const job = await resp.json();
    updateProgress(job);

    if (job.status === "error") {
      clearInterval(pollTimer);
      showError(job.error || "Something went wrong during analysis.");
    } else if (job.status === "done") {
      clearInterval(pollTimer);
      const resultsResp = await fetch(`/api/jobs/${jobId}/results`);
      const results = await resultsResp.json();
      renderResults(results);
      showState("results");
    }
  }, 1200);
}

function updateProgress(job) {
  buildStageList(job.status);
  const lastLog = job.log[job.log.length - 1];
  document.getElementById("progress-message").textContent = lastLog
    ? lastLog.message
    : "Working…";

  const track = document.getElementById("progress-track");
  track.innerHTML = "";
  job.stages.forEach((stage, i) => {
    const el = document.createElement("div");
    el.className = "progress-step";
    if (i < job.stage_index) el.classList.add("done");
    if (i === job.stage_index) el.classList.add("active");
    track.appendChild(el);
  });
}

function buildStageList(currentStage) {
  const list = document.getElementById("stage-list");
  const stages = Object.keys(STAGE_LABELS);
  const currentIndex = stages.indexOf(currentStage);
  list.innerHTML = "";
  stages.forEach((stage, i) => {
    const li = document.createElement("li");
    if (i < currentIndex) li.classList.add("done");
    if (i === currentIndex) li.classList.add("active");
    li.innerHTML = `<span class="dot"></span> ${STAGE_LABELS[stage]}`;
    list.appendChild(li);
  });
}

function showState(state) {
  ["empty", "progress", "error", "results"].forEach((s) => {
    document.getElementById(`${s}-state`).classList.toggle("hidden", s !== state);
  });
}

function showError(message) {
  document.getElementById("error-message").textContent = message;
  showState("error");
}

// ---------- Results rendering ----------
function renderResults(results) {
  const g = results.genome;

  document.getElementById("overview-cards").innerHTML = `
    <div class="overview-card"><p class="label">Accession</p><p class="value" style="font-size:16px">${escapeHtml(g.accession)}</p></div>
    <div class="overview-card"><p class="label">Length</p><p class="value">${g.length_bp.toLocaleString()} bp</p></div>
    <div class="overview-card"><p class="label">GC content</p><p class="value">${g.gc_content_pct}%</p></div>
    <div class="overview-card"><p class="label">Genes called</p><p class="value">${g.gene_count}</p></div>
  `;

  renderGenomeMap(results.genes, g.length_bp);
  renderGenesTable(results.genes, results.functional_annotation.annotations);
  renderPlaceholderCard("taxonomy-card", results.taxonomy, [
    ["Predicted family", results.taxonomy.predicted_family],
    ["Predicted genus", results.taxonomy.predicted_genus],
    ["Closest reference", results.taxonomy.closest_reference],
  ]);
  renderPlaceholderCard("host-card", results.host_prediction, [
    ["Predicted host genus", results.host_prediction.predicted_host_genus],
    ["Predicted host species", results.host_prediction.predicted_host_species],
    ["Method", results.host_prediction.method],
  ]);
  renderLifestyleCard(results.lifestyle_prediction);
}

function renderLifestyleCard(data) {
  const el = document.getElementById("lifestyle-card");
  if (data.is_placeholder) {
    renderPlaceholderCard("lifestyle-card", data, [
      ["Prediction", data.prediction],
      ["Lytic probability", data.lytic_probability],
      ["Temperate probability", data.temperate_probability],
    ]);
    return;
  }
  const lyticPct = (data.lytic_probability * 100).toFixed(1) + "%";
  const tempPct = (data.temperate_probability * 100).toFixed(1) + "%";
  el.innerHTML = `
    <span class="placeholder-badge" style="background:var(--teal-dim);color:var(--teal)">real result — BACPHLIP</span>
    <p><strong>Prediction:</strong> ${escapeHtml(data.prediction)}</p>
    <p><strong>Lytic (virulent) probability:</strong> ${lyticPct}</p>
    <p><strong>Temperate (lysogenic) probability:</strong> ${tempPct}</p>
    <p class="note">${escapeHtml(data.note || "")}</p>
  `;
}

function renderGenomeMap(genes, genomeLength) {
  const width = Math.max(700, Math.min(1000, genomeLength / 15));
  const height = 130;
  const midY = height / 2;
  const scale = (width - 20) / genomeLength;

  let arrows = "";
  genes.forEach((gene) => {
    const x1 = 10 + gene.start * scale;
    const x2 = 10 + gene.end * scale;
    const w = Math.max(2, x2 - x1);
    const isFwd = gene.strand === "+";
    const y = isFwd ? midY - 22 : midY + 8;
    const color = isFwd ? "var(--teal)" : "var(--amber)";
    arrows += `<rect x="${x1}" y="${y}" width="${w}" height="14" rx="2" fill="${color}" opacity="0.85">
      <title>${escapeHtml(gene.id)}: ${gene.start}-${gene.end} (${gene.strand})</title>
    </rect>`;
  });

  const svg = `
    <svg width="100%" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" style="min-width:700px">
      <line x1="10" y1="${midY}" x2="${width - 10}" y2="${midY}" stroke="var(--border)" stroke-width="2" />
      ${arrows}
    </svg>
  `;
  document.getElementById("genome-map").innerHTML = svg;
}

function renderGenesTable(genes, annotations) {
  const annotationById = Object.fromEntries(annotations.map((a) => [a.gene_id, a]));
  const tbody = document.getElementById("genes-tbody");
  tbody.innerHTML = genes
    .map((gene) => {
      const ann = annotationById[gene.id] || {};
      const strandClass = gene.strand === "+" ? "strand-fwd" : "strand-rev";
      return `<tr>
        <td>${escapeHtml(gene.id)}</td>
        <td>${gene.start}</td>
        <td>${gene.end}</td>
        <td class="${strandClass}">${gene.strand}</td>
        <td>${gene.length_aa}</td>
        <td>${escapeHtml(ann.function || "—")}</td>
      </tr>`;
    })
    .join("");
}

function renderPlaceholderCard(elementId, data, fields) {
  const rows = fields
    .map(([label, value]) => `<p><strong>${label}:</strong> ${value === null || value === undefined ? "—" : escapeHtml(String(value))}</p>`)
    .join("");
  const badge = data.is_placeholder
    ? `<span class="placeholder-badge">not yet wired to a real tool</span>`
    : "";
  document.getElementById(elementId).innerHTML = `
    ${badge}
    ${rows}
    <p class="note">${escapeHtml(data.note || "")}</p>
  `;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

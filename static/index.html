<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Phage Bench — Genome Analysis</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --ink: #10171A;
  --panel: #1A2327;
  --panel-raised: #212C31;
  --paper: #E9F1EF;
  --muted: #7C8E93;
  --teal: #4FD1C5;
  --teal-dim: #2E6E68;
  --amber: #E8A33D;
  --amber-dim: #6B5127;
  --border: #2A363B;
  --danger: #E36B6B;
  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--ink); color: var(--paper); font-family: var(--font-body); min-height: 100vh; }
.app { display: grid; grid-template-columns: 320px 1fr; min-height: 100vh; }
@media (max-width: 860px) { .app { grid-template-columns: 1fr; } }

.sidebar { background: var(--panel); border-right: 1px solid var(--border); padding: 28px 24px; display: flex; flex-direction: column; gap: 24px; }
.brand { display: flex; align-items: center; gap: 12px; }
.brand-mark { font-family: var(--font-display); font-size: 28px; font-weight: 700; color: var(--ink); background: var(--teal); width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.brand-text h1 { font-family: var(--font-display); font-size: 18px; font-weight: 600; margin: 0; letter-spacing: -0.01em; }
.brand-text p { margin: 2px 0 0; font-size: 12px; color: var(--muted); }
.runs-locally { font-size: 11px; color: var(--teal); background: rgba(79,209,197,0.08); border: 1px solid var(--teal-dim); border-radius: 6px; padding: 8px 10px; line-height: 1.5; }

.dropzone { border: 1.5px dashed var(--border); border-radius: 10px; padding: 22px 12px; text-align: center; cursor: pointer; transition: border-color 0.15s, background 0.15s; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.dropzone:hover, .dropzone.drag-over { border-color: var(--teal); background: rgba(79, 209, 197, 0.06); }
.dropzone-icon { font-size: 20px; color: var(--teal); }
.dropzone-label { font-size: 12.5px; color: var(--muted); line-height: 1.5; }
.dropzone-filename { font-family: var(--font-mono); font-size: 12px; color: var(--teal); }

textarea#paste-area { background: var(--ink); border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; color: var(--paper); font-family: var(--font-mono); font-size: 11.5px; width: 100%; min-height: 90px; resize: vertical; }
textarea#paste-area:focus { outline: none; border-color: var(--teal); }
.field-label { font-size: 12px; color: var(--muted); font-weight: 500; margin: 0 0 6px; }

.submit-btn { background: var(--teal); color: #0A1413; border: none; border-radius: 8px; padding: 11px; font-family: var(--font-body); font-weight: 600; font-size: 13.5px; cursor: pointer; transition: background 0.15s; width: 100%; }
.submit-btn:hover { background: #63DBD0; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.link-btn { background: none; border: none; color: var(--teal); font-size: 12px; font-weight: 500; cursor: pointer; padding: 0; text-align: left; text-decoration: underline; text-underline-offset: 2px; }

.sensitivity-row { display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: var(--muted); }
input[type="range"] { width: 100%; accent-color: var(--teal); }

.pipeline-key { margin-top: auto; padding-top: 20px; border-top: 1px solid var(--border); }
.pipeline-key-title { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin: 0 0 10px; }
#stage-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 7px; }
#stage-list li { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--muted); font-family: var(--font-mono); }
#stage-list li .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--border); flex-shrink: 0; }
#stage-list li.done { color: var(--paper); }
#stage-list li.done .dot { background: var(--teal); }
#stage-list li.active { color: var(--teal); }
#stage-list li.active .dot { background: var(--teal); box-shadow: 0 0 0 3px rgba(79,209,197,0.2); }

.main { padding: 40px 48px; max-width: 980px; }
.hidden { display: none !important; }
.eyebrow { font-family: var(--font-mono); font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--teal); margin: 0 0 10px; }
.empty-state h2, .error-state h2 { font-family: var(--font-display); font-size: 26px; font-weight: 600; margin: 0 0 12px; max-width: 520px; }
.muted { color: var(--muted); font-size: 14px; line-height: 1.6; max-width: 560px; }
.error-state h2 { color: var(--danger); }

.progress-track { display: flex; gap: 4px; margin: 18px 0 14px; max-width: 560px; }
.progress-step { flex: 1; height: 6px; border-radius: 3px; background: var(--panel-raised); transition: background 0.3s; }
.progress-step.done { background: var(--teal-dim); }
.progress-step.active { background: var(--teal); }
.progress-message { font-family: var(--font-mono); font-size: 13px; color: var(--muted); }

.overview-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 32px; }
@media (max-width: 700px) { .overview-cards { grid-template-columns: repeat(2, 1fr); } }
.overview-card { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 16px 18px; }
.overview-card .label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin: 0 0 6px; }
.overview-card .value { font-family: var(--font-display); font-size: 22px; font-weight: 600; margin: 0; }

.genome-map-wrap { margin-bottom: 32px; }
.section-label { font-family: var(--font-display); font-size: 14px; font-weight: 600; margin: 0 0 12px; }
.section-label-sub { font-family: var(--font-body); font-weight: 400; color: var(--muted); font-size: 12.5px; }
#genome-map { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 12px; overflow-x: auto; }
.legend { display: flex; gap: 18px; margin-top: 8px; }
.legend-item { font-size: 11.5px; color: var(--muted); display: flex; align-items: center; gap: 6px; }
.swatch { width: 10px; height: 10px; border-radius: 2px; display: inline-block; }
.swatch-fwd { background: var(--teal); }
.swatch-rev { background: var(--amber); }

.tabs { display: flex; border-radius: 8px; background: var(--ink); padding: 3px; gap: 2px; width: fit-content; }
.tab { background: transparent; border: none; color: var(--muted); font-family: var(--font-body); font-size: 12.5px; font-weight: 600; padding: 8px 14px; border-radius: 6px; cursor: pointer; transition: background 0.15s, color 0.15s; }
.tab.active { background: var(--panel-raised); color: var(--paper); }
.results-tabs .tabs { margin-bottom: 18px; }
.result-panel { display: none; }
.result-panel.active { display: block; }

.genes-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.genes-table th { text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); font-weight: 500; padding: 8px 12px; border-bottom: 1px solid var(--border); }
.genes-table td { padding: 9px 12px; border-bottom: 1px solid var(--border); font-family: var(--font-mono); font-size: 12.5px; }
.genes-table tr:hover td { background: var(--panel); }
.strand-fwd { color: var(--teal); }
.strand-rev { color: var(--amber); }
.genes-table-wrap { max-height: 420px; overflow-y: auto; border: 1px solid var(--border); border-radius: 10px; }
.genes-table-wrap .genes-table th { position: sticky; top: 0; background: var(--panel); }

.placeholder-card { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 24px; max-width: 560px; }
.placeholder-badge { display: inline-block; background: var(--amber-dim); color: var(--amber); font-family: var(--font-mono); font-size: 11px; padding: 3px 8px; border-radius: 5px; margin-bottom: 12px; }
.placeholder-card p { font-size: 13.5px; line-height: 1.6; color: var(--paper); margin: 0 0 8px; }
.placeholder-card p.note { color: var(--muted); font-size: 12.5px; }
.caveat-note { font-size: 12px; color: var(--muted); line-height: 1.6; margin-top: 10px; max-width: 640px; }
</style>
</head>
<body>

<div class="app">

  <aside class="sidebar">
    <div class="brand">
      <span class="brand-mark">Φ</span>
      <div class="brand-text">
        <h1>Phage Bench</h1>
        <p>genome analysis workbench</p>
      </div>
    </div>

    <p class="runs-locally">Runs entirely in your browser. Nothing is uploaded anywhere — your sequence never leaves this page.</p>

    <div class="input-panel">
      <label class="dropzone" id="dropzone" for="fasta-file">
        <span class="dropzone-icon">⤒</span>
        <span class="dropzone-label">Drop a .fasta / .fa / .txt file here<br>or click to browse</span>
        <span class="dropzone-filename" id="dropzone-filename"></span>
      </label>
      <input type="file" id="fasta-file" accept=".fasta,.fa,.fna,.txt" hidden />

      <p class="field-label">…or paste FASTA text</p>
      <textarea id="paste-area" placeholder=">my_phage
ATGCGTACG..."></textarea>

      <div>
        <div class="sensitivity-row">
          <span>Minimum gene size</span>
          <span id="sensitivity-value">30 aa</span>
        </div>
        <input type="range" id="sensitivity" min="15" max="100" value="30" step="5" />
      </div>

      <button type="button" class="link-btn" id="use-sample">Use sample genome instead</button>
      <button type="button" class="submit-btn" id="run-btn">Run pipeline</button>
    </div>

    <div class="pipeline-key">
      <p class="pipeline-key-title">Pipeline stages</p>
      <ol id="stage-list"></ol>
    </div>
  </aside>

  <main class="main">

    <section id="empty-state" class="empty-state">
      <p class="eyebrow">No genome loaded</p>
      <h2>Upload or paste a FASTA sequence to begin</h2>
      <p class="muted">Gene finding runs for real, using a 6-frame ORF scan in your browser.
        Taxonomy, host, and lifestyle prediction are shown as clearly-labeled placeholders —
        those need large reference databases and dedicated tools that can't run inside a
        static web page. See each tab for what a real implementation would use.</p>
    </section>

    <section id="progress-state" class="progress-state hidden">
      <p class="eyebrow" id="progress-genome-name">Processing…</p>
      <div class="progress-track" id="progress-track"></div>
      <p class="progress-message" id="progress-message"></p>
    </section>

    <section id="error-state" class="error-state hidden">
      <p class="eyebrow">Couldn't process that</p>
      <h2 id="error-message"></h2>
      <button class="link-btn" id="error-dismiss">Try again</button>
    </section>

    <section id="results-state" class="results-state hidden">

      <div class="overview-cards" id="overview-cards"></div>

      <div class="genome-map-wrap">
        <p class="section-label">Genome map <span class="section-label-sub">— candidate genes by position and strand</span></p>
        <div id="genome-map"></div>
        <div class="legend">
          <span class="legend-item"><i class="swatch swatch-fwd"></i> forward strand</span>
          <span class="legend-item"><i class="swatch swatch-rev"></i> reverse strand</span>
        </div>
        <p class="caveat-note">These are candidate open reading frames found by scanning for start→stop codons in all 6 frames, not a validated gene model — real tools (Prodigal/Pharokka) score coding likelihood and are more precise. Try the sensitivity slider if you get too many or too few results.</p>
      </div>

      <div class="results-tabs">
        <div class="tabs" role="tablist">
          <button class="tab active" data-rtab="genes">Genes</button>
          <button class="tab" data-rtab="taxonomy">Taxonomy</button>
          <button class="tab" data-rtab="host">Host prediction</button>
          <button class="tab" data-rtab="lifestyle">Lifestyle</button>
        </div>

        <div class="result-panel active" data-rpanel="genes">
          <div class="genes-table-wrap">
            <table class="genes-table" id="genes-table">
              <thead><tr><th>Gene</th><th>Start</th><th>End</th><th>Strand</th><th>Length (aa)</th><th>Function</th></tr></thead>
              <tbody id="genes-tbody"></tbody>
            </table>
          </div>
        </div>

        <div class="result-panel" data-rpanel="taxonomy">
          <div class="placeholder-card" id="taxonomy-card"></div>
        </div>
        <div class="result-panel" data-rpanel="host">
          <div class="placeholder-card" id="host-card"></div>
        </div>
        <div class="result-panel" data-rpanel="lifestyle">
          <div class="placeholder-card" id="lifestyle-card"></div>
        </div>
      </div>

    </section>

  </main>
</div>

<script>
const STAGE_LABELS = {
  qc: "Reading & checking sequence",
  gene_calling: "Scanning for genes (6-frame ORF search)",
  functional_annotation: "Functional annotation",
  taxonomy_classification: "Taxonomy classification",
  host_prediction: "Host prediction",
  lifestyle_prediction: "Lifestyle prediction",
  done: "Done",
};
const STAGE_KEYS = Object.keys(STAGE_LABELS);

let currentFastaText = null;

const SAMPLE_FASTA = (() => {
  // Deterministic synthetic sequence, generated once, purely for exercising
  // the pipeline UI. Not a real phage genome.
  let seed = 7;
  function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
  const bases = "ACGT";
  let seq = "";
  for (let i = 0; i < 15000; i++) seq += bases[Math.floor(rnd() * 4)];
  let fasta = ">sample_phage_001 synthetic test genome for pipeline smoke-testing\n";
  for (let i = 0; i < seq.length; i += 70) fasta += seq.slice(i, i + 70) + "\n";
  return fasta;
})();

// ---------- Sensitivity slider ----------
const sensSlider = document.getElementById("sensitivity");
const sensValue = document.getElementById("sensitivity-value");
sensSlider.addEventListener("input", () => { sensValue.textContent = sensSlider.value + " aa"; });

// ---------- Results tabs ----------
document.querySelectorAll(".results-tabs .tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".results-tabs .tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".result-panel").forEach((p) => p.classList.remove("active"));
    tab.classList.add("active");
    document.querySelector(`.result-panel[data-rpanel="${tab.dataset.rtab}"]`).classList.add("active");
  });
});

// ---------- File input / dropzone ----------
const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fasta-file");
const filenameLabel = document.getElementById("dropzone-filename");
const pasteArea = document.getElementById("paste-area");

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) loadFile(fileInput.files[0]);
});
["dragover", "dragleave", "drop"].forEach((evt) => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.toggle("drag-over", evt === "dragover");
  });
});
dropzone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) loadFile(file);
});

function loadFile(file) {
  filenameLabel.textContent = file.name;
  const reader = new FileReader();
  reader.onload = () => { currentFastaText = reader.result; pasteArea.value = ""; };
  reader.readAsText(file);
}

document.getElementById("use-sample").addEventListener("click", () => {
  pasteArea.value = SAMPLE_FASTA;
  currentFastaText = null;
  filenameLabel.textContent = "";
});

document.getElementById("run-btn").addEventListener("click", () => {
  const text = currentFastaText || pasteArea.value;
  if (!text || !text.trim()) {
    showError("Upload a FASTA file or paste FASTA text first.");
    return;
  }
  runPipeline(text);
});

document.getElementById("error-dismiss").addEventListener("click", () => showState("empty"));

// ---------- FASTA parsing ----------
function parseFasta(text) {
  const lines = text.split(/\r?\n/);
  let header = null;
  let seqParts = [];
  for (const line of lines) {
    if (line.startsWith(">")) {
      if (header !== null) break; // only take the first record
      header = line.slice(1).trim();
    } else if (header !== null) {
      seqParts.push(line.trim());
    }
  }
  if (header === null) throw new Error("No FASTA header ('>') found. Make sure your file/text starts with a '>' line.");
  const seq = seqParts.join("").toUpperCase().replace(/[^ACGTN]/g, "");
  if (seq.length < 100) throw new Error("Sequence is too short to analyze (need at least 100 bp).");
  return { id: (header.split(/\s+/)[0] || "genome"), description: header, sequence: seq };
}

// ---------- Gene finding (6-frame ORF scan) ----------
const COMPLEMENT = { A: "T", T: "A", G: "C", C: "G", N: "N" };
function reverseComplement(seq) {
  let out = "";
  for (let i = seq.length - 1; i >= 0; i--) out += COMPLEMENT[seq[i]] || "N";
  return out;
}
const STOP_CODONS = new Set(["TAA", "TAG", "TGA"]);
const CODON_TABLE = {
  TTT:"F",TTC:"F",TTA:"L",TTG:"L",CTT:"L",CTC:"L",CTA:"L",CTG:"L",
  ATT:"I",ATC:"I",ATA:"I",ATG:"M",GTT:"V",GTC:"V",GTA:"V",GTG:"V",
  TCT:"S",TCC:"S",TCA:"S",TCG:"S",CCT:"P",CCC:"P",CCA:"P",CCG:"P",
  ACT:"T",ACC:"T",ACA:"T",ACG:"T",GCT:"A",GCC:"A",GCA:"A",GCG:"A",
  TAT:"Y",TAC:"Y",TAA:"*",TAG:"*",CAT:"H",CAC:"H",CAA:"Q",CAG:"Q",
  AAT:"N",AAC:"N",AAA:"K",AAG:"K",GAT:"D",GAC:"D",GAA:"E",GAG:"E",
  TGT:"C",TGC:"C",TGA:"*",TGG:"W",CGT:"R",CGC:"R",CGA:"R",CGG:"R",
  AGT:"S",AGC:"S",AGA:"R",AGG:"R",GGT:"G",GGC:"G",GGA:"G",GGG:"G",
};
function translate(seq) {
  let protein = "";
  for (let i = 0; i + 3 <= seq.length; i += 3) protein += CODON_TABLE[seq.substr(i, 3)] || "X";
  return protein;
}

function findGenes(sequence, minAaLen) {
  const N = sequence.length;
  const genes = [];
  let geneCount = 0;

  function scanStrand(workingSeq, strand) {
    for (let frame = 0; frame < 3; frame++) {
      let i = frame;
      while (i + 3 <= workingSeq.length) {
        const codon = workingSeq.substr(i, 3);
        if (codon === "ATG") {
          let j = i;
          let foundStop = false;
          while (j + 3 <= workingSeq.length) {
            const codon2 = workingSeq.substr(j, 3);
            if (STOP_CODONS.has(codon2)) { foundStop = true; break; }
            j += 3;
          }
          if (foundStop) {
            const endIdx = j + 3; // exclusive, in workingSeq coords
            const aaLen = (j - i) / 3;
            if (aaLen >= minAaLen) {
              geneCount++;
              const orfNt = workingSeq.slice(i, endIdx);
              const protein = translate(orfNt).slice(0, -1); // drop trailing stop symbol
              let start1, end1;
              if (strand === "+") {
                start1 = i + 1;
                end1 = endIdx;
              } else {
                // workingSeq is the reverse complement; map back to original coords
                start1 = N - endIdx + 1;
                end1 = N - i;
              }
              genes.push({
                id: "gene_" + String(geneCount).padStart(4, "0"),
                start: start1,
                end: end1,
                strand,
                length_aa: aaLen,
                translation: protein,
              });
            }
            i = endIdx;
          } else {
            break; // no stop found before end of frame — incomplete ORF, skip
          }
        } else {
          i += 3;
        }
      }
    }
  }

  scanStrand(sequence, "+");
  scanStrand(reverseComplement(sequence), "-");
  genes.sort((a, b) => a.start - b.start);
  // re-number in genomic order
  genes.forEach((g, idx) => { g.id = "gene_" + String(idx + 1).padStart(4, "0"); });
  return genes;
}

function gcContent(seq) {
  if (!seq.length) return 0;
  let gc = 0;
  for (const ch of seq) if (ch === "G" || ch === "C") gc++;
  return Math.round((100 * gc / seq.length) * 100) / 100;
}

// ---------- Placeholder pipeline stages ----------
// See the note in each card for what a real implementation would use.
function functionalAnnotation(genes) {
  const annotations = genes.map((g) => ({ gene_id: g.id, function: "hypothetical protein", is_placeholder: true }));
  return { annotations, note: "Functional annotation requires an HMM search against the PHROGs database (phage-specific protein families) — e.g. via Pharokka. Every gene is shown as 'hypothetical protein' until that's wired in." };
}
function taxonomyClassification() {
  return { predicted_family: null, predicted_genus: null, closest_reference: null, is_placeholder: true, note: "Taxonomy classification requires clustering against a reference database (e.g. INPHARED via vConTACT2) — not something that can run in a browser." };
}
function hostPrediction() {
  return { predicted_host_genus: null, predicted_host_species: null, method: null, is_placeholder: true, note: "Host prediction requires a reference bacterial genome database — iPHoP is the current standard tool for this." };
}
function lifestylePrediction() {
  return { prediction: null, lytic_probability: null, temperate_probability: null, is_placeholder: true, note: "Lifestyle (lytic vs. lysogenic) prediction requires BACPHLIP's HMM domain search against known lysogeny-associated protein families." };
}

// ---------- Pipeline runner (with a little animation so stages are visible) ----------
async function runPipeline(fastaText) {
  showState("progress");
  buildStageList(null);

  let genome;
  try {
    genome = parseFasta(fastaText);
  } catch (err) {
    showError(err.message);
    return;
  }

  document.getElementById("progress-genome-name").textContent = `Processing — ${genome.id}`;

  const minAaLen = parseInt(sensSlider.value, 10);
  const steps = [
    ["qc", "Computing length and GC content"],
    ["gene_calling", "Scanning 6 reading frames for ORFs"],
    ["functional_annotation", "Annotating gene function"],
    ["taxonomy_classification", "Classifying taxonomy"],
    ["host_prediction", "Predicting bacterial host"],
    ["lifestyle_prediction", "Predicting lytic vs lysogenic lifestyle"],
  ];

  let genes = [];
  for (const [key, message] of steps) {
    buildStageList(key);
    updateProgressBar(key);
    document.getElementById("progress-message").textContent = message;
    await sleep(220); // brief pause so the pipeline is visible, not just a flash
    if (key === "gene_calling") genes = findGenes(genome.sequence, minAaLen);
  }

  const results = {
    genome: {
      accession: genome.id,
      description: genome.description,
      length_bp: genome.sequence.length,
      gc_content_pct: gcContent(genome.sequence),
      gene_count: genes.length,
    },
    genes,
    functional_annotation: functionalAnnotation(genes),
    taxonomy: taxonomyClassification(),
    host_prediction: hostPrediction(),
    lifestyle_prediction: lifestylePrediction(),
  };

  buildStageList("done");
  renderResults(results);
  showState("results");
}

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

function updateProgressBar(currentKey) {
  const idx = STAGE_KEYS.indexOf(currentKey);
  const track = document.getElementById("progress-track");
  track.innerHTML = "";
  STAGE_KEYS.forEach((key, i) => {
    const el = document.createElement("div");
    el.className = "progress-step";
    if (i < idx) el.classList.add("done");
    if (i === idx) el.classList.add("active");
    track.appendChild(el);
  });
}

function buildStageList(currentKey) {
  const list = document.getElementById("stage-list");
  const idx = currentKey ? STAGE_KEYS.indexOf(currentKey) : -1;
  list.innerHTML = "";
  STAGE_KEYS.forEach((key, i) => {
    const li = document.createElement("li");
    if (i < idx) li.classList.add("done");
    if (i === idx) li.classList.add("active");
    li.innerHTML = `<span class="dot"></span> ${STAGE_LABELS[key]}`;
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
    <div class="overview-card"><p class="label">Sequence ID</p><p class="value" style="font-size:16px">${escapeHtml(g.accession)}</p></div>
    <div class="overview-card"><p class="label">Length</p><p class="value">${g.length_bp.toLocaleString()} bp</p></div>
    <div class="overview-card"><p class="label">GC content</p><p class="value">${g.gc_content_pct}%</p></div>
    <div class="overview-card"><p class="label">Candidate genes</p><p class="value">${g.gene_count}</p></div>
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
  renderPlaceholderCard("lifestyle-card", results.lifestyle_prediction, [
    ["Prediction", results.lifestyle_prediction.prediction],
    ["Lytic probability", results.lifestyle_prediction.lytic_probability],
    ["Temperate probability", results.lifestyle_prediction.temperate_probability],
  ]);
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
    arrows += `<rect x="${x1}" y="${y}" width="${w}" height="14" rx="2" fill="${color}" opacity="0.85"><title>${escapeHtml(gene.id)}: ${gene.start}-${gene.end} (${gene.strand})</title></rect>`;
  });
  document.getElementById("genome-map").innerHTML = `
    <svg width="100%" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" style="min-width:700px">
      <line x1="10" y1="${midY}" x2="${width - 10}" y2="${midY}" stroke="var(--border)" stroke-width="2" />
      ${arrows}
    </svg>`;
}

function renderGenesTable(genes, annotations) {
  const byId = Object.fromEntries(annotations.map((a) => [a.gene_id, a]));
  document.getElementById("genes-tbody").innerHTML = genes.map((gene) => {
    const ann = byId[gene.id] || {};
    const strandClass = gene.strand === "+" ? "strand-fwd" : "strand-rev";
    return `<tr>
      <td>${escapeHtml(gene.id)}</td><td>${gene.start}</td><td>${gene.end}</td>
      <td class="${strandClass}">${gene.strand}</td><td>${gene.length_aa}</td>
      <td>${escapeHtml(ann.function || "—")}</td>
    </tr>`;
  }).join("") || `<tr><td colspan="6" style="color:var(--muted)">No candidate genes found above the current size threshold — try lowering "minimum gene size".</td></tr>`;
}

function renderPlaceholderCard(elementId, data, fields) {
  const rows = fields.map(([label, value]) => `<p><strong>${label}:</strong> ${value === null || value === undefined ? "—" : escapeHtml(String(value))}</p>`).join("");
  const badge = data.is_placeholder ? `<span class="placeholder-badge">not yet wired to a real tool</span>` : "";
  document.getElementById(elementId).innerHTML = `${badge}${rows}<p class="note">${escapeHtml(data.note || "")}</p>`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
</script>
</body>
</html>

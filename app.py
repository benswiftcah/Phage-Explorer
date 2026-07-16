"""
Phage Explorer backend.

Real, working pipeline stages:
  - genome input (FASTA upload or NCBI accession fetch)
  - gene calling (Pyrodigal)
  - lifestyle prediction, lytic vs. lysogenic (BACPHLIP)

Placeholder stages (clearly labeled in their output, not faked):
  - functional annotation      -> needs PHROGs + an HMM search (e.g. via Pharokka)
  - taxonomy classification    -> needs a reference set (e.g. INPHARED via vConTACT2)
  - host prediction             -> needs a reference bacterial genome DB (e.g. iPHoP)

Kept deliberately as one file so it's easy to upload/inspect on Hugging Face
Spaces without juggling a package structure.
"""
import asyncio
import dataclasses
import functools
import subprocess
import tempfile
import threading
import time
import uuid
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional

import pyrodigal
from Bio import Entrez, SeqIO
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
SAMPLE_FASTA = BASE_DIR / "sample_data" / "sample_phage.fasta"

Entrez.email = "phage-explorer-user@example.com"  # NCBI asks that requests self-identify

app = FastAPI(title="Phage Explorer")


async def run_in_thread(func, *args):
    """
    Python-3.8-compatible stand-in for asyncio.to_thread (added in 3.9).
    We're pinned to 3.8 for the BACPHLIP/scikit-learn compatibility fix
    (see Dockerfile), so this can't rely on the newer stdlib helper.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args))


# ============================================================
# Job store (in-memory; fine for a single small Space instance)
# ============================================================

STAGES = [
    "queued",
    "fetching_genome",
    "qc",
    "gene_calling",
    "functional_annotation",
    "taxonomy_classification",
    "host_prediction",
    "lifestyle_prediction",
    "done",
]

_lock = threading.Lock()
_jobs: Dict[str, Dict[str, Any]] = {}


def create_job() -> str:
    job_id = uuid.uuid4().hex[:12]
    with _lock:
        _jobs[job_id] = {
            "id": job_id, "status": "queued", "stage_index": 0,
            "stages": STAGES, "log": [], "error": None, "results": None,
            "created_at": time.time(),
        }
    return job_id


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    with _lock:
        job = _jobs.get(job_id)
        return dict(job) if job else None


def update_stage(job_id: str, stage: str, message: str = "") -> None:
    with _lock:
        job = _jobs.get(job_id)
        if not job:
            return
        job["status"] = stage
        if stage in STAGES:
            job["stage_index"] = STAGES.index(stage)
        if message:
            job["log"].append({"stage": stage, "message": message, "t": time.time()})


def set_error(job_id: str, message: str) -> None:
    with _lock:
        job = _jobs.get(job_id)
        if not job:
            return
        job["status"] = "error"
        job["error"] = message
        job["log"].append({"stage": "error", "message": message, "t": time.time()})


def set_results(job_id: str, results: Dict[str, Any]) -> None:
    with _lock:
        job = _jobs.get(job_id)
        if not job:
            return
        job["results"] = results
        job["status"] = "done"
        job["stage_index"] = len(STAGES) - 1


# ============================================================
# Genome input: FASTA upload or NCBI accession fetch
# ============================================================

@dataclasses.dataclass
class Genome:
    accession: str
    description: str
    sequence: str

    @property
    def length(self) -> int:
        return len(self.sequence)


def parse_uploaded_fasta(raw_bytes: bytes) -> Genome:
    text = raw_bytes.decode("utf-8", errors="ignore")
    records = list(SeqIO.parse(StringIO(text), "fasta"))
    if not records:
        raise ValueError("No FASTA records found. Make sure the file starts with a '>' header line.")
    if len(records) > 1:
        records.sort(key=lambda r: len(r.seq), reverse=True)  # analyze the largest contig
    record = records[0]
    seq = str(record.seq).upper().replace(" ", "").replace("\n", "")
    if not seq:
        raise ValueError("The FASTA record has no sequence data.")
    return Genome(accession=record.id, description=record.description, sequence=seq)


def fetch_from_ncbi(accession: str) -> Genome:
    accession = accession.strip()
    if not accession:
        raise ValueError("No accession number provided.")
    try:
        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text")
        record = SeqIO.read(handle, "fasta")
        handle.close()
    except Exception as exc:  # noqa: BLE001
        raise ValueError(
            f"Could not fetch accession '{accession}' from NCBI. "
            f"Check the accession is correct. ({exc})"
        ) from exc
    return Genome(accession=record.id, description=record.description, sequence=str(record.seq).upper())


# ============================================================
# REAL: gene calling (Pyrodigal)
# ============================================================

@dataclasses.dataclass
class Gene:
    id: str
    start: int
    end: int
    strand: str
    partial: bool
    length_aa: int
    translation: str


def call_genes(sequence: str) -> List[Gene]:
    finder = pyrodigal.GeneFinder(meta=True)
    orfs = finder.find_genes(sequence.encode())
    genes = []
    for i, orf in enumerate(orfs, start=1):
        protein = orf.translate()
        genes.append(Gene(
            id=f"gene_{i:04d}", start=orf.begin, end=orf.end,
            strand="+" if orf.strand == 1 else "-",
            partial=bool(orf.partial_begin or orf.partial_end),
            length_aa=len(protein), translation=protein,
        ))
    return genes


def gc_content(sequence: str) -> float:
    seq = sequence.upper()
    if not seq:
        return 0.0
    return round(100 * (seq.count("G") + seq.count("C")) / len(seq), 2)


# ============================================================
# REAL: lifestyle prediction (BACPHLIP)
# ============================================================

def lifestyle_prediction(genome: Genome) -> Dict[str, Any]:
    """
    Runs the actual BACPHLIP tool: an HMM search (via HMMER) for ~200
    lysogeny-associated protein domains, then a pretrained random forest
    classifier over the presence/absence pattern. Self-contained (its
    reference HMM database ships with the package), so no extra downloads.
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            fasta_path = Path(tmpdir) / "genome.fasta"
            with open(fasta_path, "w") as f:
                f.write(f">{genome.accession} {genome.description}\n{genome.sequence}\n")

            result = subprocess.run(
                ["bacphlip", "-i", str(fasta_path)],
                capture_output=True, text=True, timeout=180,
            )
            output_path = fasta_path.with_suffix(fasta_path.suffix + ".bacphlip")
            if not output_path.exists():
                raise RuntimeError(
                    f"BACPHLIP did not produce output. stderr: {result.stderr[-800:]}"
                )

            with open(output_path) as f:
                lines = [ln.rstrip("\n") for ln in f if ln.strip()]
            header = lines[0].split("\t")  # ['', 'Virulent', 'Temperate']
            values = lines[1].split("\t")  # ['<record_id>', '<p_virulent>', '<p_temperate>']
            row = dict(zip(header, values))
            p_virulent = float(row.get("Virulent", "nan"))
            p_temperate = float(row.get("Temperate", "nan"))

            prediction = "Temperate (lysogenic)" if p_temperate > p_virulent else "Virulent (lytic)"
            return {
                "prediction": prediction,
                "lytic_probability": round(p_virulent, 4),
                "temperate_probability": round(p_temperate, 4),
                "is_placeholder": False,
                "note": (
                    "Real BACPHLIP result: random forest classifier over presence/absence "
                    "of ~200 lysogeny-associated protein domains, found via HMMER. "
                    "Assumes the input is a complete phage genome — results on partial "
                    "genomes or non-phage sequences aren't meaningful."
                ),
            }
    except subprocess.TimeoutExpired:
        return _lifestyle_placeholder("BACPHLIP timed out (genome may be too large for this free instance).")
    except FileNotFoundError:
        return _lifestyle_placeholder("BACPHLIP or HMMER isn't installed in this environment.")
    except Exception as exc:  # noqa: BLE001
        return _lifestyle_placeholder(f"BACPHLIP failed: {exc}")


def _lifestyle_placeholder(reason: str) -> Dict[str, Any]:
    return {
        "prediction": None, "lytic_probability": None, "temperate_probability": None,
        "is_placeholder": True, "note": reason,
    }


# ============================================================
# PLACEHOLDER stages: functional annotation, taxonomy, host
# ============================================================

# ============================================================
# REAL: functional annotation (curated Pfam profile set + HMMER)
# ============================================================

from build_hmm_db import PHAGE_PFAM_FAMILIES  # noqa: E402

PFAM_LABELS = {accession: label for accession, label in PHAGE_PFAM_FAMILIES}
HMM_DB_PATH = BASE_DIR / "data" / "phage_profiles.hmm"


def functional_annotation(genes: List[Gene]) -> Dict[str, Any]:
    """
    Runs the actual genes through HMMER's hmmscan against a curated,
    locally-bundled set of ~20 well-established phage protein family
    profiles from Pfam (built at Docker build time — see build_hmm_db.py).

    This is real HMM-based annotation, not a placeholder — but it's
    deliberately a small, curated set rather than full PHROGs (38,880
    families, 3GB), which doesn't fit a free-tier instance's resources.
    Genes that don't match one of these ~20 families are honestly shown
    as "hypothetical protein" — that reflects the reference set's size,
    not a broken search.
    """
    if not genes:
        return {"annotations": [], "note": "No genes to annotate."}

    if not HMM_DB_PATH.exists():
        # Build-time step didn't run or failed — fail soft into the
        # placeholder shape rather than crashing the whole pipeline.
        annotations = [
            {"gene_id": g.id, "function": "hypothetical protein", "is_placeholder": True}
            for g in genes
        ]
        return {
            "annotations": annotations,
            "note": "Local HMM profile database not found on this deployment — functional annotation unavailable.",
        }

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            faa_path = Path(tmpdir) / "genes.faa"
            with open(faa_path, "w") as f:
                for gene in genes:
                    f.write(f">{gene.id}\n{gene.translation}\n")

            tbl_path = Path(tmpdir) / "hits.tbl"
            subprocess.run(
                [
                    "hmmscan", "--tblout", str(tbl_path), "--noali",
                    "-E", "1e-5", str(HMM_DB_PATH), str(faa_path),
                ],
                capture_output=True, text=True, timeout=120, check=True,
            )

            # Keep only the best (lowest e-value) hit per gene.
            best_hit: Dict[str, tuple] = {}  # gene_id -> (accession, evalue)
            with open(tbl_path) as f:
                for line in f:
                    if line.startswith("#") or not line.strip():
                        continue
                    parts = line.split()
                    target_accession = parts[1].split(".")[0]  # strip Pfam version suffix
                    query_gene_id = parts[2]
                    evalue = float(parts[4])
                    if query_gene_id not in best_hit or evalue < best_hit[query_gene_id][1]:
                        best_hit[query_gene_id] = (target_accession, evalue)

            annotations = []
            matched = 0
            for gene in genes:
                hit = best_hit.get(gene.id)
                if hit:
                    accession, evalue = hit
                    label = PFAM_LABELS.get(accession, accession)
                    matched += 1
                    annotations.append({
                        "gene_id": gene.id, "function": label,
                        "pfam_accession": accession, "evalue": evalue,
                        "is_placeholder": False,
                    })
                else:
                    annotations.append({
                        "gene_id": gene.id, "function": "hypothetical protein",
                        "is_placeholder": True,
                    })

            return {
                "annotations": annotations,
                "note": (
                    f"Real HMM search (HMMER hmmscan) against a curated set of "
                    f"{len(PHAGE_PFAM_FAMILIES)} common phage protein families from Pfam "
                    f"— matched {matched} of {len(genes)} genes. This is a small, hand-picked "
                    f"subset (capsid, portal, terminase, tail, integrase, lysis, replication "
                    f"genes), not the full PHROGs database (38,880 families) — genes outside "
                    f"this set are shown as 'hypothetical protein' because they weren't "
                    f"checked against a family that would recognize them, not because they "
                    f"were checked and failed."
                ),
            }
    except subprocess.TimeoutExpired:
        annotations = [{"gene_id": g.id, "function": "hypothetical protein", "is_placeholder": True} for g in genes]
        return {"annotations": annotations, "note": "Annotation search timed out."}
    except Exception as exc:  # noqa: BLE001
        annotations = [{"gene_id": g.id, "function": "hypothetical protein", "is_placeholder": True} for g in genes]
        return {"annotations": annotations, "note": f"Annotation search failed: {exc}"}


def taxonomy_classification() -> Dict[str, Any]:
    return {
        "predicted_family": None, "predicted_genus": None, "closest_reference": None,
        "is_placeholder": True,
        "note": ("Taxonomy classification requires clustering against a reference database "
                  "(e.g. INPHARED via vConTACT2) — not yet wired into this deployment."),
    }


def host_prediction() -> Dict[str, Any]:
    return {
        "predicted_host_genus": None, "predicted_host_species": None, "method": None,
        "is_placeholder": True,
        "note": ("Host prediction requires a reference bacterial genome database "
                  "(iPHoP is the current standard tool) — not yet wired into this deployment."),
    }


# ============================================================
# Pipeline orchestration
# ============================================================

async def run_pipeline(job_id: str, genome: Genome) -> None:
    try:
        update_stage(job_id, "qc", "Computing length and GC content")
        length = genome.length
        gc = await run_in_thread(gc_content, genome.sequence)

        update_stage(job_id, "gene_calling", "Calling genes with Pyrodigal")
        genes = await run_in_thread(call_genes, genome.sequence)

        update_stage(job_id, "functional_annotation", "Annotating gene function")
        annotation = await run_in_thread(functional_annotation, genes)

        update_stage(job_id, "taxonomy_classification", "Classifying taxonomy")
        taxonomy = await run_in_thread(taxonomy_classification)

        update_stage(job_id, "host_prediction", "Predicting bacterial host")
        host = await run_in_thread(host_prediction)

        update_stage(job_id, "lifestyle_prediction", "Running BACPHLIP (HMM search + classifier)")
        lifestyle = await run_in_thread(lifestyle_prediction, genome)

        results = {
            "genome": {
                "accession": genome.accession, "description": genome.description,
                "length_bp": length, "gc_content_pct": gc, "gene_count": len(genes),
            },
            "genes": [dataclasses.asdict(g) for g in genes],
            "functional_annotation": annotation,
            "taxonomy": taxonomy,
            "host_prediction": host,
            "lifestyle_prediction": lifestyle,
        }
        set_results(job_id, results)
    except Exception as exc:  # noqa: BLE001
        set_error(job_id, str(exc))


# ============================================================
# Routes
# ============================================================

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/api/sample")
async def get_sample_genome():
    if not SAMPLE_FASTA.exists():
        raise HTTPException(status_code=404, detail="Sample genome not found.")
    return FileResponse(SAMPLE_FASTA, media_type="text/plain", filename="sample_phage.fasta")


@app.post("/api/jobs")
async def submit_job(
    file: Optional[UploadFile] = File(default=None),
    accession: Optional[str] = Form(default=None),
):
    if not file and not accession:
        raise HTTPException(status_code=400, detail="Provide either a FASTA file or an NCBI accession number.")

    job_id = create_job()
    try:
        if file is not None:
            update_stage(job_id, "fetching_genome", "Reading uploaded FASTA")
            raw = await file.read()
            genome = parse_uploaded_fasta(raw)
        else:
            update_stage(job_id, "fetching_genome", f"Fetching {accession} from NCBI")
            genome = await run_in_thread(fetch_from_ncbi, accession)
    except ValueError as exc:
        set_error(job_id, str(exc))
        return {"job_id": job_id}

    asyncio.create_task(run_pipeline(job_id, genome))
    return {"job_id": job_id}


@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return {
        "id": job["id"], "status": job["status"], "stage_index": job["stage_index"],
        "stages": job["stages"], "error": job["error"], "log": job["log"],
    }


@app.get("/api/jobs/{job_id}/results")
async def get_job_results(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job["status"] == "error":
        raise HTTPException(status_code=422, detail=job["error"])
    if job["status"] != "done":
        raise HTTPException(status_code=409, detail="Job is still running.")
    return job["results"]

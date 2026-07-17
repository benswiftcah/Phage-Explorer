[README.md](https://github.com/user-attachments/files/30115430/README.md)
# Phage Explorer

A phage genome analysis tool. Upload a FASTA file or give an NCBI accession,
and get back real gene predictions and a real lytic-vs-lysogenic lifestyle
prediction.

## What's real here

| Stage | Status | Tool |
|---|---|---|
| Genome input (upload / NCBI fetch) | **Real** | Biopython |
| Gene calling | **Real** | PHANOTATE (phage-specific; Pyrodigal auto-fallback) |
| Lifestyle prediction (lytic/lysogenic) | **Real** | BACPHLIP (HMMER + random forest) |
| Functional annotation | **Real (curated subset)** | HMMER + ~20 hand-picked Pfam phage families |
| Taxonomy classification | Placeholder | needs a reference set (e.g. INPHARED + vConTACT2) |
| Host prediction | Placeholder | needs a reference bacterial genome DB (e.g. iPHoP) |

Functional annotation runs a real HMM search (`hmmscan`), but against a
curated set of ~29 well-established Pfam phage protein families (capsid,
portal, terminase, tail, integrase, excisionase, lysis, Red recombination,
DNA replication genes) rather than the full PHROGs database (38,880
families, 3GB unzipped — too large for a free-tier instance). Genes
outside this set show "hypothetical protein", honestly reflecting the
reference set's size rather than a failed search. See `build_hmm_db.py`
for the exact family list and the InterPro API calls used to build the
local HMM database at Docker build time.

## Deploying (Render.com)

This repo is set up to deploy directly on Render as a **Docker** web
service, free tier, no credit card:

1. Push/upload this repo to GitHub.
2. On Render: **New -> Web Service** -> connect this GitHub repo.
3. Render auto-detects the `Dockerfile` at the repo root -- leave environment
   as **Docker**, instance type **Free**.
4. Click **Create Web Service**. First build takes a few minutes (installing
   HMMER + compiling a couple of Python packages).
5. Your app is live at `https://<your-service-name>.onrender.com`.

Free-tier services spin down after ~15 minutes of inactivity; the next
visit takes 30-60 seconds to wake back up. That's normal for free hosting,
not a bug.

## Why PHANOTATE instead of just Pyrodigal

General-purpose gene callers (Prodigal, which Pyrodigal wraps) are tuned
for typical bacterial gene spacing and reliably under-call genes on phage
genomes, which pack genes far more densely and with heavy overlap. This
is a documented limitation, not a tuning issue -- it's the reason
PHANOTATE exists as a phage-specific alternative. Direct comparison on
real phage lambda (NC_001416.1, 48,502 bp, ~73 annotated genes):

| Caller | Genes found |
|---|---|
| Pyrodigal (meta mode) | 62 |
| PHANOTATE | 88 |

PHANOTATE is noticeably slower (a more exhaustive dynamic-programming
search is exactly why it catches more genes) -- expect the gene-calling
stage to take 10-20+ seconds on a real genome, longer on Render's free
CPU tier than in a fast dev environment. `call_genes()` in `app.py` tries
PHANOTATE first and automatically falls back to Pyrodigal if it's ever
unavailable or errors out, so gene calling never hard-fails.

## Why Python 3.8

The Dockerfile pins `python:3.8-slim` deliberately. BACPHLIP's pretrained
classifier was pickled with `scikit-learn==0.23.1`, and that exact version
only publishes prebuilt wheels for Python 3.7/3.8. On a newer Python, pip
either fails to build scikit-learn from source or resolves to a newer
version that can't load the pickle. Don't bump the Python or scikit-learn
version without testing that the classifier still loads.

## Why the app reads $PORT

Render assigns the port your service must listen on via the `PORT`
environment variable at container start (default 10000) -- it's not fixed
the way some other hosts do it. The Dockerfile's `CMD` reads `$PORT` at
runtime for this reason; don't hardcode a port number here.

# Python 3.8 is required here, not a stylistic choice: BACPHLIP ships a
# pretrained model pickled with scikit-learn==0.23.1, and that exact
# scikit-learn version only has prebuilt wheels for Python 3.7/3.8. A newer
# Python forces scikit-learn to be built from source or resolved to a newer
# version that can't load the pickle (breaks BACPHLIP's classifier step).
FROM python:3.8-slim

# hmmer provides hmmsearch, which BACPHLIP calls as a subprocess.
RUN apt-get update && apt-get install -y --no-install-recommends \
    hmmer \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
WORKDIR /app

COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=user . /app

# Build the curated phage-protein-family HMM database (downloads ~20 Pfam
# HMMs and presses them into a local HMMER database). Runs at build time,
# not per-request, and baked into the image. If this step's network calls
# fail on a given platform, see build_hmm_db.py -- it degrades gracefully
# (skips unreachable families) rather than failing the whole build, as
# long as at least one family downloads successfully.
RUN python3 build_hmm_db.py

USER user
ENV HOME=/home/user

# Render injects the port to listen on via $PORT (default 10000) — it is
# NOT fixed like it was on Hugging Face Spaces, so this must be read at
# container start, not baked in. Shell form (not exec form) is required
# so the environment variable actually gets expanded.
CMD sh -c "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"

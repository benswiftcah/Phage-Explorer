"""
Build-time script: downloads a curated set of phage-relevant Pfam protein
family HMM profiles and assembles them into one local HMMER database.

Why a curated subset and not full PHROGs: PHROGs (the standard phage
annotation database) is ~38,880 families and 3 GB unzipped -- too large
for a free-tier instance's disk/RAM/build-time budget. This uses ~20
well-established, individually-verified Pfam families instead: covers the
classic phage gene categories (capsid, portal, terminase, tail, integrase,
lysis, DNA replication) at a fraction of the size. Genes that don't match
one of these ~20 families will still show "hypothetical protein" -- that's
an honest reflection of a small reference set, not a bug.

Each family is fetched from the InterPro API, which serves each Pfam
family's HMM individually and compressed:
    https://www.ebi.ac.uk/interpro/api/entry/pfam/{ACCESSION}/?annotation=hmm

Run at Docker build time (see Dockerfile) so the database is baked into
the image -- no per-request network calls, and any download problems
surface immediately in the build log rather than at first user request.
"""
import gzip
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# (Pfam accession, friendly function label) -- every accession here was
# verified against a real source (Pfam/InterPro pages or peer-reviewed
# papers citing it) before being added; see conversation history / commit
# message for sourcing notes if this list is ever extended.
PHAGE_PFAM_FAMILIES = [
    # Capsid / head
    ("PF05065", "major capsid protein"),
    ("PF05125", "capsid protein (P2-like)"),
    ("PF05396", "capsid protein (T7-like)"),
    # Portal / head-tail connector
    ("PF04860", "portal protein"),
    ("PF05136", "portal protein"),
    ("PF12236", "head-tail connector protein"),
    # Tail
    ("PF13550", "tail protein"),
    # DNA packaging (terminase)
    ("PF03592", "terminase (packaging ATPase)"),
    ("PF04466", "terminase (packaging ATPase)"),
    ("PF03237", "terminase (packaging ATPase)"),
    ("PF05876", "terminase large subunit"),
    # Lysogeny / integration
    ("PF00589", "integrase (site-specific recombination)"),
    ("PF00717", "repressor protein (autocleaving peptidase domain)"),
    # Lysis
    ("PF00959", "endolysin (peptidoglycan hydrolase)"),
    ("PF05106", "holin (lysis, membrane pore-forming)"),
    ("PF10746", "holin (lysis, membrane pore-forming)"),
    ("PF16082", "holin (lysis, membrane pore-forming)"),
    # DNA replication / metabolism
    ("PF00476", "DNA polymerase (family A)"),
    ("PF03796", "DNA helicase (DnaB-like, C-terminal domain)"),
    ("PF02945", "HNH endonuclease (recombination/DNA processing)"),
    ("PF00145", "DNA methyltransferase"),
    ("PF01653", "DNA ligase (adenylation domain)"),
    ("PF13392", "HNH endonuclease"),
]

INTERPRO_URL_TEMPLATE = "https://www.ebi.ac.uk/interpro/api/entry/pfam/{}/?annotation=hmm"


def fetch_one(accession: str) -> bytes:
    url = INTERPRO_URL_TEMPLATE.format(accession)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        compressed = resp.read()
    return gzip.decompress(compressed)


def main():
    out_dir = Path(__file__).resolve().parent / "data"
    out_dir.mkdir(exist_ok=True)
    combined_path = out_dir / "phage_profiles.hmm"

    succeeded = []
    failed = []

    with open(combined_path, "wb") as out_f:
        for accession, label in PHAGE_PFAM_FAMILIES:
            try:
                hmm_bytes = fetch_one(accession)
                out_f.write(hmm_bytes)
                if not hmm_bytes.endswith(b"\n"):
                    out_f.write(b"\n")
                succeeded.append(accession)
                print(f"[ok]   {accession}  {label}")
            except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
                failed.append(accession)
                print(f"[skip] {accession}  {label}  -- {exc}", file=sys.stderr)

    print(f"\nDownloaded {len(succeeded)}/{len(PHAGE_PFAM_FAMILIES)} profile families.")
    if failed:
        print(f"Skipped (annotation feature will just have less coverage): {failed}", file=sys.stderr)

    if not succeeded:
        print("ERROR: zero profile families downloaded, cannot build a usable database.", file=sys.stderr)
        sys.exit(1)

    # hmmpress builds the binary index files (.h3f/.h3i/.h3m/.h3p) hmmscan needs.
    subprocess.run(["hmmpress", str(combined_path)], check=True)
    print(f"Pressed HMM database at {combined_path}")


if __name__ == "__main__":
    main()

"""Fetch and derive the analysis input from the pinned public ProPublica COMPAS release.

The upstream dataset is NOT redistributed in this CODECHECK package. This script downloads
ProPublica's public `compas-scores-two-years.csv` at the repository commit pinned below,
applies ProPublica's published two-year inclusion filters, retains only the seven variables
used by the analysis, and writes `compas_analysis_min.csv`.
"""
from pathlib import Path
import hashlib
import pandas as pd

UPSTREAM_COMMIT = "bafff5da3f2e45eca6c2d5055faad269defd135a"
SRC = (
    "https://raw.githubusercontent.com/propublica/compas-analysis/"
    f"{UPSTREAM_COMMIT}/compas-scores-two-years.csv"
)
KEEP = ["id", "sex", "age", "race", "decile_score", "priors_count", "two_year_recid"]
EXPECTED_ROWS = 6172
EXPECTED_SHA256 = "8fe0a122e7bd08d79b217d92bab1d111c0b3192dad2f11832d49a6591a0a5d6e"

d = pd.read_csv(SRC)
print(f"upstream rows: {len(d)}")
d = d[(d.days_b_screening_arrest <= 30) & (d.days_b_screening_arrest >= -30) &
      (d.is_recid != -1) & (d.c_charge_degree != "O") & (d.score_text != "N/A")]
print(f"after ProPublica filters: {len(d)}  (expected {EXPECTED_ROWS})")
assert len(d) == EXPECTED_ROWS, "filtered cohort size does not match the published 6,172"

out = d[KEEP].copy()
out.to_csv("compas_analysis_min.csv", index=False)
h = hashlib.sha256(Path("compas_analysis_min.csv").read_bytes()).hexdigest()
print(f"wrote compas_analysis_min.csv  ({len(out)} rows, {len(KEEP)} columns)")
print(f"SHA-256: {h}")
assert h == EXPECTED_SHA256, "derived input hash differs from the locked analysis input"

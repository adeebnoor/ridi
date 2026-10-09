#!/usr/bin/env python3
"""Write LOCK.json: SHA-256 of models.json and every analysis/runner file. Commit LOCK.json publicly
(repository commit + OSF registration) BEFORE any generation. The runner refuses to start if a file differs."""
import hashlib, json, pathlib, re, sys
from datetime import datetime, timezone
here = pathlib.Path(__file__).resolve().parent
files = ["models.json", "run_scale_curve.py", "aggregate_scale_curve.py"]
M = json.loads((here / "models.json").read_text())
unresolved = [m["model_id"] for t in ("primary_family", "optional_tier") for m in M[t] if not re.fullmatch(r"[0-9a-f]{40}", m["revision"])]
if unresolved:
    sys.exit(f"Unresolved revisions (run resolve_revisions.py first): {unresolved}")
feature = here / "per_question_features.jsonl"
prereg = here.parent / "preregistration" / "OSF_Preregistration_RIDI-SCALE-CURVE-v1.md"
if not feature.is_file() or not prereg.is_file():
    sys.exit("Frozen P4 feature file and preregistration Markdown must be present before locking")
lock = {"study": M["study"],
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "files": {f: hashlib.sha256((here / f).read_bytes()).hexdigest() for f in files},
        "feature_sha256": hashlib.sha256(feature.read_bytes()).hexdigest(),
        "preregistration_sha256": hashlib.sha256(prereg.read_bytes()).hexdigest(),
        "generation_started": False}
(here / "LOCK.json").write_text(json.dumps(lock, indent=2) + "\n")
print(json.dumps(lock, indent=2))

#!/usr/bin/env python3
"""Fill exact Hugging Face commit SHAs into models.json (run once, BEFORE the lock and before any generation).
Requires network access to huggingface.co. Never changes a revision that is already a 40-hex SHA."""
import json, re, sys, pathlib
from huggingface_hub import HfApi
p = pathlib.Path(__file__).with_name("models.json")
M = json.loads(p.read_text())
api = HfApi()
for tier in ("primary_family", "optional_tier"):
    for m in M[tier]:
        if re.fullmatch(r"[0-9a-f]{40}", m["revision"]):
            print("kept", m["model_id"], m["revision"]); continue
        info = api.model_info(m["model_id"], revision="main")
        m["revision"] = info.sha
        m["resolved_at_utc"] = __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z"
        print("resolved", m["model_id"], info.sha)
p.write_text(json.dumps(M, indent=2) + "\n")

#!/usr/bin/env python3
"""LEGACY synthetic row generator; its files are NOT accepted by the locked analysis.

This generator predates terminal-attempt and provenance gates. It intentionally
creates no study lock, receipts or feature provenance and cannot run the analysis
end to end. The maintained, isolated synthetic-only tests are:

    python -m unittest discover -s tests -p test_aggregate_integrity.py -v

Never mix this generator's output with real study output directories.
"""
import json, sys, pathlib, random
print("WARNING: legacy synthetic records only; NOT compatible with the locked analysis. "
      "Use tests/test_aggregate_integrity.py for isolated end-to-end synthetic tests.", file=sys.stderr)
feat = [json.loads(l) for l in open(sys.argv[1])]
out = pathlib.Path(sys.argv[2]); rng = random.Random(1)
rates = {"qwen3-0.6b": .30, "qwen3-1.7b": .25, "qwen3-4b": .20, "qwen3-8b": .17, "qwen3-14b": .14, "qwen3-32b": .12}
for k, p in rates.items():
    for d in ["nq", "hotpotqa", "fever", "scifact"]:
        rows = []
        for f in [f for f in feat if f["dataset"] == d]:
            rc = rng.random() < .5; flip = rng.random() < p + (.08 if f["tot_either"] > 0 else 0)
            xc = (not rc) if flip else rc; fc = (not rc) if rng.random() < .01 else rc
            rows.append({"dataset": d, "query_id": str(f["qid"]), "task": f["task"], "model_key": k,
                         "reference_single_correct": rc, "random_single_correct": xc, "reference_fixed16_correct": fc,
                         "intervention_changed": rc != xc, "floor_changed": rc != fc, "correct_to_wrong": rc and not xc,
                         "wrong_to_correct": (not rc) and xc, "canonical_changed": flip or rng.random() < .2})
        p_ = out / k / d / "attempt1"; p_.mkdir(parents=True, exist_ok=True)
        (p_ / f"{k}__{d}__records.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        (p_ / "run_meta.json").write_text(json.dumps({"checks": {"determinism_first16_identical": 16, "determinism_n": 16}}))
print("legacy synthetic records written; not directly analyzable")

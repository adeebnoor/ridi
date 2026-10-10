# Post-registration deviation 001 — task-label alias in the S5 feature join

Study: RIDI-RAG-QWEN3-SCALE-CURVE-v1 (OSF whjbs). Written 2026-10-10T07:19:25Z, before any outcome estimate of this study was computed or inspected.

**Defect.** The frozen P4 feature file labels the FEVER and SciFact task as `verdict`; the frozen runner labels the same 300 questions `classification`. The locked analysis requires the two labels to be identical and stopped with `ValueError: P4 task mismatch` (receipt 2026-10-10T05:32:47Z) before computing anything.

**Change.** None to any locked file. A separate wrapper imports the locked `aggregate_scale_curve.py` unchanged (its SHA-256 is still verified against LOCK.json) and replaces only `load_features` with a copy that treats `verdict` and `classification` as the same task label. Every other check in `load_features` (feature SHA-256, exact 800-question coverage, strata sizes 93/238/86/282) is kept verbatim.

**Scope.** The task label is used only to join the frozen P4 strata (secondary analysis S5) and in the `qa` stratum test, which is unaffected (`qa` is spelled identically in both files). H1–H3 and S1–S4 do not read the feature file. No outcome record, threshold, seed, draw count or model status is changed. The analysis is run once.

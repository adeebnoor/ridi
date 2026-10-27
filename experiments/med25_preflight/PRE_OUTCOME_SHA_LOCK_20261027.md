# RIDI-MED-25 pre-outcome software and input freeze

**Status:** prospective snapshot before any MED25 model benchmark inference. This note is a data/code receipt, **not an OSF registration** and **not model results**.

Snapshot UTC date: 2026-10-27.

| Artifact | SHA-256 |
|---|---|
| `RIDI_MED25_v2_9_PREOUTCOME_SOFTWARE_FREEZE_20261027.zip` (pre-outcome runnable code archive) | `af4b0cdf8bbee14fa5ff43cb51382ab5a4be6b3c330d3f391db1ef7a05191d45` |
| Software file hash manifest | `a138b828bd85a0e5a3fb47c9387073d3c7837f790461aa036a9597594c99e5bb` |
| Local private data/input lock | `eb7d4b826bd7b48f3809f1e66bc977c58f31c6a586cd6f7fe8f40b9775d67847` |
| Pinned 27-model revision manifest | `ced685a27bbaf84642347114e7786c68b8fc6a7af75987a221b8b482f01e3a34` |

The intended prospective protocol is drafted under [OSF MED25 working project](https://osf.io/qzrfg/) and [private OSF registration draft](https://osf.io/registries/drafts/6adfd80239ce331aacf7f9e3/metadata); **not yet submitted** as of this record.

Inputs: PubMedQA expert 1,000 questions and MedQA USMLE 1,273 questions, MedRAG/textbooks 125,847 chunks. Ref=top-10 BM25, alternative=nonoverlapping nearest-BM25-score passages; scores are **not identical**, no physician-grade passage relevance assessment. All 2,273 questions and 22,730 exchange slots validated locally before model generation.

GPU readiness: synthetic RunPod A100 SXM pod was launched and stopped, $1.793/hr. Terminal output could not be read; actual Torch/vLLM runtime and model loading **not verified**. 21 of 27 tokenizer raw token-length profiles were checked; max 5,517, six unknown; model context 8,192 tokens remains a candidate runtime configuration pending per-model validation.

All model benchmark answers, hypotheses H1-H4, and Figure 6 MED25 results: **not generated**. Do not claim this source file establishes confirmatory preregistration or results. Avoid open redistribution of copyrighted test questions/textbook excerpts; those remain on authorized local Windows device.

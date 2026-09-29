# CFC ↔ RIDI Candidate Registry v0.1 — Construction Record

**Status:** CONSTRUCTED / NOT FROZEN POOL / NO SEED  
**Date:** 2026-09-29  
**Eligibility gate:** frozen and mirrored bilaterally before registry construction.

## Result

The frozen eligibility checker was run unchanged against the complete candidate registry.

- registrations: **800**
- ACCEPT: **800**
- REJECT: **0**
- checker SHA-256: `96ca16e12e3f2fecb5a06998eb28476e250b2a0965f2b26713da298391958904`
- candidate registry SHA-256: `09824e8fa0837cc852b34c984b3ad7156a7433a57d672f4124356f4806e2fccf`
- eligibility audit SHA-256: `23e027e7228c3a09d13b238619ca87389f304f3fb281c37b386cca6a6defe826`
- eligible-pool **draft** SHA-256: `ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade`

The 800 registrations are the entire registered primary RAG reference-vs-random frame: NQ 250, HotpotQA 250, FEVER 150, SciFact 150.

No candidate was included or excluded using:
- A/B model-output equality or difference;
- correctness;
- CFC output;
- RIDI output;
- desired asymmetry;
- publication interest.

## Source basis

See `SOURCE_PROVENANCE.md`.

The evaluation-definition binding is the retained preregistration artifact:

`protocol/PREREGISTRATION_NATURE_RAG.md`

SHA-256:

`0f7babda273f68e2095343f2fb33f2dca3c8720f95ed87ca3a0f47d1b337b063`

All 800 pairs were structurally checked to have identical complete relevance-grade vectors between reference and random before registry construction.

## Artifact transport

The large TSV artifacts are currently available as a temporary byte-exact transport bundle while this candidate registry is under bilateral review:

https://firestorage.ai/en/f/zdtjoL6fvp6w

Transport ZIP:
- filename: `CFC_RIDI_CANDIDATE_REGISTRY_INPUT_v0.1.zip`
- bytes: **435,772**
- SHA-256: `2b96ee5319cb93bce9b752fb4c6c3353c0e0463d8cd11e79f0dd682423093b00`
- current transport expiry: **2026-10-13T10:24:46Z**

The transport URL is **not** an authoritative freeze record. The authoritative identities are the SHA-256 values above. The transport exists only so the other party can independently obtain and verify the exact registry/audit/pool-draft bytes during review.

## Boundary

This step is candidate-registry construction and mechanical eligibility evaluation only.

It is **not**:
- eligible-pool freeze;
- seed generation;
- seed commitment;
- case selection;
- substantive CFC execution;
- substantive RIDI execution;
- interpretation.

The next step is independent bilateral verification of the registry, audit and pool-draft bytes. Only after agreement may the exact eligible pool be frozen. Seed commit–reveal remains later.

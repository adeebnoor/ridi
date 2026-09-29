# CFC ↔ RIDI selected specimen — I1-safe bilateral handoff request

**Case:** `RAG-nq-test1035`  
**Purpose:** Complete exact-byte neutral specimen freeze without crossing pre-commit inspection boundaries.

## Requested CFC-side mechanical action

Using the already-reviewed original transport:

- `source_specimens_1600.jsonl`
- `offline_endpoints_1600.jsonl`

run the public deterministic extractor:

`collaboration/cfc-ridi/instantiation-v0.1/tools/extract_selected_specimen.py`

Expected frozen selected-line SHA-256 identities:

```text
source A    60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734
endpoint A  e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67
source B    018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308
endpoint B  e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5
```

The extractor must PASS all four exact-line identities before either side proceeds.

## Shared neutral handoff allowed by I1

After PASS, CFC may send/publish for bilateral neutral freeze:

- exact `source_A.jsonl`;
- exact `source_B.jsonl`;
- exact `endpoint_A.jsonl`;
- exact `endpoint_B.jsonl`;
- `EXTRACTION_MANIFEST.json`;
- extractor/tool identity and execution log.

These are neutral selected-case records already permitted to both sides by I1.

## Do not send to RIDI yet

Before both substantive raw-bundle hash commitments, do **not** send:

- CFC mapped per-arm input;
- CFC mapping manifest contents;
- CFC authority manifest contents;
- CFC gates/reasons;
- CFC per-arm outputs;
- derived CFC pair classification;
- CFC interpretation.

CFC may record/freeze those artifacts privately on its own side and communicate only the cryptographic identities and validation status necessary to establish the pre-execution freeze.

## RIDI-side action after neutral receipt

RIDI will independently:
1. rehash all four exact JSONL line files including LF;
2. verify the four frozen selected-row hashes;
3. verify the extraction manifest;
4. freeze the neutral selected specimen identity;
5. construct the RIDI-permitted input under the frozen evaluation definition;
6. record RIDI input hash/version;
7. exchange only pre-execution freeze identities/status with CFC.

Only after both sides confirm pre-execution freeze completeness may substantive execution begin independently.

**Evidence before execution.**

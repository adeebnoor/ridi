# CFC ↔ RIDI Eligible Pool v0.1 — pre-publication receipt check

**Check date:** 2026-09-29  
**Status:** CFC-SUPPLIED POOL BYTES VERIFIED / CFC PUBLIC POOL MIRROR STILL INCOMPLETE / NO SEED / NO CASE SELECTION

## Received eligible-pool bytes

RIDI received a CFC-supplied file named `eligible_pool.tsv` for pre-publication verification.

Exact local verification:

- bytes: **654915**
- lines: **801** (1 header + 800 data rows)
- SHA-256: `ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade`
- unique case IDs: **800**
- unique pair fingerprints: **800**
- duplicate case IDs: **0**
- duplicate pair fingerprints: **0**

Dataset counts:

- NQ: **250**
- HotpotQA: **250**
- FEVER: **150**
- SciFact: **150**

The received bytes therefore match the frozen eligible-pool digest exactly.

## CFC public branch check

CFC branch observed:

`iller1/cfc-ai-evaluation@freeze/cfc-ridi-eligible-pool-v0.1`

Observed branch head at this check:

`a31e86cab8ee2c34f4e392fae370c3e2d8651313`

The branch already contains byte-identical mirrors of the RIDI-side freeze metadata:

- `research/cfc-ridi-eligible-pool-v0.1/ELIGIBLE_POOL_FREEZE_RECORD.md`
  - Git blob: `276155f4c7a03b25067b2d0bc3bd386f37402cfd`
  - identical to the RIDI freeze-record blob.
- `research/cfc-ridi-eligible-pool-v0.1/POOL_SHA256_FROZEN.txt`
  - Git blob: `5c8b3643732638b3ad0d9ecb4baa973bfa936f04`
  - identical to the RIDI frozen-manifest blob.

At the time of this check, the CFC branch tree does **not** yet contain the exact `eligible_pool.tsv` payload. Therefore the bilateral exact-byte pool mirror is not yet complete.

## Boundary

Receipt and local hash verification do not substitute for public CFC publication.

No seed may be generated, committed or revealed, and no case may be selected, until:

1. CFC publishes the exact `eligible_pool.tsv` bytes;
2. the published file independently verifies to SHA-256
   `ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade`;
3. CFC publishes its final mirror record/commit; and
4. RIDI verifies that public record and exact-byte identity.

**Evidence before selection.**

# CFC–RIDI v0.2 — Bilateral Exact-Hash Closure of Phase F Neutral Schema R1

**Closure date:** 2026-10-01  
**Status:** BILATERALLY ACCEPTED / NEUTRAL-SCHEMA EXACT-HASH CLOSED / F2 MAY BEGIN  
**Authority:** signed F0 feasibility workplan  
**F1 status:** bilaterally accepted

## 1. Exact artifact accepted

Artifact:

`collaboration/cfc-ridi/v0.2/PHASE_F_NEUTRAL_ARM_SCHEMA_DRAFT_R1.json`

RIDI review branch:

`review/cfc-ridi-v0.2-neutral-schema-r1`

Exact identity:

- bytes: `10353`
- SHA-256: `d609a6d6af94d1108048360a349edb612b65b95336d5f90e6874c4da022b60a0`
- Git blob: `c2d85835897350d9a10260e9febfbfa01d10eea6`
- line endings: LF only
- terminal LF: yes

RIDI confirms acceptance of this exact artifact identity without amendment.

## 2. CFC independent acceptance

CFC independently reviewed and accepted the same exact artifact identity in:

`collaboration/cfc-ridi/v0.2/PHASE_F_NEUTRAL_SCHEMA_R1_CFC_REVIEW.md`

CFC repository:

`iller1/cfc-ai-evaluation`

CFC review commit:

`64e9d811aa3c0fd938a096fe419884ac86da151b`

CFC result:

`PHASE_F_NEUTRAL_SCHEMA_R1_CFC_REVIEW_PASS`

The CFC review reproduced the same bytes, SHA-256 and Git blob and found R1 consumable under the accepted F1 boundary without hidden case-specific semantic assumptions.

## 3. Accepted semantic boundary

This closure accepts the schema contract only.

In particular:

- one mapping unit exposes one arm only;
- `recorded_endpoint.canonical` is bounded to the candidate conclusion role only;
- endpoint values, source/query text, passage text, IDs, hashes, dataset/task labels, model identifiers and source bindings do not establish authority, correctness, semantic support, independence, provenance, scope, freshness, epistemic role, evidence polarity or decision `as_of` state;
- missing semantic/authority state remains missing;
- positive authority, if later used, must come only through the separately frozen F4 authority universe and its frozen applicability/binding rules;
- no field absent from R1 may be invented by F2;
- no controller-facing class or method outside the bilaterally accepted F1 interface may be used by F2.

Any required schema or F1-interface expansion requires a versioned amendment and renewed bilateral exact-hash acceptance before use.

## 4. Source-corpus verification boundary

R1 binds:

`contexts_800.jsonl`

SHA-256:

`1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`

The current RIDI pre-send review records the 1,600-row R1 field-presence audit. CFC's current review did not claim to rerun that audit; it relied on continuity to the same exact corpus identity independently verified during v0.1 source recovery. This limitation is preserved unchanged.

## 5. Bilateral closure

The required sequence was:

**F1 signed → neutral-schema exact-hash acceptance → F2.**

CFC exact-hash acceptance is recorded at commit `64e9d811aa3c0fd938a096fe419884ac86da151b`.

RIDI now confirms and accepts the same exact neutral-schema identity.

Therefore:

`PHASE_F_NEUTRAL_SCHEMA_R1_BILATERAL_EXACT_HASH_CLOSED`

This record closes the neutral-schema gate only. It does not itself claim F2 implementation, F3 validation, F4 authority completion, or substantive CFC/RIDI execution.

F2 may begin only from this closed baseline and must preserve the accepted F0/F1/schema boundaries.

# CFC ↔ RIDI neutral handoff — RIDI independent verification

**Verification date:** 2026-09-29  
**Selected case:** `RAG-nq-test1035`  
**Status:** NEUTRAL HANDOFF VERIFIED / RIDI INPUT FREEZE PERMITTED / NO SUBSTANTIVE EXECUTION

## Public CFC chronology

- ZIP publication commit: `6930975339820dc8344a55ae1cb46f6121791804`
- handoff-record commit: `bd298684758da04570ab451277fcebb544fb5ae0`
- handoff-record direct parent: `6930975339820dc8344a55ae1cb46f6121791804`
- ZIP Git blob: `ed40be0fb1fb237ae16320bf23842565f248de0f`

## Independent ZIP verification

Public archive:

`research/cfc-ridi-instantiation-v0.1/CFC_RIDI_RAG-nq-test1035_I1_NEUTRAL_HANDOFF_v0.1.zip`

Independent RIDI verification:

- bytes: **5271**
- SHA-256: `f6845736496c51d5407ddfe46481a07a8d7ee43eb4735e3c23aee934607b3b56`
- ZIP opens successfully;
- exactly 8 archive members;
- no CFC mapped input, authority manifest, gates/reasons, outputs or interpretation present.

## Exact neutral selected records

| member | bytes | SHA-256 | LF terminated |
|---|---:|---|---|
| `source_A.jsonl` | 994 | `60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734` | YES |
| `source_B.jsonl` | 993 | `018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308` | YES |
| `endpoint_A.jsonl` | 382 | `e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67` | YES |
| `endpoint_B.jsonl` | 379 | `e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5` | YES |

Result: **4/4 MATCH** with the frozen selected-row bindings.

## Manifest and extractor verification

- `EXTRACTION_MANIFEST.json` SHA-256:
  `dd570c50f2746512f90fcb407fbc403cdc17f2afae677c2e1ab740e9f65cf3a7`
- archived extractor bytes: **3035**
- archived extractor SHA-256:
  `05037e140d58f508413871827537e5b207555da1f9639ea48bd7a53d7972c669`
- independently computed Git blob identity of archived extractor:
  `8b506b2d540923e036b6a2c222948e4b8cc3bd6d`

That Git blob identity exactly matches the RIDI extractor published at commit
`338ac387459d64a466c1df84256f476d92ca4a09`.

The extraction log reports PASS and the manifest entries agree with independently recomputed member sizes/hashes.

## Provenance boundary

This verification establishes exact identity of the selected records relative to the previously reviewed transport. It does not remove or expand the already documented upstream provenance limitation concerning the original source archives/preregistration beyond that reviewed transport.

## I1 boundary

RIDI has not received or inspected any CFC mapped input, authority manifest, CFC gate/reason, CFC output or CFC interpretation.

The next permitted RIDI-side step is exact input/version freeze. Substantive execution remains prohibited until CFC separately reports its private M1/A1/I1 input-freeze identities and validation status.

**Evidence before execution.**

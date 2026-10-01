# CFC ↔ RIDI v0.2 — Phase F neutral-schema R1 pre-send review

**Review date:** 2026-10-01  
**Status:** DRAFT FOR BILATERAL NEUTRAL-SCHEMA REVIEW ONLY / NO F2 AUTHORIZED  
**F1 status:** BILATERALLY ACCEPTED  
**F1 baseline:** CFC Anchor 0.2.90rc1  
**F1 interface SHA-256:** `b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184`

## Exact schema artifact

File:

`PHASE_F_NEUTRAL_ARM_SCHEMA_DRAFT_R1.json`

Exact identity:

- bytes: `10353`
- SHA-256:
  `d609a6d6af94d1108048360a349edb612b65b95336d5f90e6874c4da022b60a0`
- Git blob:
  `c2d85835897350d9a10260e9febfbfa01d10eea6`
- line endings: LF only
- terminal LF: yes

## Source basis independently checked

Registered source corpus:

`contexts_800.jsonl`

- exact corpus SHA-256:
  `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`
- rows: `1600`
- candidate pairs: `800`
- NQ: 250 cases / 500 arm rows
- HotpotQA: 250 cases / 500 arm rows
- FEVER: 150 cases / 300 arm rows
- SciFact: 150 cases / 300 arm rows
- source tasks: `qa`, `verdict`
- every source arm contains exactly 10 passages
- all 1600 rows contain the source fields required to construct the source side of this schema.

The registered source corpus itself also contains fields intentionally **not exposed** to the F2 adapter schema:
- `gold`;
- `passages[].grade`;
- full prompt text;
- `condition` (reference/random).

Their omission is deliberate.

## One-arm visibility rule

The neutral schema is an **arm-level** schema, not a pair-level schema.

One mapping operation receives exactly one arm instance.

The counterpart arm is not part of the schema.

The schema prohibits supplying or computing through the adapter:
- RIDI PASS/FAIL;
- endpoint equality/difference;
- correctness;
- gold labels;
- expected asymmetry;
- publication-interest labels;
- retrieval grades.

This prevents the mapping layer from conditioning authority/representation on the eventual cross-arm comparison.

## Exact-source naming rule

R1 preserves frozen source terminology wherever practical:

- `question`, not a renamed semantic field;
- `passages[].docid`;
- `passages[].text`;
- endpoint `raw`;
- endpoint `canonical`;
- endpoint `model`;
- endpoint `revision`;
- endpoint `source_generations_sha256`.

The schema adds only mechanical binding fields such as SHA-256 values and passage ordinals.

## Candidate-claim boundary

Only:

`recorded_endpoint.canonical`

is eligible to enter CFC as the candidate claim/conclusion value.

This does **not** make the endpoint:
- evidence;
- semantic support;
- authority;
- correctness;
- provenance;
- independence evidence.

The raw endpoint remains audit/provenance material only.

## Evidence/authority boundary

The neutral schema supplies exact source content and immutable bindings only.

It supplies **no positive authority record**.

In particular, source/query text, passage text, doc IDs, hashes, dataset/task labels, model identifiers and case/arm IDs do not establish:
- identity authority;
- semantic-support authority;
- evidence authority;
- provenance authority;
- epistemic role;
- scope/applicability;
- freshness;
- failure-domain topology;
- support-set independence.

Any positive authority later used must come from the separately frozen F4 authority universe and pass its frozen applicability/binding rules.

Missing authority remains missing.

## Identity/temporal limitation retained

The neutral schema intentionally does not invent:
- authoritative entity/event/version identity;
- evidence polarity;
- epistemic role;
- lineage/dependency;
- decision `as_of` semantics;
- scope applicability.

If the accepted F1 interface plus later F4 authority records cannot supply required state faithfully, Phase F must stop under the already signed NO-GO semantics.

## Endpoint-contract basis

The endpoint object uses the exact field names already present in the frozen v0.1 neutral endpoint records and consumed by the frozen RIDI selected-case runner.

This review does **not** claim a new substantive endpoint result, endpoint equality, or correctness.

No RIDI runner has been executed for v0.2.

## Interface-change guard

The accepted F1 interface remains the maximum controller-facing surface.

If the future adapter requires a CFC public class/method outside that accepted interface:
- stop;
- version the F1 interface;
- obtain renewed bilateral F1 acceptance before use.

If F2 requires a neutral-schema field absent from R1:
- stop;
- version this schema;
- obtain renewed bilateral neutral-schema acceptance before use.

## Review decision

Current status:

`NEUTRAL_SCHEMA_R1_READY_FOR_CFC_REVIEW`

This means only that RIDI is proposing the exact artifact above for CFC independent review.

It does **not** authorize adapter implementation.

Under signed F0:

**F1 signed → neutral-schema exact-hash acceptance → F2.**

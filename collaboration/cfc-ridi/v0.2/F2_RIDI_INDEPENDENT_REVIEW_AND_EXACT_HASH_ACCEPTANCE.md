# CFC–RIDI v0.2 — RIDI Independent F2 Review and Exact-Hash Acceptance of Candidate Adapter v0.1

**Review date:** 2026-10-01  
**Status:** RIDI REVIEW PASS / RIDI EXACT-HASH ACCEPTANCE / PENDING CFC F2 COUNTERSIGN  
**Authority:** signed F0 feasibility workplan  
**F1 status:** bilaterally accepted  
**Neutral schema R1:** bilaterally exact-hash closed  
**F2 reporting convention:** bilateral and operative

## 1. Candidate reviewed

CFC review branch:

`review/cfc-ridi-v0.2-f2-adapter-v0.1`

Candidate head commit:

`4167783eb48e1a1677107cb1359ad9b2f890017f`

Pre-F2 base:

`c8eb82fbae4f78ac11cab2ef49db3d21af78e722`

Independent RIDI comparison reproduced:

- branch status: 4 commits ahead / 0 behind;
- exactly four added files;
- all four files are under `collaboration/cfc-ridi/v0.2/f2_adapter/`;
- no controller or unrelated repository file is modified.

## 2. Exact artifact identities independently reproduced

### adapter.py

- bytes: `28972`
- SHA-256: `4b975fda6242c9a7e33d0d692705ef6fe82683dbf2bddefc0345c2e5504b480a`
- Git blob: `85bd07b602d3555a306a5200457704fcfa0bffe3`

### test_adapter.py

- bytes: `6586`
- SHA-256: `4f70526185dbb69e4073c0baf89a6f924e8e1e220ba0317c339708bf5b152f34`
- Git blob: `04af56414b7aa370d67f31a12e2e0fa3a1be9845`

### README.md

- bytes: `3479`
- SHA-256: `3bf666564b2c1a7f85526a3e223e7385e30a61c73e8d5f67ca0b17d954d7638a`
- Git blob: `2d3e763ebf83b9be5edc21bf9a4cb4a9d2efa606`

### ADAPTER_MANIFEST.json

- bytes: `1348`
- SHA-256: `32b8c36ebb434fa620cdae970ed12bbb389a1ae62d20be6005e78b7c0db89591`
- Git blob: `b34b948c15c453b7d35ecfaf8429af0616150987`

Result:

`RIDI_F2_EXACT_IDENTITY_PASS`

## 3. F1/interface boundary review

RIDI reviewed the exact adapter source against the bilaterally accepted F1 interface manifest:

- F1 interface SHA-256:
  `b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184`
- Anchor wheel SHA-256:
  `b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`
- neutral schema R1 SHA-256:
  `d609a6d6af94d1108048360a349edb612b65b95336d5f90e6874c4da022b60a0`

The adapter's declared package-level symbols match the accepted F1 class list exactly.

The adapter's declared Controller-method allowlist matches the accepted F1 method list exactly.

Static source inspection found no:
- `cfc_anchor._engine` or other private Anchor import;
- private Controller attribute access;
- unapproved Controller method call;
- monkeypatch path;
- `sys.modules` injection;
- dynamic private import path;
- controller modification path;
- alternate controller path;
- case-ID-specific execution branch.

The exact Controller methods actually called by the adapter are a subset of the accepted F1 method surface.

Result:

`RIDI_F2_STATIC_BOUNDARY_AUDIT_PASS`

## 4. Neutral-schema boundary review

RIDI confirms that the exact candidate:

- validates one neutral arm at a time;
- requires the exact neutral-schema root/subobject key sets;
- rejects hidden/extra root fields;
- requires the frozen source-corpus identity;
- checks question and passage text SHA-256 bindings;
- requires exactly ten ordered passage records;
- carries `recorded_endpoint.canonical` as the candidate conclusion;
- does not promote `recorded_endpoint.raw`, query text or passage text into authority state;
- emits unresolved semantic-state markers before later external resolution;
- emits `authority_state = NOT_ASSERTED_BY_NEUTRAL_SCHEMA`;
- emits `substantive_execution_authorized = False` during neutral preparation;
- requires externally supplied resolved semantic/authority state before Controller execution.

The candidate itself contains no verifier implementation and creates no substantive authority record.

## 5. Independent public-test rerun

RIDI created a separate GitHub Actions verification path on:

`review/cfc-ridi-v0.2-f2-independent-review`

Expanded verification workflow commit:

`8fd8987502eec344e8e0e95e76988fb093997fcd`

Successful independent run:

`36853204619`

The run independently fetched the four candidate files from the exact CFC candidate commit and then:

1. reproduced all four byte lengths;
2. reproduced all four SHA-256 values;
3. reproduced all four Git blob identities;
4. compiled `adapter.py` and `test_adapter.py`;
5. reran the published representation suite;
6. reran an independent AST/static F1-boundary audit;
7. performed a positive public-interface probe against the exact frozen Anchor wheel.

Published representation tests independently reproduced:

`PASS 8/8`

Result:

`RIDI_F2_PUBLIC_TEST_RERUN_PASS`

## 6. Positive exact-Anchor public-interface probe

RIDI independently used the public CFC Demonstrator v1.0-rc1 release, whose release archive identity was checked before extraction.

The exact wheel found and verified was:

`cfc_anchor-0.2.90rc1-py3-none-any.whl`

Wheel bytes:

`211808`

Wheel SHA-256:

`b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`

The wheel was installed into a clean temporary Python environment without dependencies.

The candidate's `public_interface_probe(...)` then independently confirmed:

- exact wheel SHA-256 enforcement;
- all accepted F1 public symbols present;
- all accepted F1 Controller methods present;
- `private_engine_accessed = false`.

Result:

`RIDI_F2_POSITIVE_PUBLIC_INTERFACE_PROBE_PASS`

## 7. Non-blocking downstream validation boundary

This F2 acceptance is intentionally limited.

It does not establish that a future F4/F5 resolved-state package is substantively valid, correctly scoped, correctly time-bound, independent, or backed by qualifying real authority.

In particular, F3 should adversarially test at least:

- cross-case or cross-arm resolved-state substitution;
- wrong claim-identity binding;
- scope/applicability mismatch;
- decision-`as_of` mismatch;
- provenance/lineage dependency erasure;
- false independence from distinct-looking identifiers;
- support-count/independence mismatch;
- host-trust verifier/authority mismatch;
- reordered or incorrectly rebound passage authority state;
- hidden fallback or semantic promotion under malformed resolved state.

F4/F5 remain responsible for freezing and validating the real authority universe, provenance, applicability and exact case/state binding.

These are downstream validation requirements, not reasons to alter the exact F2 candidate before F3.

## 8. RIDI F2 decision

RIDI finds no F2 implementation-boundary violation in candidate adapter v0.1.

RIDI therefore explicitly accepts the exact candidate identities listed above.

Result:

`F2_CANDIDATE_ADAPTER_V0_1_RIDI_REVIEW_PASS`

and

`F2_CANDIDATE_ADAPTER_V0_1_RIDI_EXACT_HASH_ACCEPTED`

This is F2 candidate acceptance only.

It is not:
- F3 acceptance;
- F4 authority-universe acceptance;
- F5 calibration acceptance;
- substantive CFC/RIDI execution approval.

Under the signed F0 bilateral-acceptance rule, F2 exact-hash closure remains pending explicit CFC acceptance/countersign of the same exact candidate identity after this RIDI review.

No F3 implementation/test freeze begins before that F2 bilateral closure is recorded.

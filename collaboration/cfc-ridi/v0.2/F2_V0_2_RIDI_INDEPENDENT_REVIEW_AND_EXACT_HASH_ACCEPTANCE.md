# CFC–RIDI v0.2 — RIDI Independent F2 v0.2 Review and Exact-Hash Acceptance

**Review date:** 2026-10-01  
**Status:** RIDI REVIEW PASS / RIDI EXACT-HASH ACCEPTANCE / PENDING CFC COUNTERSIGN  
**Authority:** signed F0 feasibility workplan  
**Repair target:** reproduced F3-T05 cross-case / cross-arm resolved-state substitution failure

## Candidate reviewed

Candidate:

`CFC-RIDI-F2-ADAPTER-v0.2`

CFC candidate commit:

`930d7b0119159eaedbaf947691d9510b4c61d81c`

Prior failed v0.1 candidate remains unchanged at:

`4167783eb48e1a1677107cb1359ad9b2f890017f`

## Exact candidate identities independently reproduced

### adapter.py

- bytes: `30630`
- SHA-256: `15b7d01787237b2e5f0d1ca106c4e84aaf1976a2512179c79c458fe3d80e634b`
- Git blob: `373598e8774622cc91d43b811eb636a231bd906c`

### test_adapter.py

- bytes: `8853`
- SHA-256: `3798cfb0b9c79311cb74b4bd5be71c2805ff225d316a57f2fb55c2d8462fd732`
- Git blob: `81d948ef8cc19ad471eeb05121fa64f7a885e6aa`

### README.md

- bytes: `3891`
- SHA-256: `0c441a05b75c62b827c69c0d40a83d7ede02b66d40b757156e3ddcec4d070ba7`
- Git blob: `55df7702ed90f6134762136171e5557cdde692a2`

### probe_public_api.py

- bytes: `730`
- SHA-256: `cf330aabe63cb5b1722bdbffc0ec92980e4d312cbcdf771c69c7fff6b4a2622a`
- Git blob: `4125a52565edc69a026ddd646cdd32880e68a137`

### ADAPTER_MANIFEST.json

- bytes: `2125`
- SHA-256: `6e56866ac5d6ee7eddc82a06d8c172cb886d38d98f2e7fa1fa76d3afa03aa264`
- Git blob: `2bb1efff7b5da612c77a86afae8f0f90c5dac402`

Result:

`RIDI_F2_V02_IDENTITY_PASS`

## Repair review

RIDI confirms that v0.2 adds a deterministic root-level:

`neutral_arm_binding`

The exact binding includes:

- binding version;
- neutral-schema SHA-256;
- case ID;
- arm;
- dataset;
- task;
- draw;
- question SHA-256;
- registered-context-line SHA-256;
- endpoint-record SHA-256;
- candidate-conclusion SHA-256;
- canonical SHA-256 of the ordered passage-binding set.

The required resolved-state package must contain the exact binding derived from the already validated neutral arm.

The adapter performs this comparison inside `_validate_resolved_state(...)`.

The binding check occurs before:
- Anchor public-API loading;
- host-trust construction;
- Controller construction;
- any Controller evaluation call.

A mismatch raises `BindingError`.

RIDI therefore confirms that the v0.2 repair directly addresses the previously reproduced F3-T05 substitution path at the F2 representation boundary.

## Narrow-change review

Relative to v0.1 adapter source, RIDI observed only:

- adapter version increment from v0.1 to v0.2;
- addition of `neutral_arm_binding(...)`;
- inclusion of that binding in authority requirements and execution output;
- requirement and validation of the binding in resolved state;
- addition of the prohibition against resolved-state reuse across case/arm.

No prior v0.1 representation guard was removed.

No F1 public-interface expansion was observed.

No private Anchor access, monkeypatching, private-state injection, controller modification or case-specific outcome branch was observed.

Neutral Schema R1 and the frozen F3 criteria remain unchanged.

## Independent RIDI execution

RIDI GitHub Actions workflow:

`CFC-RIDI F2 v0.2 independent RIDI review`

Run ID:

`36886429562`

RIDI workflow commit:

`97deb1f40bd6d77bb4aabf837eceef5a63f1ecf8`

Independent results:

`RIDI_F2_V02_COMMIT_PASS`

`RIDI_F2_V02_IDENTITY_PASS`

`RIDI_F2_V02_ANCHOR_IDENTITY_PASS`

Published representation suite independently reproduced:

`PASS 10/10`

Result:

`RIDI_F2_V02_TESTS_PASS`

## Independent public-interface probe

RIDI ran the candidate-supplied `probe_public_api.py` against the exact frozen Anchor wheel:

`cfc_anchor-0.2.90rc1-py3-none-any.whl`

Anchor wheel SHA-256:

`b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`

Result:

`PUBLIC_INTERFACE_PROBE_PASS`

and:

`RIDI_F2_V02_PUBLIC_INTERFACE_PASS`

The accepted F1 public-interface identity remains:

`b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184`

## Additional RIDI binding-field audit

RIDI independently mutated every root binding component one at a time and confirmed rejection for all of:

- binding_version;
- neutral_schema_sha256;
- case_id;
- arm;
- dataset;
- task;
- draw;
- question_sha256;
- registered_context_line_sha256;
- endpoint_record_sha256;
- candidate_conclusion_sha256;
- passage_bindings_sha256.

RIDI also independently applied a foreign case+arm root binding while keeping compatible passage-level bindings and reproduced `BindingError`.

Result:

`RIDI_F2_V02_ALL_BINDING_FIELDS_REJECT_MISMATCH_PASS`

Static boundary result:

`RIDI_F2_V02_STATIC_BOUNDARY_PASS`

## RIDI decision

RIDI finds no F2 implementation-boundary violation in v0.2 and accepts the exact candidate identity above.

Results:

`F2_ADAPTER_V0_2_RIDI_REVIEW_PASS`

`F2_ADAPTER_V0_2_RIDI_EXACT_HASH_ACCEPTED`

This is not bilateral F2 closure yet.

CFC must explicitly countersign the same exact v0.2 identity.

After bilateral F2 v0.2 closure, the only permitted next step is a complete rerun of frozen F3 T01–T15 under the unchanged F3 criteria.

No F4 progression is authorized before F3 passes.

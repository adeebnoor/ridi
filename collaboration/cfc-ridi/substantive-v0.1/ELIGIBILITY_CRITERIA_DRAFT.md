# Eligible candidate pool criteria v0.1

**Status: DRAFT — NOT FROZEN**

These criteria are intentionally outcome-independent. They must be jointly approved and frozen before any substantive selection seed is created.

## Inclusion criteria

A candidate pair may enter the pool only if all of the following are true before selection:

1. **Stable pair identity.** The case has one unique ASCII `case_id` and exactly two arms, A and B.
2. **Immutable source reference.** The source specimen for each arm can be identified by immutable bytes or a stable public/versioned record, with SHA-256 recorded.
3. **Fixed RIDI evaluation premise.** The evaluation definition used to declare A/B equivalent is already defined and can be applied mechanically without seeing CFC output.
4. **Recorded downstream endpoint.** A recorded or permitted offline verdict/action exists for both arms so the frozen RIDI primary endpoint can be evaluated without causing a blocked real-world action.
5. **One-support compatibility.** There is no authoritative original decision rule requiring more than one independent support. Any candidate with an explicit authoritative requirement >1 is ineligible for this first experiment.
6. **M1 representability.** The neutral source fields required by frozen M1 can be represented honestly, including explicit absent-field handling. Missing authority facts may remain NOT_SUPPLIED; they are not repaired.
7. **A1 authority boundary available.** Any authority evidence to be inspected already exists within the pre-frozen A1/I1 boundary. No post-selection discretionary authority assertion is needed to make the case run.
8. **I1 inspection compatibility.** The case can be executed while respecting the frozen pre-commit inspection matrix.
9. **No consequential execution.** RIDI can use recorded/offline downstream outputs if CFC blocks; no live business, clinical, financial or other consequential action is required.
10. **No outcome-based eligibility.** Inclusion does not depend on a predicted or known CFC ALLOW/BLOCK result, RIDI PASS/FAIL result, desired asymmetry, correctness label, or publication value.
11. **Prior exposure recorded.** Any prior public appearance of the case or its A/B outcome is recorded as metadata. Prior exposure is not silently ignored.
12. **No substantive case chosen in advance.** Eligibility rationale is documented before commit–reveal selection and must not identify a preferred case.

## Exclusion criteria

Exclude a candidate if any of the following is known before pool freeze:

- authoritative original support requirement >1;
- missing/unstable A or B source identity;
- no fixed evaluation premise;
- no recorded/permitted offline downstream endpoint;
- M1 cannot faithfully encode the case even with NOT_SUPPLIED handling;
- required authority would have to be newly invented, solicited or edited after selection;
- execution would require violating I1;
- execution would require a prohibited real-world action;
- eligibility depends on known/expected CFC or RIDI output;
- duplicate canonical case ID or duplicate source specimen under another ID.

## Explicit non-exclusions

The following do **not** by themselves exclude a case:

- missing authority that frozen M1/A1 can honestly represent as NOT_SUPPLIED;
- expected possibility of CFC BLOCK;
- expected possibility of RIDI PASS or FAIL;
- unknown correctness;
- a null, negative or NOT EVALUABLE final result, provided the case was eligible under the pre-selection rules.

## Frozen pool format

When jointly approved, the pool is written as exact UTF-8, LF-terminated `eligible_pool.tsv`, sorted lexicographically by `case_id`.

Required columns:

`case_id	source_a_sha256	source_b_sha256	source_ref_a	source_ref_b	evaluation_definition_id	offline_endpoint_present	original_support_requirement	prior_public_exposure	eligibility_rationale`

The exact file SHA-256 identifies the frozen pool.

This draft does not contain any candidate IDs.

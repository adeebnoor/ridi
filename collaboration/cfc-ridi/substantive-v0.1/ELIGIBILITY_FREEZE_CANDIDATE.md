# CFC ↔ RIDI Eligibility Gate v0.1 — Freeze Candidate Record

**Status:** FREEZE CANDIDATE — NOT FROZEN  
**Date:** 2026-09-28  
**Purpose:** Exact-byte candidate for bilateral eligibility-gate freeze before any candidate registry is populated.

## Exact artifacts proposed for freeze

| Artifact | Bytes | SHA-256 | Git blob SHA |
|---|---:|---|---|
| `ELIGIBILITY_CRITERIA_DRAFT.md` | 9,268 | `b766a0452af82343fe7ee33dbe8dfb7ccb0a1d557f6d0ccaf14676eefb827e8a` | `9392e8b4241bc5bf308c380607675d3a8641b214` |
| `candidate_registry_TEMPLATE.tsv` | 414 | `12992e3c8591d41dc2dc38de0ebe46e8c491d3a39e242d6021286e1815b5fd29` | `a27549f3b182b42be6e2cf828785cf0784b84450` |
| `eligible_pool_TEMPLATE.tsv` | 269 | `128a74efb1921e6c57a6cc02145b6e8facf1ff40c9dde36fd62b950cdc7d4f26` | `7db73a5d0534cda97bda1210816e4704f84c4222` |
| `tools/eligibility_check.py` | 11,388 | `96ca16e12e3f2fecb5a06998eb28476e250b2a0965f2b26713da298391958904` | `d3df8cb5bc1fa9e024e98b9d728e2c03077351cd` |

## Narrow checker correction after independent review

The previously proposed checker hash `c5e7cc59...` is superseded and must **not** be frozen.

The current checker now parses candidate-registry TSV rows as a canonical byte-oriented format rather than permissive CSV. It rejects:
- extra fields;
- missing fields;
- embedded tab delimiters;
- blank rows;
- multiline/noncanonical row shapes.

For accepted canonical input, `registry_row_sha256` is computed from the exact original UTF-8 row bytes including its terminating LF, not from reconstructed declared fields.

Negative regression tests cover extra fields, missing fields and embedded delimiters, plus a direct assertion that the audit row hash equals the SHA-256 of the original source-line bytes.

Latest checker-correction CI:
https://github.com/adeebnoor/ridi/actions/runs/36356315694

Result: **PASS**

## Clarifications incorporated

1. `UNKNOWN` original support requirement is distinct from `AUTHORITATIVE_1` and is ineligible for this first bounded experiment until resolved using permitted pre-selection evidence.
2. Each arm binds source/specimen SHA-256 and recorded offline-endpoint SHA-256 separately. The evaluation definition has both a stable identifier/version and immutable SHA-256.
3. Duplicate handling is order-independent: the same A/B pair, including reversed A/B under another ID, receives the same pair fingerprint and cannot create an additional selection entry. Sharing one arm with an otherwise distinct pair does not by itself create a duplicate.
4. Eligibility is determined mechanically from permitted pre-selection fields only. The checker preserves ACCEPT/REJECT, ordered reason codes, registry-row hash and checker hash. It does not execute CFC or RIDI, compare A/B verdicts for equivalence, inspect hidden correctness or rank cases by scientific interest.

## Mechanical checker behavior

The checker:
- computes per-arm bindings from source + offline endpoint hashes;
- computes an order-independent pair fingerprint;
- rejects `AUTHORITATIVE_GT1` and `UNKNOWN`;
- rejects invalid/missing frozen fields;
- detects reversed duplicate registrations;
- allows a shared single arm across otherwise distinct pairs;
- records metadata conflicts rather than silently choosing between them;
- emits a complete eligibility audit plus only ACCEPT rows into the pool.

No manual override is permitted by the proposed criteria.

## Verification

Latest infrastructure CI incorporating these clarifications:

https://github.com/adeebnoor/ridi/actions/runs/36356315694

Result: **PASS**

Test coverage includes:
- UNKNOWN support requirement rejection;
- authoritative >1 rejection;
- reversed-pair duplicate detection;
- shared-one-arm non-duplicate behavior;
- duplicate metadata-conflict rejection;
- evaluation-definition hash and pair-fingerprint validation;
- exact registry schema/LF behavior;
- deterministic selection;
- deterministic raw-bundle bytes.

## State

- candidate registry rows: **0**
- eligible pool rows: **0**
- substantive case selected: **false**
- selection seed created: **false**
- substantive CFC/RIDI execution: **false**

Bilateral approval of the exact four artifacts above is required before the eligibility gate is labeled FROZEN and before any real candidate registration is added.

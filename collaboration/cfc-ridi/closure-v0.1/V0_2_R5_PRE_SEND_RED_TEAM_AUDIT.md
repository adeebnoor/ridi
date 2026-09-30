# CFC ↔ RIDI v0.2 DRAFT R5 — pre-send red-team audit

**Audit status:** PASS FOR BILATERAL REVIEW / NOT PASS FOR PROTOCOL FREEZE / NOT PASS FOR IMPLEMENTATION / NOT PASS FOR ELIGIBILITY OR EXECUTION

## Audit objective

Test whether the draft still permits the main v0.1 failure mode:

> freeze/select first, then discover that source, authority, adapter or controller-interface constraints make faithful execution impossible.

## Checks

| Risk | R5 control | Audit |
|---|---|---|
| Controller version changes after work begins | F1 exact baseline + Section 12 immutability | PASS |
| Implementation assumptions differ between parties | F0 bilateral feasibility-workplan sign-off | PASS |
| Synthetic custom-case fixtures become substantive authority | F2/F3/F5 explicit nonfixture prohibition | PASS |
| Adapter invents evidence/semantic support/authority | F3 adversarial representation-only suite | PASS |
| Private/monkeypatched bypass used to make CFC run | F2 explicit interface/monkeypatch restriction | PASS |
| Source bytes missing after selection | Phase A1 durable source-universe freeze before eligibility | PASS |
| Temporary transport expires mid-experiment | A1 durable-route requirement | PASS |
| Authority records searched/found after selection | F4 cutoff + F4→A2 continuity rule; any membership/semantic change resets Phase F | PASS |
| Authority applicability decided after selection | A3 frozen acceptance/binding/conflict/missing rules | PASS |
| Validity/freshness changes because date moves | A4 temporal/as-of freeze | PASS |
| Claim/scope rewritten after selected case is known | A5 claim/decision-context contract | PASS |
| Original support requirement silently weakened | A6 support-requirement contract | PASS |
| Adapter tuned to v0.1 selected case | Section 3 case-agnostic exposure firewall; no case-ID special exception | PASS |
| Calibration cases leak into substantive pool | Section 3 permanent CALIBRATION/EXCLUDED rule | PASS |
| Feasibility/calibration cases handpicked after outcome inspection | F5 deterministic authority-state-based case-selection rule + frozen IDs/hashes before execution | PASS |
| Missing-authority representability discovered after selection | F5-B + E3/E4 before seeds | PASS |
| Eligibility peeks at CFC/RIDI outcomes | E1/E2 mapping-only eligibility | PASS |
| Eligibility checker calls CFC closure | E2 explicitly prohibited | PASS |
| Candidate omissions hidden before eligibility audit | E5 complete candidate source-frame manifest frozen before checker; rejected cases/reasons retained | PASS |
| Pool built before executable path proven | F/A/D/P occur before E | PASS |
| Bundle/commit/exchange machinery fails only after substantive run | D3 excluded plumbing rehearsal | PASS |
| Selected-case gate becomes first discovery | Section 10 requires exact eligibility-classification reproduction | PASS |
| Newly released CFC version substituted late | Section 12 reset required | PASS |
| Authority contents disclosed contrary to independence boundary | Section 13 pre-freeze I1 content-access rule | PASS |
| Quiet repair/reselection | Section 14 explicit reset/no-go | PASS |

## Known unresolved items — intentionally gated, not protocol omissions

R5 does **not** claim these are already solved:

1. Exact v0.2 CFC baseline has not been selected.
2. A compliant nonfixture substantive adapter has not yet been demonstrated.
3. A real complete-authority calibration case has not yet been identified/verified.
4. Missing-authority behavior of the selected baseline/adapter has not yet been demonstrated.
5. The substantive authority universe has not yet been frozen.
6. v0.2 M1/A1/I1 do not yet exist as frozen artifacts.

These are exactly the Phase F/A deliverables. Failure of any one stops v0.2 before eligibility or seeds.

## CFC implementation facts checked before this audit

Public CFC records show:
- the existing custom-case runner uses `SYNTHETIC_CUSTOM_FIXTURE` trust;
- the v0.1 anchor has documented public-surface decision-accounting reachability boundaries;
- CFC-next 0.3.0a2 is a separately frozen baseline, but its freeze evidence alone does not establish a nonfixture RIDI-specific adapter.

R5 therefore does not nominate either implementation automatically.

## Final post-hardening check

Additional changes verified after the first audit:

- document title now correctly identifies **DRAFT R5**;
- v0.1 exposure exclusion is expressed as a **case-agnostic contamination rule**, with `RAG-nq-test1035` merely an instance of that rule;
- F4 authority-universe cutoff is explicit;
- F4 authority membership/semantics cannot change on the way to A2 without resetting Phase F;
- F5 calibration cases must be selected by a frozen deterministic authority-state rule before execution;
- E5 freezes the candidate source frame before checker execution and retains rejected candidates/reason codes.

No remaining issue found that would justify another draft revision **before bilateral review**.

## Send recommendation

**Safe to send R5 for review only.**

Do **not** ask for:
- protocol approval;
- annex approval;
- controller freeze;
- adapter implementation start;
- eligibility construction;
- seed generation.

First ask Krzysztof to review R5 and confirm whether the F0 feasibility-workplan structure is acceptable. Only after bilateral F0 agreement should implementation feasibility work begin.

**Review before implementation. Feasibility before protocol freeze.**

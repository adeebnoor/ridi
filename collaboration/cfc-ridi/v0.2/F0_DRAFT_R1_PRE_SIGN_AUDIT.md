# CFC ↔ RIDI v0.2 — F0 DRAFT R1 pre-sign audit

**Audit status:** PASS FOR BILATERAL F0 REVIEW/SIGN-OFF REQUEST ONLY  
**Not authorized:** controller selection / controller modification / adapter development before sign-off / protocol freeze / eligibility / seeds / selection / substantive execution

## Exact artifact audited

- file: `F0_FEASIBILITY_WORKPLAN_DRAFT_R1.md`
- bytes: **16703**
- SHA-256: `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`
- Git blob: `a3b14166230eec9e66716918ddbf324ed19c67df`
- line endings: LF only
- terminal LF: yes

## Krzysztof clarification coverage

| Requested clarification | F0 control | Audit |
|---|---|---|
| Responsibility and verification matrix | Section 2 assigns producer, independent verifier and bilateral acceptance for every Phase F artifact/decision | PASS |
| Predeclared failure semantics | Section 5 names baseline, authority, API, representation, F5-A/F5-B and verification-disagreement stop statuses/actions | PASS |
| Failure remains valid outcome | Section 5 explicitly prohibits relaxing acceptance criteria | PASS |
| Implementation boundary | Sections 1 and 4 separate pre-sign read-only inspection from post-sign bounded Phase F work | PASS |
| No frozen-controller modification | Section 4.1; modified controller becomes a new baseline | PASS |
| No private bypass/monkeypatch | Sections 3.1, 4.2 and 5.3 | PASS |
| No adapter development before signed workplan | Section 1.1 | PASS |

## Additional recurrence-prevention checks

| v0.1 recurrence risk | F0 control | Audit |
|---|---|---|
| Implementation assumptions differ between parties | F0 must be same-hash bilaterally signed before Phase F begins | PASS |
| Baseline chosen implicitly | F0 lists process only; F1 single-baseline nomination is a later bilateral decision | PASS |
| Adapter uses private CFC path | Approved F1 interface only; no hidden/private state injection | PASS |
| Synthetic authority used to make run work | Sections 4, 5 and 6 explicitly prohibit it | PASS |
| Authority created for calibration case | F4/F5 real pre-existing authority only | PASS |
| Authority universe moves after feasibility | F4 cutoff; later membership/semantic change resets Phase F | PASS |
| Calibration cases selected for convenient outputs | Section 7 deterministic selector; prohibited use of framework outputs/correctness/asymmetry | PASS |
| Private authority contents falsely called independently verified | Sections 2.1 and 7 distinguish content-level CFC validation from RIDI manifest/selection reproduction | PASS |
| Adapter repaired after F5 without re-testing | Section 5.4 requires new adapter version + full F3 + both F5-A/F5-B rerun | PASS |
| Failure causes criterion weakening | Section 5 explicitly forbids relaxation | PASS |
| Missing-authority result forced to be “successful” | F5-B may legitimately be EXECUTABLE_MISSING_AUTHORITY or MAPPING_NOT_EVALUABLE; intended requirement fixed before interpretation | PASS |
| Progress despite bilateral disagreement | F6_HOLD_VERIFICATION_DISAGREEMENT blocks progression | PASS |
| Temporary source disappears | Section 6.3 requires durable retrievability/hash verification for F5 source bytes | PASS |

## Intentionally unresolved after F0

F0 deliberately does **not** decide:

1. which CFC controller baseline will be selected;
2. whether any listed baseline is suitable;
3. whether a compliant nonfixture adapter can be built;
4. whether sufficient real authority exists;
5. which calibration cases will be selected;
6. whether missing-authority states are executable;
7. whether Phase F will PASS;
8. any v0.2 eligibility rule, pool, seed or substantive result.

Those are later gated decisions. Their absence from F0 is intentional.

## Sign-off rule

F0 may be called **SIGNED** only if both Adeeb and Krzysztof explicitly approve:

```text
22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e
```

for the exact 16,703-byte `F0_FEASIBILITY_WORKPLAN_DRAFT_R1.md`.

Any byte change invalidates prior approval and requires a new draft identity/hash.

## Recommendation

**Safe to send for F0 workplan review/sign-off only.**

Do not pair the request with:
- a preferred controller;
- adapter code;
- eligibility construction;
- seeds;
- execution instructions.

**Sign the workplan before feasibility implementation. Failure remains evidence.**

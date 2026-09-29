# CFC ↔ RIDI RIDI-side pre-execution input freeze v0.1

**Case:** `RAG-nq-test1035`  
**Status:** RIDI INPUT + RUNNER FROZEN / CFC PRIVATE INPUT-FREEZE STATUS PENDING / NO SUBSTANTIVE EXECUTION

## Neutral handoff

RIDI independently verified the exact CFC-neutral handoff:
- ZIP publication commit: `6930975339820dc8344a55ae1cb46f6121791804`
- CFC handoff record: `bd298684758da04570ab451277fcebb544fb5ae0`
- ZIP SHA-256: `f6845736496c51d5407ddfe46481a07a8d7ee43eb4735e3c23aee934607b3b56`
- four selected JSONL line hashes: **4/4 MATCH**
- extraction manifest SHA-256: `dd570c50f2746512f90fcb407fbc403cdc17f2afae677c2e1ab740e9f65cf3a7`
- extractor Git blob identity: `8b506b2d540923e036b6a2c222948e4b8cc3bd6d`

## Frozen RIDI input

File:

`RIDI_INPUT.json`

Exact UTF-8/LF bytes SHA-256:

```text
0f92f41721a452c7045c4c384d4345ba7335fc5ee724150c880ca2174edf75e0
```

The input contains only I1-permitted RIDI material. Ground-truth correctness and all prohibited CFC-private material remain withheld.

The frozen primary endpoint is the shared-protocol RIDI verdict/action-equivalence endpoint. For this QA case it is mechanically instantiated using the preregistered task-specific canonical outputs already recorded in the neutral endpoint records:

```text
PASS iff canonical_A == canonical_B
FAIL iff canonical_A != canonical_B
NOT_EVALUABLE if a required input/output is absent
```

This is the case-level realization of the preregistered canonical-output-change definition; no new normalization, parser or post-selection threshold is introduced.

## Frozen RIDI runner

File:

`tools/run_ridi_selected_case_v0_1.py`

SHA-256:

```text
a532c605f664d275e8da8e7ae041f5eec45490a37e128d87158bac004c992866
```

Expected Git blob identity from exact bytes:

```text
2102d80569eb9917df1903b80ca9853bd4d81c18
```

The runner:
- verifies the frozen RIDI input SHA-256;
- independently verifies all four neutral JSONL line hashes;
- checks the frozen evaluation entry fields;
- compares only the preregistered canonical downstream strings for the primary endpoint;
- reports context identity differences only as secondary fields;
- withholds correctness and interpretation;
- has no discretionary parameters affecting PASS/FAIL.

## Execution environment lock

Planned RIDI execution environment:
- Python: `3.13.5`
- implementation: CPython
- OS family: Linux x86_64
- external Python dependencies: **none** (stdlib only)

The exact runtime version/environment is to be repeated in the raw execution bundle.

## Stop condition

RIDI substantive execution is **not permitted yet**.

Before running the frozen RIDI runner, CFC must separately complete its private M1/A1/I1 instantiation and provide only:
1. exact CFC mapped-input artifact hash(es);
2. authority/mapping manifest hash(es);
3. controller/config/version hash(es);
4. validation status that frozen M1/A1/I1 were applied without post-selection changes;
5. explicit statement that no substantive CFC execution has occurred.

CFC must not disclose the prohibited artifact contents to RIDI at this stage.

Once both pre-execution freezes are recorded, both sides may execute independently.

**Evidence before execution.**

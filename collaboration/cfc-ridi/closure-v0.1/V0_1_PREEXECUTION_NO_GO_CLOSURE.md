# CFC ↔ RIDI shared-case protocol v0.1 — RIDI acceptance of pre-execution NO-GO

**Closure date:** 2026-09-30  
**Selected case:** `RAG-nq-test1035`  
**Status:** V0.1 CLOSED AT PRE-EXECUTION GATE / CFC MAPPING_NOT_EVALUABLE / NO SUBSTANTIVE CFC OR RIDI EXECUTION

## Verified source recovery

RIDI recovered and publicly committed the exact pre-existing registered source artifact:

- `contexts_800.jsonl`
- bytes: `25266491`
- SHA-256: `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`
- recovery commit: `a198f07969b47cd25b812ba1a79f516f5e1c679a`
- Git blob: `e7c031dc4697b08052a35d8b676bb8203c145714`

The CFC side independently reverified the complete recovered bytes.

## CFC-side formal pre-execution decision

CFC commit:

`f52053ba28b1001fd594d8f091ca8c68b3f93674`

records:

- source availability: **PASS**;
- exact source SHA-256/byte count: **MATCH**;
- faithful executable instantiation under frozen v0.1 M1/A1/I1: **MAPPING_NOT_EVALUABLE / PRE-EXECUTION NO-GO**;
- valid completed mapped-input / mapping-manifest / authority-manifest / substantive runner/config freeze identities: **NOT AVAILABLE**;
- substantive CFC execution: **NOT PERFORMED**;
- RIDI raw result/output: **NOT INSPECTED**.

The CFC record explicitly distinguishes this from a substantive CFC verdict or `CFC_PAIR_NOT_EVALUABLE` result from an executed controller run.

## RIDI-side acceptance

RIDI accepts the CFC pre-execution NO-GO as protocol-conformant.

Accordingly:

1. RIDI will not execute the already frozen RIDI runner for this case.
2. No raw RIDI output bundle will be produced.
3. No substantive CFC/RIDI comparison result exists for v0.1.
4. The selected case remains fixed historically; it is not silently replaced.
5. No M1/A1/I1 patch, authority retrofit, threshold change, synthetic substitution or alternate CFC runner may be introduced under v0.1.
6. Any renewed experiment requires an explicit versioned reset and renewed bilateral freeze before a new substantive selection.

## What v0.1 did establish

The v0.1 record nevertheless establishes several reproducible methodological facts:

- bilateral protocol and annexes were frozen before case selection;
- the 800-case eligible pool was independently reproduced and mirrored exact-byte;
- joint seed commit–reveal deterministically selected `RAG-nq-test1035`;
- all 800 selection scores independently reproduced byte-for-byte;
- the exact neutral selected specimen and endpoint records were independently extracted and verified;
- the requested original `contexts_800.jsonl` source was recovered and independently verified;
- the frozen pre-execution authority/implementation gate detected that the available substantive CFC path could not be faithfully instantiated without introducing prohibited synthetic/post-selection authority.

This is a bounded **pre-execution protocol finding**, not evidence of CFC or RIDI substantive performance.

## Publication boundary

Any manuscript or report using this record must state that:
- no substantive controller comparison was executed in v0.1;
- no CFC ALLOW/BLOCK result exists;
- no RIDI PASS/FAIL result from the selected case was executed;
- the NO-GO concerns the frozen experiment-specific implementation/authority mapping, not CFC in general;
- the result demonstrates the value of a pre-execution authority gate by preventing an invalid experiment from being run.

**Evidence before execution — and stop when execution is not justified.**

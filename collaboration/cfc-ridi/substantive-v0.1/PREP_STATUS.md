# CFC ↔ RIDI substantive preparation status

**Status:** READY FOR BILATERAL ELIGIBILITY-CRITERIA REVIEW  
**Date:** 2026-09-28  
**Branch:** `prep/cfc-ridi-substantive-infra-v0.1`

## Completed preparatory work

- Drafted outcome-independent eligible-pool inclusion/exclusion criteria.
- Created an empty `eligible_pool_TEMPLATE.tsv`; candidate rows remain zero.
- Implemented strict pool validation:
  - exact UTF-8/LF requirements;
  - exact column order;
  - printable ASCII canonical IDs;
  - lowercase SHA-256 identities;
  - mandatory recorded/offline endpoint;
  - exclusion of authoritative support requirements >1;
  - prior-public-exposure field;
  - lexical sorting and duplicate rejection.
- Implemented the frozen protocol's commit–reveal formulas exactly:
  - participant seed commitment;
  - combined selection hash;
  - per-case score;
  - lowest-score selection with lexicographic tie break.
- Tooling does not generate selection seeds.
- Added deterministic raw-bundle construction with fixed ZIP member timestamps and stored bytes.
- Added raw-bundle SHA/size/manifest verification.
- Drafted a result-neutral joint-paper skeleton.
- Added CI checks using Python standard library only.

## Automated verification

Latest CI run:

https://github.com/adeebnoor/ridi/actions/runs/36354135346

Result: **PASS**

The CI confirms:
- candidate rows = 0;
- substantive case selected = false;
- selection seed created = false;
- pool validation tests pass;
- selection reproducibility tests pass;
- deterministic raw-bundle byte test passes.

## Not performed

- No eligible pool has been frozen.
- No real candidate ID has been added.
- No selection seed has been created or revealed.
- No substantive case has been selected.
- No substantive CFC or RIDI run has been executed.
- No result has been written into the paper skeleton.

## Next protocol-safe step

After the Krzysztof-side annex mirror and the chronology-clean repeat of the excluded mechanical dry run, jointly review/freeze the eligibility criteria, construct the eligible pool under those frozen criteria, hash/freeze that exact pool, and only then enter seed commit–reveal.

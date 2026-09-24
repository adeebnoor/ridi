# RIDI Nature P4 — post-registration, pre-outcome clarification

**Date:** 24 September 2026  
**Status:** locked before any P4 machine-judge output.

## Why this clarification exists

OSF registration `ms4w8` prespecified that P4 would use **two LLM judges from different model families** and fixed the P4 endpoint, query panel, exchange construction, human-audit sample size/seeds, and decision rule. The filed text did not record the exact model IDs for the two machine judges. No P4 machine-judge output has been generated or inspected as of this lock.

This document fills only that omitted implementation detail. It does **not** change the P4 hypothesis, endpoint, clean-subset definition, query panel, passages, bootstrap procedure, threshold, human sample, or seeds. P4 will be reported as using a dated post-registration pre-outcome model-ID clarification, not as if the model IDs had appeared in the original registration.

## Locked machine judges

1. **Judge 1:** `mistralai/Mistral-7B-Instruct-v0.3`  
   Revision: `c170c708c41dac9275d15a8fff4eca08d52bab71`

2. **Judge 2:** `allenai/OLMo-2-1124-7B-Instruct`  
   Revision: `470b1fba1ae01581f270116362ee4aa1b97f4c84`

These are different model families and both exact revisions were already frozen as registered model-family transfer assets in the recovered original experiment manifest before P4 execution.

## Locked P4 judge prompt

```
You are auditing evidence for a {kind}.
{label}: {question}

Passage:
{passage}

Does this passage contain any information that would help {goal}, including partial, indirect or misleading evidence that a reader could use? Reply with exactly one word: YES or NO.
```

Prompt SHA-256: `e7d4f75fad480666101c1dbd1b185f1990b1aa9107644185e7e8ece6e05fdd47`

## Locked analysis

Unchanged from OSF `ms4w8`:

- clean query: every exchanged passage is judged uninformative by **both** machine judges and contains no normalized QA gold string;
- primary rate: equal-dataset-weight correctness-change macro on the recovered 800-query panel;
- support criterion: point estimate >= 0.05 and lower 95% stratified-bootstrap bound > 0.02;
- P4 is a judged-uninformative subset, not proof of semantic irrelevance;
- human audit: 200 unique query-passage items, sample seed `20260926`, annotation-order seeds `20260927` and `20260928`.

## Human annotation gate

No human annotation files will be shown to annotators and no human labels will be collected until King Abdulaziz University has issued the applicable institutional determination and all resulting review/consent requirements have been satisfied.

## Outcome handling

All P4 machine-judge failures/unparsed outputs will be reported. Thresholds and judge identities will not be changed after outcome inspection.

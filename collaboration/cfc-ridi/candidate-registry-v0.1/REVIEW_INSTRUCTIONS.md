# CFC ↔ RIDI Candidate Registry v0.1 — Independent Review Instructions

**Status:** REVIEW ONLY — NO POOL FREEZE / NO SEED / NO CASE SELECTION

## 1. Obtain the exact transport bundle

Temporary review transport:

https://firestorage.ai/en/f/zdtjoL6fvp6w

Expected file:

`CFC_RIDI_CANDIDATE_REGISTRY_INPUT_v0.1.zip`

Expected ZIP identity:

- bytes: `435772`
- SHA-256: `2b96ee5319cb93bce9b752fb4c6c3353c0e0463d8cd11e79f0dd682423093b00`

Example:

```bash
sha256sum CFC_RIDI_CANDIDATE_REGISTRY_INPUT_v0.1.zip
```

Do not review contents if the ZIP hash does not match exactly.

## 2. Verify the included run artifacts

Expected uncompressed artifact hashes:

```text
09824e8fa0837cc852b34c984b3ad7156a7433a57d672f4124356f4806e2fccf  candidate_registry.tsv
23e027e7228c3a09d13b238619ca87389f304f3fb281c37b386cca6a6defe826  eligibility_audit.tsv
ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade  eligible_pool_draft.tsv
c5c49b7c93c32bcfee23d20f6cb7456d9f6d14b9ab8d2846b6a320f91f4ac0ff  SOURCE_PROVENANCE.md
8718c56a1a1afce095b74df409d67f0a346c0d0d6dbf1e8560f2ffaa69c67f2a  checker_run.txt
96ca16e12e3f2fecb5a06998eb28476e250b2a0965f2b26713da298391958904  eligibility_check_frozen.py
```

## 3. Confirm registry shape

Expected:

- 800 data rows + 1 header in `candidate_registry.tsv`
- 800 data rows + 1 header in `eligibility_audit.tsv`
- 800 data rows + 1 header in `eligible_pool_draft.tsv`

Dataset frame:

- NQ: 250
- HotpotQA: 250
- FEVER: 150
- SciFact: 150

## 4. Re-run the frozen checker

The included checker must itself hash to:

`96ca16e12e3f2fecb5a06998eb28476e250b2a0965f2b26713da298391958904`

Run:

```bash
python eligibility_check_frozen.py candidate_registry.tsv \
  --audit-out eligibility_audit_repeat.tsv \
  --pool-out eligible_pool_repeat.tsv
```

Expected stdout:

```text
checker_sha256=96ca16e12e3f2fecb5a06998eb28476e250b2a0965f2b26713da298391958904
candidate_registry_sha256=09824e8fa0837cc852b34c984b3ad7156a7433a57d672f4124356f4806e2fccf
registration_count=800
accepted_count=800
rejected_count=0
eligibility_audit_sha256=23e027e7228c3a09d13b238619ca87389f304f3fb281c37b386cca6a6defe826
eligible_pool_sha256=ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade
```

The repeated audit and pool files must match the stated SHA-256 identities exactly.

## 5. Review boundaries

The reviewer may inspect:
- registry construction fields;
- source and endpoint hashes;
- evaluation-definition binding;
- support-requirement status;
- eligibility flags and reasons;
- checker behavior.

For this pre-pool-freeze review, do **not** use:
- computed CFC outcomes;
- computed RIDI PASS/FAIL;
- correctness;
- desired asymmetric cell;
- scientific attractiveness of particular cases

to accept/reject candidates or alter the registry.

## 6. Next step only after bilateral verification

If the exact registry, audit and pool-draft bytes independently reproduce:

1. approve the exact eligible-pool draft SHA-256;
2. create a separate eligible-pool freeze record;
3. mirror that exact frozen pool on both sides;
4. only then proceed to seed commit–reveal.

No seed should be created before the exact pool freeze.

# CFC ↔ RIDI pre-execution bilateral freeze — CFC private status request

**Selected case:** `RAG-nq-test1035`  
**RIDI status:** NEUTRAL HANDOFF VERIFIED / RIDI INPUT + RUNNER FROZEN / NO SUBSTANTIVE EXECUTION

RIDI has independently verified the public neutral handoff and frozen its permitted input and runner.

## RIDI frozen identities

- RIDI input SHA-256:
  `0f92f41721a452c7045c4c384d4345ba7335fc5ee724150c880ca2174edf75e0`
- RIDI input Git blob:
  `7381164f715aa90d7d6e0a2083bc0cd13e85e15f`
- RIDI runner SHA-256:
  `a532c605f664d275e8da8e7ae041f5eec45490a37e128d87158bac004c992866`
- RIDI runner Git blob:
  `2102d80569eb9917df1903b80ca9853bd4d81c18`
- neutral ZIP SHA-256:
  `f6845736496c51d5407ddfe46481a07a8d7ee43eb4735e3c23aee934607b3b56`

No RIDI substantive run has been executed.

## Required CFC response before execution

Under frozen I1, CFC should **not** disclose the private artifact contents. CFC should publish only:

1. mapped arm-A input SHA-256 and byte size;
2. mapped arm-B input SHA-256 and byte size;
3. mapping-manifest SHA-256 and byte size;
4. authority-manifest SHA-256 and byte size;
5. exact frozen CFC controller/runner/config version or commit/hash identities;
6. M1 SHA-256 used:
   `7adc4229277280acf9f48528a74ace7df9ba28ac1295e30ced318a7c1a3ee858`;
7. A1 SHA-256 used:
   `86f8b73bbb7e6f59aea95f2f388d15b78c3cda2d9ffc5190336b3e5a4ca64be9`;
8. I1 SHA-256 used:
   `2f3a86e6e9e4b32633813bc2bd82dd2e04f55d7a643ca32780a78b997c01ae4b`;
9. mechanical-instantiation validation status;
10. explicit confirmation that:
   - no post-selection mapper/authority/threshold change occurred;
   - no substantive CFC execution has occurred;
   - no RIDI raw result/output was inspected.

## Bilateral execution gate

Substantive execution begins only after RIDI verifies the CFC public freeze-status record and confirms that both sides' input/config freezes are complete.

After that confirmation:
- CFC executes independently using its private frozen input;
- RIDI executes independently using its frozen public input;
- neither side sends raw outputs;
- each side first assembles one immutable raw bundle and publishes only `SHA256(bundle exact bytes)` + byte size;
- exact bundle exchange occurs only after both raw-bundle commitments exist.

**Evidence before execution.**

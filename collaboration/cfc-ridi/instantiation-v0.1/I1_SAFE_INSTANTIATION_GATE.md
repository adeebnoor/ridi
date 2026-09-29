# CFC ↔ RIDI mechanical instantiation gate v0.1

**Selected case:** `RAG-nq-test1035`  
**Frozen M1:** `7adc4229277280acf9f48528a74ace7df9ba28ac1295e30ced318a7c1a3ee858`  
**Frozen A1:** `86f8b73bbb7e6f59aea95f2f388d15b78c3cda2d9ffc5190336b3e5a4ca64be9`  
**Frozen I1:** `2f3a86e6e9e4b32633813bc2bd82dd2e04f55d7a643ca32780a78b997c01ae4b`

## Allowed shared pre-execution material

Both sides may inspect and freeze:
- selected case ID;
- exact neutral A/B source specimen bytes;
- exact neutral A/B offline endpoint bytes;
- immutable references and SHA-256 identities;
- recorded offline verdict/action values because I1 explicitly permits them to both sides;
- the frozen protocol and M1/A1/I1 identities.

## RIDI-side pre-commit material

Adeeb/RIDI may additionally inspect the RIDI-permitted surface, including:
- retrieval rank positions;
- relevance-grade vector;
- retrieval metrics;
- selected identities;
- recorded offline verdict/action A/B.

RIDI must not inspect CFC mapped input, CFC authority records, CFC gates/reasons, CFC outputs or CFC interpretation before both raw-bundle hashes are committed.

## CFC-side pre-commit material

Krzysztof/CFC may mechanically instantiate M1/A1/I1 using the selected neutral specimen and already-existing authority records permitted by A1/I1.

The CFC side must **not send the mapped CFC input or authority manifest to RIDI before raw-bundle commitment**.

The CFC side may publish or communicate only their cryptographic identities/validation status needed to establish the pre-execution freeze, without disclosing prohibited contents to RIDI.

## No-go conditions

Stop before substantive execution if:
- any selected exact-line hash mismatches;
- the selected record is absent or duplicated;
- a required source field cannot be faithfully represented under frozen M1;
- A1 requires an authority fact that did not already exist inside the permitted evidence boundary;
- a protocol ambiguity would require discretionary mapping after selection;
- either side would need to inspect a field prohibited by I1.

A no-go result requires a recorded versioned reset. No re-selection or quiet repair is permitted.

## Required freeze before execution

Before either substantive run:
1. freeze exact neutral A/B source line bytes and hashes;
2. freeze exact neutral A/B endpoint line bytes and hashes;
3. RIDI freezes its exact input/manifest identity;
4. CFC freezes its exact mapped per-arm input/manifest identity privately on the CFC side;
5. record validation status and implementation/version identities.

Only after those items exist may the two systems execute independently.

**Evidence before execution.**

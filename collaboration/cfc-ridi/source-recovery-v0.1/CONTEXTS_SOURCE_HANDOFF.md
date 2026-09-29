# CFC ↔ RIDI exact source-context handoff v0.1

**Date:** 2026-09-30  
**Selected case:** `RAG-nq-test1035`  
**Status:** EXACT PRE-EXISTING `contexts_800.jsonl` RECOVERED AND PUBLICLY COMMITTED / CFC INDEPENDENT VERIFICATION PENDING / EXECUTION GATE CLOSED

## Requested frozen source identity

The CFC-side HOLD requested the exact pre-existing registered source artifact:

- filename: `contexts_800.jsonl`
- expected bytes: `25266491`
- expected SHA-256:
  `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`

No reconstruction or post-selection annotation was authorized.

## Historical GitHub verification

RIDI commit:

`8ff699b63d21096e0d585befdefcdb7a94b93329`

introduced an execution-time recovery check for this exact artifact.

GitHub Actions run/job:

- run: `35935298332`
- job: `107430864294`

logged on 2026-09-23:

```text
execution_asset_sha256= d0fd425973965c33e6a4e9bc53e4ec65382dbc6ca946aac48f70496a571a01ea
contexts_sha256= 1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1 bytes= 25266491
1600 contexts, 800 queries, datasets {'nq': 250, 'hotpotqa': 250, 'fever': 150, 'scifact': 150}
OK
```

That establishes that the exact source bytes pre-existed the current CFC ↔ RIDI selected-case execution.

## Exact recovery from active pre-existing execution archive

A later active RIDI execution archive was used only as a transport source:

- public share: `https://firestorage.ai/en/f/OjZ4x0tKnOrV`
- file: `RIDI_Nature_POSTREG_EXECUTION_READY_20260924.zip`
- file ID: `01a0d33b991472e4ba11a81ae1646a5c`
- archive bytes: `77073111`
- archive SHA-256:
  `509af2d85d0c305bb729b055a78e5c43670b871969d70b5cd66c64ae63cc4081`
- archive member:
  `RIDI_Nature_POSTREG_EXECUTION_READY_20260924/p2_p3/data/contexts_800.jsonl`

Recovery workflow:

- workflow run: `36631590266`
- job: `109621892044`
- result: `SUCCESS`

The workflow refused to commit unless the extracted member matched both the frozen byte count and frozen SHA-256.

## Permanent GitHub publication

Recovery commit:

`a198f07969b47cd25b812ba1a79f516f5e1c679a`

GitHub path:

`collaboration/cfc-ridi/source-recovery-v0.1/contexts_800.jsonl`

Git blob:

`e7c031dc4697b08052a35d8b676bb8203c145714`

Git tree size:

`25266491` bytes

Recovery manifest:

`collaboration/cfc-ridi/source-recovery-v0.1/CONTEXTS_RECOVERY_MANIFEST.txt`

Manifest records:

```text
contexts_bytes=25266491
contexts_sha256=1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1
verification=PASS
```

## Access

Commit-pinned GitHub file:

`https://github.com/adeebnoor/ridi/blob/a198f07969b47cd25b812ba1a79f516f5e1c679a/collaboration/cfc-ridi/source-recovery-v0.1/contexts_800.jsonl`

Commit-pinned raw bytes:

`https://raw.githubusercontent.com/adeebnoor/ridi/a198f07969b47cd25b812ba1a79f516f5e1c679a/collaboration/cfc-ridi/source-recovery-v0.1/contexts_800.jsonl`

Independent CFC verification command:

```bash
curl -L \
  https://raw.githubusercontent.com/adeebnoor/ridi/a198f07969b47cd25b812ba1a79f516f5e1c679a/collaboration/cfc-ridi/source-recovery-v0.1/contexts_800.jsonl \
  -o contexts_800.jsonl

wc -c contexts_800.jsonl
sha256sum contexts_800.jsonl
```

Expected:

```text
25266491 contexts_800.jsonl
1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1  contexts_800.jsonl
```

## Boundary

This recovery resolves only the source-availability gap for the exact pre-existing `contexts_800.jsonl` requested in the CFC HOLD.

It does **not**:
- create a new authority assertion;
- reconstruct missing content;
- alter M1/A1/I1;
- alter the selected case;
- expose CFC-private mapped inputs or manifests;
- start substantive CFC or RIDI execution;
- remove any separate provenance limitation concerning other upstream artifacts.

CFC should independently retrieve and verify the public bytes before deciding whether its private M1/A1/I1 instantiation can proceed or whether another frozen no-go condition remains.

**Evidence before execution.**

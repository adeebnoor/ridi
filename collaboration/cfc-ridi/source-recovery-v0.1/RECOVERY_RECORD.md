# CFC ↔ RIDI source recovery v0.1 — exact registered contexts

**Purpose:** recover the exact pre-existing `contexts_800.jsonl` artifact requested by the CFC-side M1/A1 pre-execution check.

## Frozen expected identity

- filename: `contexts_800.jsonl`
- bytes: `25266491`
- SHA-256: `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`

## Historical GitHub provenance

GitHub commit `8ff699b63d21096e0d585befdefcdb7a94b93329` added a recovery step that downloaded a pre-existing execution asset and asserted the exact contexts SHA-256 before copying it into the frozen execution tree.

GitHub Actions run `35935298332`, job `107430864294`, subsequently logged:

```text
execution_asset_sha256= d0fd425973965c33e6a4e9bc53e4ec65382dbc6ca946aac48f70496a571a01ea
contexts_sha256= 1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1 bytes= 25266491
1600 contexts, 800 queries, datasets {'nq': 250, 'hotpotqa': 250, 'fever': 150, 'scifact': 150}
OK
```

The original temporary Firestorage transport used by that run later expired.

## Active recovery source

An active later RIDI execution share contains:

`RIDI_Nature_POSTREG_EXECUTION_READY_20260924.zip`

Public share:
`https://firestorage.ai/en/f/OjZ4x0tKnOrV`

Public file ID:
`01a0d33b991472e4ba11a81ae1646a5c`

The recovery workflow on this branch downloads that archive, searches for exactly one `contexts_800.jsonl`, and refuses to proceed unless both exact byte size and SHA-256 match the frozen identity above.

If verification succeeds, the workflow commits only:
- `collaboration/cfc-ridi/source-recovery-v0.1/contexts_800.jsonl`
- `collaboration/cfc-ridi/source-recovery-v0.1/CONTEXTS_RECOVERY_MANIFEST.txt`

No reconstruction, reserialization, annotation, or authority assertion is performed.

**Execution gate remains closed until the recovered GitHub file independently verifies.**

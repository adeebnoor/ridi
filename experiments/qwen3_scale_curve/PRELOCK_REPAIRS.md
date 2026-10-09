# Pre-lock implementation repairs — 2026-10-09

Study: RIDI-RAG-QWEN3-SCALE-CURVE-v1.

These changes were made before creating LOCK.json, before registration, and before any model generation for this study. No scientific outcomes were generated or inspected. Hypotheses, effect definitions, thresholds, seeds, panel, prompts, model sizes and generation conditions remain those in the supplied preregistration.

## Repairs

1. Attempts are immutable, sequential and limited to three. A retry requires a recorded technical failure with identical configuration; success cannot be rerun. Partial answers are fsynced as they are generated, and completion uses atomic status/metadata files. A hard machine loss must be documented by the external supervisor before retry; a stale running marker is never silently treated as failure.
2. Enforce the specified BF16 dtype and 80GB-class GPU count. Check the exact required lock files and study identity using explicit exceptions rather than removable assertions.
3. Analysis checks terminal status of all 24 primary jobs before reading outcome records. It verifies successful attempt identity, model/revision, configuration, lock and records hash. Failed attempts are excluded and partially completed models are reported as not executed.
4. Compare the exact equal-benchmark point estimate on its integer lattice so exactly 5 percentage points satisfies the inclusive H1 threshold. Preserve strict confidence-bound thresholds. Compare the S4 permutation statistic using equivalent integer count sum-of-squares, preserving ties and the planned variance statistic.
5. Require the frozen P4 feature file, verify its SHA-256 and exact 800-question coverage, and verify the prespecified strata sizes 93, 238, 86 and 282. Add the promised pooled estimates and fixed16 accuracy outputs.
6. Add a no-generation --preflight-only check for actual archive compatibility, and integrity tests using synthetic data only.

## Frozen inputs and registration materials

- The six September 2 source archives match the pre-existing SHA-256 constants. All four preflight runs reproduce the registered panel order, document identities and prompt-manifest hashes. See validation/source_preflight.json.
- code/per_question_features.jsonl is copied byte-for-byte from Nature_RIDI_v14.3_20261009.zip / Supplementary_Data_3.zip / analysis/per_question_features.jsonl.
- Feature SHA-256: dc9d3f48a8bab7874e3925cf8b87d74732d56d6d91c79381989c9fd6c208e4cc.
- The supplied Word and Markdown preregistration texts are unchanged. LOCK.json also records the Markdown and P4 feature hashes.
- resolve_revisions.py was executed successfully before make_lock.py; the four new dense model revisions and optional model revision are fixed. Existing 8B/32B revisions are preserved.

## Runtime validation boundary

Preflight and synthetic tests do not establish GPU execution success. In particular, the fixed batch of 16 on 32B must fit the chosen hardware without reducing the registered batch size or quantizing weights. No GPU job may start before the public commit and immutable OSF registration are complete.

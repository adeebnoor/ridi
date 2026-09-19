# RIDI-RAG-QWEN3-32B-SCALE-v1 — public pre-output lock

**Status:** post hoc scale-transfer extension, publicly locked before any successful Qwen3-32B generation.

This is **not** an OSF preregistration and does not change the registration status of the original RIDI RAG experiment at OSF txwdv. It reuses the original registered 800-query primary panel and intervention exactly, changing only model scale within the Qwen3 family.

## Prior failed attempts

Two earlier Qwen3-32B jobs (`6aac8dcd5c02253cfb1457f9`, `6aac8eaab1dc2b62dc58fe81`) failed while acquiring an expired temporary prompt/input archive, before the model was loaded and before any Qwen3-32B endpoint output was produced. They remain in the audit trail.

## Frozen source reconstruction

The execution root is reconstructed from the original 2 September 2026 files:

- `RIDI_RAG_NATURE_CONTROL_POSTREG_20260902.zip`
  - SHA-256 `4b5bc603fcbd5165766beabc05d17ec7e0cefa6e0d8c9c47fd65b06eca61c864`
- `prepared-v4-nq.zip`
  - SHA-256 `5b1e813b5e486f9c588c0a73a3d04a1402f4959d991a1c1631fa007f8559bc13`
- `prepared-v4-hotpotqa.zip`
  - SHA-256 `783f1f41db0f22e9ca59ce8ddb9520d06105dd7a817746d8032295cd57025bfb`
- `prepared-v4-fever.zip`
  - SHA-256 `b2cc0868918569047ba7b44f193e26a759a4e268d964cf8f20141c7d15eecd63`
- `prepared-v4-scifact.zip`
  - SHA-256 `fcc9483c65b06df889c34267a358c79bc7720d507f2d03c0419a8d1d772be5dc`
- archived primary Qwen3-8B result package `RIDI_RAG_RESULTS__PRIMARY_H1_H2.zip`
  - SHA-256 `c19942d0eb4a0087195c46a45831a1cf864676b813485dcf4e5565a2a676f231`

The nested registered bundle must equal SHA-256
`1a3c4909fa9c351826a7b9a861173b8d64df534ae095c96dd15d2d6281eed31b`,
and the frozen manifest must equal
`0dd99d3737b9fe4d92ce2228d4227e42d3b15b52b9f204be11dc5b53d03d2885`.

Before this lock, all 73 files named by the frozen manifest were reconstructed from the original archives and matched their registered SHA-256 values exactly (73/73, zero missing, zero mismatches).

## Prompt lock

Prompts are reconstructed with the original registered `code/prompts.py`, original query text, original corpus bytes, passage truncation of 1,200 Unicode characters, and the exact reference/random document identities archived in the v54 primary result rows.

Registered prompt-template SHA-256:
- QA: `33ba5e64e87c14ae6646764099f40ffde5229842eaa4765e7fb0f410eb456745`
- classification: `9c95b42a6dd6e164d1702589eb80560ce4175aadfcc2084dbda4732bff51f4e2`

A deterministic 800-row prompt-hash manifest was created before Qwen3-32B generation:
- all 800 rows: `e70de01f40f57fe5db14f1b100839b40763edbc55267e2054a4092bc33a1920c`
- NQ 250: `78f32c89197c3f46fa405000a0d99664c975e9b52d0136c239407ac7a4b75330`
- HotpotQA 250: `dcc66ff3c27bb3f0693e34cff68fd45771b081356ccaa031714e3f1f31866b49`
- FEVER 150: `54231e17d0f367d617df6615ea8869c79952ba1057923c7b238776354ad9b4df`
- SciFact 150: `76842af60eabbeacec99bef62b619bb643b6f00d08bf8d03503ea940b0c7a7fa`

The execution must reproduce the corresponding dataset prompt-manifest hash before model loading.

## Single scientific change

Original primary model:
- `Qwen/Qwen3-8B`
- revision `b968826d9c46dd6066d109eabc6255188de91218`

Scale-transfer model:
- `Qwen/Qwen3-32B`
- revision `9216db5781bf21249d130ec9da846c4624c16137`

Everything else is retained:
- 800 queries: NQ 250, HotpotQA 250, FEVER 150, SciFact 150
- BM25
- k=10
- reference versus primary random identity substitution
- same exact selected document identities
- same prompt template and passage bytes
- max_new_tokens=128
- thinking disabled
- greedy decoding (do_sample=False)
- seed 20260902
- deterministic PyTorch algorithms
- TF32 disabled
- same frozen scoring module and gold labels

No quantization is permitted. The runtime must report the loaded parameter dtype and GPU.

## Primary scale-transfer endpoint

For Qwen3-32B, compute the equal-dataset-weight macro factual-correctness divergence rate between reference and random identity-substitution contexts.

The original H2 design boundaries are reused **before** 32B output:
- macro >= 5%: supports transfer of the registered behavioral consequence to 32B;
- macro < 2%: falsifies the strong scale-transfer consequence;
- 2% <= macro < 5%: inconclusive for the predeclared scale-transfer criterion.

These criteria do not re-register or alter the original H2.

## Required reporting

Report regardless of direction:
- each dataset's flip count/rate;
- equal-dataset-weight macro and 100,000-draw stratified bootstrap 95% interval;
- correct-to-incorrect and incorrect-to-correct counts;
- normalized/canonical output change where available from the frozen scorer;
- paired query-level 32B-minus-8B flip-vector difference with a 100,000-draw dataset-stratified bootstrap interval (seed 20260919);
- exact environment, model revision, source hashes, prompt-manifest hashes and raw-output hashes.

No query may be removed because its 32B result is inconvenient.

## Interpretation boundary

This experiment tests scale transfer within one open-weight model family at one larger scale. It cannot establish behavior for proprietary models, all large models, all prompts, or all retrieval settings.

# RIDI-PREDICT-v1 execution status

The preregistration is public and accepted at https://osf.io/xrzp5/ (registered 2026-10-10T18:56:09.996751Z). The registered ZIP was downloaded and all 63 members compared byte-for-byte with the preparation directory before creating LOCK.json. The package SHA-256 is 1b9c7de56870749f3434970b1dae6ab8cd8883138198efc980a75f83f374e9cb.

The README_AR.md and PREPARATION_STATE.json retain their historical pre-registration state. This execution note records the subsequent verified registration and lock creation. No model responses have been generated and no confirmatory analysis has been performed for this study. OSF lock attachment and its verification remain required before generation.

## Form display clarification

OSF's form renderer removed the angle-bracket dataset placeholder in the Randomization identifier. The registered ZIP, Markdown protocol, and runner retain the intended identifier: the dataset name followed by :bm25 (nq:bm25, hotpotqa:bm25, fever:bm25). This is a display clarification only; the registered scientific files, seeds, panel and settings are unchanged.

The attached scientific files remain byte-identical to the registration. The private PI coding key is not included.

## Input packaging

The known-source filter is published as known_source_filter.json.gz to fit the publishing service payload limit. Before running the unchanged runner, decompress it with `gzip -dk known_source_filter.json.gz`. The uncompressed SHA-256 must match LOCK.json (bc2aecee5a27fc33b75e5caf5c000764ee1c88598533075ace19884a8c613df8). Its original uncompressed bytes are also in the verified registered OSF ZIP. Compression is transport packaging only; no scientific file is changed.

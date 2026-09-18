# Technical clarification after failed preparation run

Protocol: `RIDI-NATURE-FRONTIER-DOWNSTREAM-v1`

This note is timestamped **before any successful retrieval output or language-model endpoint output** from the extension.

## Failed run

The first preparation attempt, GitHub Actions run `35347356145` from commit `1455a7e53671995beffdc110a6ab45b640fb7060`, failed in every retrieval job before a TREC run was produced. The failure was technical: Anserini's Java topic downloader could not retrieve the BEIR topic file from `raw.githubusercontent.com`. No retrieval scores, frontier results or model answers from the extension were inspected.

## Locked implementation clarification

The original protocol defined the candidate universe as the union of the two frozen retriever candidate lists but did not state how to obtain a score from one retriever for a candidate surfaced only by the other retriever.

Before successful retrieval, the implementation is clarified as follows:

1. Each retriever (BM25 and SPLADE++) is executed to depth **1,000** for every query.
2. The frontier candidate universe is the union of **BM25 top-100** and **SPLADE++ top-100** document identities.
3. A query is eligible only if **every identity in that top-100 union has an emitted score in both top-1,000 runs**. No missing score is imputed.
4. Baseline and updated score vectors used by the exact frontier are therefore genuine emitted BM25 and SPLADE++ scores on the same fixed candidate universe.
5. The primary and sensitivity selection capacities remain `k={10; 5,20}`; tolerances remain `eta={0.001; 0.0001}`.
6. For each dataset independently, 100 query IDs are sampled without replacement from the sorted eligible IDs using NumPy `default_rng(20260918)`. Sampling occurs before any language-model generation.
7. Candidate passage text is truncated to the first 1,200 Unicode characters, matching the registered RAG prompt standardization.

This clarification changes neither the scientific question nor any endpoint. It prevents arbitrary score completion for cross-retriever candidates.

## Topic/qrel acquisition repair

To avoid the Java downloader failure, the new preparation workflow downloads the same Anserini BEIR topic and qrel files directly over HTTPS with retries, records their SHA-256 hashes, and passes the local topic file to Pyserini. This is an acquisition repair only.


## Second preparation failure

GitHub Actions run `35349531324` also failed before retrieval because the initially pinned dependency set was internally inconsistent: current Pyserini 2.1.0 requires Transformers >=5, while the first repaired requirements file pinned Transformers 4.57.6. No retrieval command executed and no extension endpoint output was produced. The dependency set was therefore repaired, still before retrieval, to the versions resolved successfully by the immediately preceding Pyserini installation environment: Pyserini 2.1.0, huggingface_hub 1.32.0, Transformers 5.17.0, Torch 2.14.0 and NumPy 2.5.3.


## Third preparation failure and upstream repository migration

GitHub Actions run `35349689574` reached the retrieval step after the dependency repair but failed before any TREC output was written because the manually specified topic URL used the historical `castorini/anserini-tools/topics-and-qrels` path, which now returns HTTP 404. Inspection of the upstream GitHub repository showed that `castorini/anserini-tools` has moved to `castorini/eval`, where topics and qrels are stored in separate `topics/` and `qrels/` directories. The exact four BEIR qrel paths were verified as UTF-8 files, and the four topic paths were verified to exist (GitHub rejected only because they are gzip binaries). No retrieval score, frontier result or language-model endpoint output was produced by the failed run.

The acquisition code is therefore repaired to use the same BEIR topic/qrel filenames from the current `castorini/eval` repository. This is an upstream-path migration only; query definitions, sample seed, retrievers, depths, k, eta and endpoints are unchanged.


## Assembly-only repair after successful retrieval

The third full preparation run (`35350211540`) successfully completed all eight locked retrieval jobs (BM25 and SPLADE++ for all four datasets), producing the top-1,000 TREC artifacts. Its assembly jobs then failed before sample selection because a repository-editing operation had inserted a literal `\\n` token into the Python source between `QREL_BASE` and `INDEX_FLAT`, causing a syntax error. No 100-query sample, frontier selection or language-model output was produced by that failure.

The syntax defect was repaired at commit `59c4e145ff2bdfd704a11e26bf6f1bf065979fc3`. To avoid rerunning or changing the already successful retrievals, the next step consumes the immutable retrieval artifacts from run `35350211540` and performs assembly only. The retrieval artifacts themselves are not recomputed.

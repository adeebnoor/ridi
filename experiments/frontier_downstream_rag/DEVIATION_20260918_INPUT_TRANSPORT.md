# Deviation note — retrieval input transport, 18 September 2026

Protocol: `RIDI-NATURE-FRONTIER-DOWNSTREAM-v1`

The first post-lock input-preparation run (GitHub Actions run `35347356145`) failed **before any retrieval endpoint or language-model output was produced**. Pyserini/Anserini attempted to download its registered BEIR topic files from `raw.githubusercontent.com/castorini/anserini-tools` inside the Java process and raised an I/O download exception across retrieval jobs.

This is a source-transport failure, not a scientific endpoint result.

To preserve the locked scientific design, the preparation code is changed only as follows:

- query texts and qrels are read from the official BEIR dataset archives hosted by the BEIR project;
- each query list is materialized locally as TSV before invoking the same Pyserini prebuilt indexes;
- datasets, retrievers (BM25/SPLADE++), prebuilt indexes, top-100 candidate rule, sample plan, k values, eta values, frontier definition, generator, scorers and endpoints are unchanged.

No retrieval ranking, frontier result, generation or downstream endpoint from this extension was inspected before this deviation was committed. The failed run remains in the public audit trail.

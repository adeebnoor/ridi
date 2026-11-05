# Review-only classification-parser sensitivity

Status: proposed post hoc analysis tooling. The tests use explicitly synthetic fixtures. Passing CI is not execution of the study and is not independent replication or CODECHECK certification. No patient records, unpublished answer archives, provider credentials, or manuscript files are committed here. The registered scoring code, existing results, and main branch are unchanged by this review branch.

## Why this tool exists

A response may start with an explicit label wrapper, such as `Verdict: SUPPORTS`. A strict first-token parser can treat that response as unparseable. This tool separates imported registered correctness, format-sensitive parsing, and changes between parseable labels. It does not establish the semantic truth of an answer or the accuracy of a benchmark label.

This analysis is **post hoc**. The need for it was identified after inspection of an external illustrative output and existing study summaries. The optional-wrapper parser is therefore not an outcome-naive preregistered endpoint. The registered endpoint must remain reported separately regardless of this analysis's result.

## Frozen rules

1. Include every query in the original FEVER and SciFact primary panels (150 each); no filtering to changed cases, valid-looking responses, or particular gold labels.
2. Use the archived reference, independently generated identity control, permutation control, and random-replacement response for each query. Do not regenerate answers for this analysis.
3. Import the **original saved canonical labels** as `registered_labels`. They are not reconstructed using a guessed implementation. Optional archived correctness is checked for consistency, never silently repaired.
4. Apply exactly one format-tolerant rule to raw text without consulting gold: labels at the start, optionally preceded by opening Markdown and `Verdict:`, `Answer:`, `Label:`, or `Classification:`. Accepted labels remain exactly SUPPORTS, REFUTES, and NOT_ENOUGH_INFO, case-insensitively. Do not search arbitrary explanation text, infer synonyms, or use an LLM judge.
5. Count missing/unparseable output as incorrect in the all-query endpoint. Report the both-parseable subset only as a separate conditional sensitivity with its denominator. Neither subset replaces the all-query endpoint.
6. Report both directions of correctness change, reference and alternative accuracy, unparseable counts, canonical-label changes, and persistence/resolution/new appearance of registered flips. A label change may leave both answers wrong.
7. Use paired resampling within each dataset, retaining the same query draw under both scorers. The two-dataset classification macro is **not** the four-dataset primary endpoint. No registered pass/fail decision is recalculated here.
8. Retain all results regardless of direction. No model generation, external calls, original-input editing, or output-directory overwriting is performed.

## Required normalized inputs

The frozen panel is a JSON object with exactly two keys and the original query identifiers as strings:

```json
{"fever": ["original-query-id-1", "..."], "scifact": ["original-query-id-1", "..."]}
```

The ellipses above are explanatory, not valid input. Each actual panel must contain exactly 150 unique original IDs. The following is a **synthetic schema example, not a study result**. Responses are one JSON object per line:

```json
{"dataset":"fever","query_id":"synthetic-example","gold":"SUPPORTS","answers":{"reference":"Verdict: SUPPORTS","identity":"Verdict: SUPPORTS","permutation":"SUPPORTS","random":"REFUTES"},"registered_labels":{"reference":"UNPARSEABLE","identity":"UNPARSEABLE","permutation":"SUPPORTS","random":"REFUTES"}}
```

Optional `registered_correctness` has the same four condition keys with integer 0/1 values. The original raw answer strings and original gold labels must be copied exactly from the archived study outputs and benchmark freeze. Record the source archive hashes and extraction procedure separately. Do not create normalized input by manually choosing convenient cases, modifying answer strings, or assigning new labels with this sensitivity parser.

An adapter from a particular archive layout is deliberately not guessed. Before study execution, verify its real schema, reconcile all 300 query IDs with the frozen panels, and compare the imported registered-label endpoint against the authoritative original output. An adapter/primary-endpoint mismatch is a stop condition, not a reason to alter the recorded result.

## Run

Python 3.10 or later; only the standard library is required for analysis.

```bash
python review_tools/rag_parser_sensitivity.py \
  --responses normalized_original_classification_responses.jsonl \
  --panel frozen_classification_panels.json \
  --out parser_sensitivity_review \
  --draws 10000 --seed 20260914
```

The command refuses incomplete, duplicated, extra-panel or inconsistent records and an existing output directory. It records input and code SHA-256 values. Output:

- `sensitivity_report.json`: per-dataset comparisons, control diagnostics, flip decomposition and paired bootstrap intervals.
- `per_query_diagnostics.csv`: source query identifiers and labels, with no raw response text. Access to this output still needs an appropriate research-data release review.

Test only:

```bash
pytest -q tests/test_rag_parser_sensitivity_review.py
```

A successful synthetic 300-query CLI test is **not** a run on 300 real queries. The tool's numerical test outputs must never be imported into the manuscript. The registered primary result, proprietary-model transport, longer-generation sensitivity, independent human scoring, and formal external verification are separate evidence items.

# Pre-output Mistral tokenizer dependency repair

**Timing:** documented after the first Mistral jobs failed and before any Mistral model generation or endpoint output.

The initial Mistral executions stopped while constructing the pinned tokenizer because the runtime had `sentencepiece` but not the `protobuf` Python package. The exception occurred before model loading and before any benchmark response was generated.

Repair: install a pinned `protobuf` package in the execution environment and rerun the unchanged public runner.

No model revision, dataset, frozen panel, prompt, batch rule, evaluator, endpoint, seed, decoding setting or statistical analysis changes.

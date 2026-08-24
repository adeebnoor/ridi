# Independent blind-run instructions

Protocol: `RIDI-CYBER-NATURAL-UPDATE-v1`  
Immutable protocol commit: `773219057b03fafb21dbc9c4623284a2da0ca83a`

This package is designed for a separately identified team. The manuscript author
must not operate the replication environment or disclose the author's result file
before the team returns its execution record.

## Run

Use Python 3.10 or later on a networked Linux, macOS or Windows system:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install numpy scipy
python experiments/cyber_natural_update/replication/run_sealed_replication.py
```

The runner verifies the locked files, downloads the source-commit-pinned public
inputs, executes the unchanged analysis and writes:

- `replication_output/locked_results.json`
- `replication_output/input_manifest.json`
- `replication_output/replication_execution.json`

Return these three files with a completed `TEAM_DECLARATION.md`. Do not edit the
protocol, code, cutoffs, outcome window, identity tolerance or external gate.

## Independence rule

A matching machine run is not by itself an independent replication. The team must
identify its organization and named executor, declare that the author did not run
the environment, and report any author assistance. Until those conditions are met,
the manuscript describes this package as a pending independent replication request.


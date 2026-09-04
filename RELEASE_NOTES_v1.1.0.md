# ridi-audit 1.1.0

Date prepared: 2026-09-04

## Researcher-first API

The main addition is a single high-level entry point:

```python
import pandas as pd
from ridi_audit import audit

before = pd.read_csv("examples/r0.csv")
after = pd.read_csv("examples/r1.csv")
report = audit(before, after, k=[3, 5])
print(report)
```

`AuditReport` supports:

- compact human-readable output;
- `to_dict()`;
- `to_markdown()`; and
- `control(k=..., eta=...)` for direct minimum-turnover selection inside an updated-score utility-regret budget.

## Scientific/documentation alignment

- Repository home aligned to the manuscript **Identical audits can yield different AI decisions**.
- Added a graphical abstract centered on `audit equivalence ≠ allocation equivalence ≠ decision equivalence`.
- Current public evidence page now foregrounds preregistered RAG, EPSS production turnover and the exact identity–utility frontier.
- Registered RxNorm and Open Targets failures remain visible as claim boundaries.
- External verification wording distinguishes exact EPSS numerical reproduction from targeted substantive SciFact regeneration.
- CODECHECK wording now states precisely that the request is registered, formal checking has not begun and no certificate is claimed.

## Compatibility

- Python 3.10–3.12 remain the CI-tested versions.
- Existing low-level functions and CLI commands remain available.
- This is a minor-version API addition; existing `1.0.0` programmatic interfaces are not intentionally removed.

## Distribution status

The repository is ready to build/package version 1.1.0. A public package-index release should only be described as available after the distribution has actually been uploaded and independently checked from a clean environment.

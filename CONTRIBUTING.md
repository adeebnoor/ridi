# Contributing to RIDI

RIDI is open to code contributions **and** scientific challenges. A useful contribution does not need to confirm the project’s claims.

## High-value contributions

### Independent replication
Run a locked workflow in a genuinely separate environment and report the raw result, including discrepancies. Use the **Independent replication** issue form.

### New domain application
Bring a real capacity-limited pipeline: RAG, clinical alerts, cybersecurity remediation, fraud/compliance triage, inspection, hiring, grants, moderation or another finite score-to-action system. Use the **New domain application** issue form.

### Boundary / counterexample
Show a setting where standard evaluation already identifies membership, where RIDI is redundant, or where allocation turnover has no meaningful consequence. These results are scientifically valuable.

### Method or software extension
Improve correctness, interoperability, performance, reporting, visualization, privacy-preserving identity audit, controls or the identity–utility frontier.

## Code workflow

1. Open an issue describing the proposed change and its scientific or engineering rationale.
2. Create a focused branch and add tests for behavioral changes.
3. Run:

```bash
python -m pip install -e ".[dev]"
pytest -q
```

4. Submit a focused pull request using the repository template.

## Research discipline

For an empirical contribution, document the decision object, capacity, selection rule, comparator, conventional metrics, identity result and the strongest available control. If downstream harm/benefit is claimed, define that endpoint independently rather than inferring it from turnover.

Preserve adverse outcomes, null results, parser/model deviations and protocol lineage. Do not tune confirmatory thresholds after inspecting the outcome and present the result as preregistered.

See the [Allocation Identity Reporting Checklist](docs/REPORTING_CHECKLIST.md).

## Data and privacy

Do not submit confidential, proprietary, patient-level or otherwise restricted data. Stable pseudonyms, hashes/commitments, aggregate identity-turnover statistics or private auditor mappings are acceptable when the application requires privacy.

## License

By contributing code, you agree that it may be distributed under the MIT License.

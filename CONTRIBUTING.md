# Contributing

Contributions that improve correctness, interoperability, documentation or domain validation are welcome.

1. Open an issue describing the proposed change and its scientific rationale.
2. Create a focused branch and add tests for behavioral changes.
3. Run `python -m pip install -e ".[dev]"` and `pytest -q`.
4. Submit a pull request using the repository template.

For new representation interventions, document what is frozen, the mechanism-matched control, the decision cutoff, the tie rule and any stochastic calibration. Preserve adverse outcomes and do not tune confirmatory thresholds after inspecting results.

By contributing code, you agree that it may be distributed under the MIT License. Do not submit confidential, proprietary, patient-level or otherwise restricted data.


# ridi-audit 1.1.1

Documentation and independent-verification synchronization patch. The public scientific API is unchanged from 1.1.0.

## What changed

- PyPI long description synchronized to the current researcher-first README.
- Completed second blind external SciFact 275 regeneration documented.
- Public verification wording now distinguishes exact audit preservation from generation-stack deviations.
- Public-index post-publish installation verification added to the release workflow.

## Independent SciFact 275 regeneration

A second independent executor returned the blind run with all frozen audit-equivalence checks preserved. Canonical outputs were:

- reference: `SUPPORTS`
- identity control: `SUPPORTS` (raw output byte-identical to reference)
- order-only permutation: `SUPPORTS`
- audit-equivalent identity substitution: `REFUTES`

The executor disclosed a hardware-driven serving deviation: the CPU-only host used the same frozen inputs and prompt conditioning but generated through a Q4_K_M `qwen3:8b` llama.cpp/Ollama path rather than the pinned bf16 Hugging Face runtime. The result is therefore described as a cross-serving/quantization robustness regeneration, not as a byte-identical backend reproduction.

A separate blind regeneration by another external executor independently reproduced the same substantive `SUPPORTS` versus `REFUTES` pattern on a distinct GPU/software stack, with a disclosed strict-parser boundary on a `Verdict: SUPPORTS` prefix.

These targeted runs support robustness of the decisive SciFact case. They do not replace the preregistered 800-query aggregate endpoint and are not CODECHECK certification.

## Install

```bash
pip install ridi-audit==1.1.1
ridi-audit demo
```

## Links

- PyPI: https://pypi.org/project/ridi-audit/
- Repository: https://github.com/adeebnoor/ridi
- Quick Start: https://github.com/adeebnoor/ridi/blob/main/docs/QUICKSTART.md
- Evidence: https://github.com/adeebnoor/ridi/blob/main/paper/README.md
- Reproducibility: https://github.com/adeebnoor/ridi/blob/main/docs/REPRODUCIBILITY.md

# Publish `ridi-audit` to PyPI

Public package: **https://pypi.org/project/ridi-audit/**

Current release: **`ridi-audit==1.1.1`**

The project is published through **PyPI Trusted Publishing (GitHub OIDC)**. No long-lived PyPI password or API token is stored in GitHub.

## Current trusted-publisher identity

| Field | Value |
|---|---|
| PyPI project | `ridi-audit` |
| GitHub owner | `adeebnoor` |
| GitHub repository | `ridi` |
| Workflow | `release.yml` |
| Environment | `pypi` |

The first trusted upload created the PyPI project successfully. The 1.1.1 release was then published through the same OIDC binding.

## Release pipeline

`.github/workflows/release.yml` performs, in order:

1. exact package-version verification;
2. the full test suite;
3. wheel and source-distribution build;
4. strict Twine metadata validation;
5. installation of the built wheel into a fresh virtual environment;
6. CLI and Python API smoke tests;
7. PyPI Trusted Publishing with PyPI/Sigstore attestations;
8. a second clean installation from the **public PyPI index** after publication;
9. another CLI/API smoke test against the public package.

The 1.1.1 public-index verification completed successfully.

## Current public install

```bash
pip install ridi-audit==1.1.1
ridi-audit --version
ridi-audit demo
```

Or simply install the latest release:

```bash
pip install ridi-audit
```

## 1.1.1 artifact hashes

- wheel SHA-256: `b91dcf6cf227a3a579d88318029c02d78e378d16510a2223d17223acbf7bb6f7`
- source distribution SHA-256: `a2af6f98171cb5b5a307911eeca2824dd401e014d595c6af69c94ddcf3d5440e`

The publishing action also generated upload attestations recorded in the public transparency infrastructure used by PyPI/Sigstore.

## Future releases

For each later version:

1. update the version in both `pyproject.toml` and `src/ridi_audit/__init__.py`;
2. update `CITATION.cff`, `CHANGELOG.md` and release notes;
3. require green CI on all supported Python versions;
4. run `Publish ridi-audit to PyPI` with the exact version, or publish a GitHub Release tagged `v<version>`;
5. require the public-index verification job to pass before considering the release complete.

PyPI versions are immutable. Never overwrite or reuse a published version.

## Security posture

- Publishing is isolated to `.github/workflows/release.yml`.
- `id-token: write` is scoped only to the publishing job.
- Build/test steps run separately without OIDC publishing permission.
- The `pypi` GitHub environment is part of the trusted identity.
- Release concurrency prevents overlapping uploads for the same ref.
- Trusted Publishing uses short-lived credentials rather than a stored PyPI token.
- PyPI attestations bind uploaded artifacts to the GitHub Actions publisher identity.

Review any proposed modification to `release.yml` as carefully as a package-upload credential.

## Scientific boundary

Publishing the software package does **not** imply peer review, journal acceptance, independent scientific certification or endorsement of the accompanying manuscript. Software release status and manuscript status remain separate.

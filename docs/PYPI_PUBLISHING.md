# Publish `ridi-audit` to PyPI

Public package target: **`ridi-audit`**  
Canonical project URL after the first successful upload: **https://pypi.org/project/ridi-audit/**

The repository is configured for tokenless publication using **PyPI Trusted Publishing (GitHub OIDC)**. No long-lived PyPI password or API token should be stored in GitHub.

## One-time PyPI account authorization

This is the only account-bound step. While signed in to PyPI, open:

**https://pypi.org/manage/account/publishing/**

Create a **pending GitHub Trusted Publisher** for a new project using these exact values:

| PyPI field | Exact value |
|---|---|
| PyPI project name | `ridi-audit` |
| GitHub owner | `adeebnoor` |
| GitHub repository | `ridi` |
| Workflow filename | `release.yml` |
| Environment | `pypi` |

Do not change capitalization, add `.github/workflows/` to the workflow field, or omit the environment. PyPI matches these fields against the OIDC claims emitted by the publishing job.

A pending publisher does **not** reserve the project name. The project is created only when the first trusted upload succeeds.

## First publication

After the pending publisher has been saved:

1. Open the repository's GitHub Actions page.
2. Select **Publish ridi-audit to PyPI**.
3. Choose **Run workflow** on `main`.
4. Enter version **`1.1.0`** exactly.
5. The workflow will:
   - verify the requested version against `pyproject.toml`;
   - run the test suite;
   - build wheel and source distributions;
   - run strict Twine metadata validation;
   - install the built wheel into a fresh virtual environment and smoke-test the public API and CLI;
   - upload through PyPI Trusted Publishing;
   - generate and upload PyPI/Sigstore attestations;
   - print distribution hashes in the workflow log.

On the first successful upload, PyPI creates the project and converts the pending publisher into a normal trusted publisher.

## Clean-install verification

After publication:

```bash
python -m venv /tmp/ridi-pypi-check
source /tmp/ridi-pypi-check/bin/activate
python -m pip install --upgrade pip
pip install ridi-audit==1.1.0
ridi-audit --version
ridi-audit demo
python - <<'PY'
from ridi_audit import audit, compare_allocations

result = compare_allocations(
    ['doc-1', 'doc-2', 'doc-3'],
    ['doc-1', 'doc-2', 'doc-4'],
)
assert result.changed_slots == 1
print('ridi-audit 1.1.0: clean PyPI install OK')
PY
```

On Windows, use the standard Windows virtual-environment activation command instead of `source`.

## Future releases

For each later version:

1. update the version in both `pyproject.toml` and `src/ridi_audit/__init__.py`;
2. update `CHANGELOG.md` and release notes;
3. require green CI on all supported Python versions;
4. publish a GitHub Release tagged exactly `v<version>`; the release workflow verifies that the tag matches package metadata before publishing.

PyPI versions are immutable. Never overwrite or reuse a published version.

## Security posture

- Publishing is isolated to `.github/workflows/release.yml`.
- `id-token: write` is scoped only to the publishing job.
- Build/test steps run in a separate job without OIDC publishing permission.
- The `pypi` GitHub environment is included in the trusted identity.
- Release concurrency prevents overlapping uploads for the same ref.
- Trusted Publishing generates short-lived credentials rather than storing a long-lived PyPI token.
- PyPI attestations bind uploaded artifacts to the GitHub Actions publisher identity.

Review any proposed modification to `release.yml` as carefully as a package-upload credential.

## Scientific boundary

Publishing the software package does **not** imply peer review, journal acceptance, independent certification, or endorsement of the accompanying manuscript. Software release status and manuscript status remain separate.

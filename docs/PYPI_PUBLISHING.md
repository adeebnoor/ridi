# PyPI publishing for `ridi-audit`

The repository is configured for tokenless PyPI publication using **PyPI Trusted Publishing (GitHub OIDC)**. No long-lived PyPI API token should be stored in GitHub.

## One-time PyPI account step

In PyPI, open your account sidebar → **Publishing**, then create a **pending trusted publisher** for a new project with these exact values:

- **PyPI project name:** `ridi-audit`
- **GitHub owner:** `adeebnoor`
- **GitHub repository:** `ridi`
- **Workflow filename:** `release.yml`
- **Environment:** `pypi`

The authorized workflow lives at `.github/workflows/release.yml` and grants `id-token: write` only to the publishing job.

## First publication

After the pending trusted publisher has been saved in PyPI:

1. Open **Actions → Publish ridi-audit to PyPI** in GitHub.
2. Choose **Run workflow** on `main`.
3. The workflow runs the tests, builds both wheel and source distribution, validates package metadata with Twine, then publishes through OIDC.
4. PyPI will create the `ridi-audit` project on first successful publication and convert the pending publisher into a normal trusted publisher.
5. Verify the package from a clean environment:

```bash
python -m venv /tmp/ridi-pypi-check
source /tmp/ridi-pypi-check/bin/activate
python -m pip install --upgrade pip
pip install ridi-audit==1.1.0
ridi-audit --version
ridi-audit demo
python - <<'PY'
from ridi_audit import audit, AuditReport
print('ridi-audit import OK')
PY
```

On Windows PowerShell, activate the virtual environment with the normal Windows activation command instead of `source`.

## Normal future releases

For later versions:

1. Update the version in `pyproject.toml` and `src/ridi_audit/__init__.py`.
2. Update `CHANGELOG.md` and release notes.
3. Ensure CI passes on Python 3.10–3.12.
4. Publish a GitHub Release for the version. The same workflow will publish the corresponding distributions automatically.

PyPI versions are immutable: never reuse an already-published version number.

## Security notes

- Keep publishing isolated to `.github/workflows/release.yml`.
- Keep `id-token: write` scoped to the publishing job only.
- Use the dedicated `pypi` GitHub environment; it can later be configured with manual approval rules if desired.
- Review any proposed changes to the release workflow as carefully as you would review a package-upload credential.

## Scientific boundary

Publishing the software package does **not** imply that the manuscript has been peer reviewed, accepted or published. The repository and package metadata should continue to state the manuscript status independently of the software release status.

# Scanner finding: archive worker
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: pyproject.toml, uv.lock, worker/, tests/; CI uses uv 0.9.5 with Python 3.12.
pyproject.toml [project].dependencies contains fixture-archive-stream==1.4.0.
uv.lock resolves fixture-archive-stream 1.4.0 for every supported platform.
Synthetic advisory FIXTURE-P-21 affects fixture-archive-stream >=1.4.0,<1.4.2.
Scanner location: uv.lock; the matching [project] declaration is a runtime dependency.
The supplied upstream note identifies 1.4.2 as fixed and compatible with Python 3.12.
No parent dependency or other version of this package occurs in the supplied lock summary.
The repository runs archive corruption and streaming-boundary tests with uv run pytest.
CI uses uv sync --locked and audits an exported runtime requirements selection.
Please propose the smallest change and distinguish planned checks from completed checks.

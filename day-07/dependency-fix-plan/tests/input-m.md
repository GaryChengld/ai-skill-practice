# Scanner finding: knowledge monorepo
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: web/package.json, web/package-lock.json, services/indexer/pyproject.toml, services/indexer/uv.lock.
web/package.json declares @fixture/search-shell@7.0.0; its lock summary has no scanner findings.
services/indexer/pyproject.toml declares fixture-index-client==2.8.0; this service uses uv 0.9.5.
services/indexer/uv.lock resolves fixture-index-client 2.8.0 -> fixture-linkdecode 2.3.1.
Synthetic advisory FIXTURE-M-44 affects fixture-linkdecode >=2.3.0,<2.3.4; 2.3.4 fixes it.
The scanner's finding path is services/indexer/uv.lock, runtime graph, Python 3.12.
Supplied metadata: index-client 2.8.0 permits linkdecode >=2.3,<3; 2.8.1 requires >=2.3.4,<3.
The publisher describes index-client 2.8.1 as a compatible patch; the finding has one path.
The indexer runs link-normalization regression tests with uv run pytest and CI uses uv sync --locked.
What should we change, and how can we tell the affected service is fixed?

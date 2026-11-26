The next release tag should be **2.0.0** — a **major** bump.

The commit `fix(api): validate authorization on export requests` includes a breaking-change footer: exports no longer accept the legacy `X-Export-Token` header and require a bearer token instead.
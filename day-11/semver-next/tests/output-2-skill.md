The next release tag should be **2.0.0**, a major bump.

The deciding commit is `fix(api): validate authorization on export requests`: its `BREAKING CHANGE` footer says exports no longer accept the legacy `X-Export-Token` header and require a bearer token instead.
The next release tag should be **`0.10.0`**, a minor bump.

The deciding commit is `feat(config)!: replace timeout_ms with request_timeout`, which signals a breaking change. The major-zero policy lowers release bumps one level, so a breaking change raises the minor version while the major version is zero.
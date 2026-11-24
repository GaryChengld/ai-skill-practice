What commit message would you use for this staged diff?

- `src/config/options.ts`: remove the deprecated public `legacyMode` option. The config parser rejects files that still contain the key.
- `docs/config.md`: tell existing users to remove `legacyMode` from their config before upgrading.

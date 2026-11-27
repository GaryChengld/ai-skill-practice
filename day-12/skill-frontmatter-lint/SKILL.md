---
name: skill-frontmatter-lint
description: Check SKILL.md frontmatter for Agent Skills format and field errors. Use when a skill is not recognized, its setup looks wrong, or its metadata needs validation before publishing. Not for tuning description triggers, reviewing instruction quality, or checking MCP configuration.
compatibility: Requires uv with Python 3.10 or newer, or Python 3.10 or newer with PyYAML 6.0.3 already installed.
---

# Lint skill frontmatter

1. Identify the requested skill directories or `SKILL.md` files. Run the linter from the user's working directory, using the script's path inside this skill:

   ```text
   uv run "<skill-dir>/scripts/lint_frontmatter.py" PATH [PATH ...]
   ```

   Replace the placeholders, run it without reading its source, and wait for the result. If `uv` is unavailable and Python 3.10+ with PyYAML 6.0.3 is already installed, use `python3` or `python` with the same script and arguments. Otherwise tell the user which prerequisites are missing. Do not inspect the YAML and guess the result.
2. Use the exit status and output to decide what to report.
   - `0`: Report that there are no errors and include any warnings.
   - `1`: Relay the lint errors and warnings from `results`.
   - `2`: Relay the argument or path error from stderr and ask for a corrected path.
   - `3`: Relay `parse_error` for malformed files and any findings on the other files in the batch. Ask the user to fix parsing before rechecking that file.
   - `4`: Rerun with the `uv run` command printed on stderr. If `uv` is unavailable, explain the prerequisites. Do not substitute a manual YAML judgment.
3. For each finding, report its `field` and `line` when present, explain `message`, and preserve any concrete replacement in `fix`. Distinguish errors, warnings, and parse failures. Only report issues present in the tool result. Modify files only if the user asks.

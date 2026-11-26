---
name: semver-next
description: Calculate the next semantic version from commits since the last release tag. Use when asked what version or release tag comes next, or whether changes call for a major, minor, or patch bump. Not for writing commit messages, drafting release notes, or explaining SemVer concepts.
compatibility: Requires Python 3. Git is needed only when collecting commits from a repository.
---

# Next release version

1. Use the current version and commit file supplied by the user. When collecting commits from Git, confirm the starting tag and run the following from the repository, replacing `LAST_TAG` with the actual tag:

   ```text
   git log --no-merges --format="%B%n--END--" LAST_TAG..HEAD
   ```

   Check that Git succeeds, then save its output as UTF-8 or pass it on stdin. Each commit ends with a standalone `--END--` line. Ask which tag to use if the release line is unclear.
2. Run the script by its path inside this skill directory, from the user's working directory, so relative commit-file paths still resolve. Do not read the script's source. If `python3` is unavailable, use `python`.

   ```text
   python3 "<skill-dir>/scripts/next_version.py" --current v1.4.2 --commits commits.txt
   ```

   Substitute the actual skill path, version, and file. Use `--commits -` for stdin. Capture the process exit status and wait for it to finish before replying.
3. Handle the result by exit status:
   - `0`: Read the JSON. `current` is the input, `next` the resulting tag, and `bump` the effective change (`major`, `minor`, `patch`, or `none`). `major_zero_shift` says whether the major-zero policy was applied to a release bump. `reasons` lists the decisive `header` and `rule` pairs. `unparsed` lists ignored headers.
   - `2`: Report the diagnostic and request the corrected version or commit input it calls for. Leave the next tag unspecified.
   - `3`: Explain that a prerelease input cannot be used. Ask which stable tag or version line to continue and leave the next tag unspecified.
4. On success, state `next` and `bump`, then cite up to three deciding commits and their rules. When `major_zero_shift` is true, explain that this policy lowers bumps one level at major zero, with patch as the minimum. Breaking changes raise the minor version, and features, fixes, and performance changes raise the patch version. With `none`, say the current version stays the same. If `unparsed` is nonempty, mention the ignored commit headers. Use the provided version and bump exactly. Do not recompute or change them.

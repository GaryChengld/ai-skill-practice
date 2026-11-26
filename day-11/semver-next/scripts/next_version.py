"""Calculate the next release version from a stable version and commit messages."""

import argparse
import json
from pathlib import Path
import re
import sys


NUMBER = r"(?:0|[1-9][0-9]*)"
IDENTIFIERS = r"[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*"
VERSION = re.compile(
    rf"(?P<prefix>v?)(?P<major>{NUMBER})\.(?P<minor>{NUMBER})\.(?P<patch>{NUMBER})"
    rf"(?:-(?P<prerelease>{IDENTIFIERS}))?(?:\+{IDENTIFIERS})?"
)
HEADER = re.compile(r"(?P<type>[a-zA-Z][a-zA-Z0-9-]*)(?:\([^()\s]+\))?(?P<breaking>!)?: +\S.*")
BREAKING = re.compile(r"BREAKING(?: |-)CHANGE:")
BUMP_NAMES = ("none", "patch", "minor", "major")
DELIMITER = "--END--"


class PrereleaseVersion(ValueError):
    """A well-formed version outside the stable-release calculation policy."""


def parse_version(text):
    match = VERSION.fullmatch(text)
    guidance = "Pass a stable MAJOR.MINOR.PATCH version with --current, optionally prefixed with v."
    if match is None:
        raise ValueError(f"Invalid current version {text!r}. {guidance}")
    prerelease = match["prerelease"]
    if prerelease:
        if any(part.isdigit() and len(part) > 1 and part.startswith("0") for part in prerelease.split(".")):
            raise ValueError(f"Invalid current version {text!r}: prerelease numbers cannot have leading zeros. {guidance}")
        raise PrereleaseVersion(
            f"Cannot calculate a next release from prerelease {text!r}. "
            "Pass the last stable tag with --current and provide commits since that tag, "
            "or ask which stable version line to continue."
        )
    return match["prefix"], [int(match[field]) for field in ("major", "minor", "patch")]


def commit_messages(text):
    message = []
    for line in text.splitlines():
        if line == DELIMITER:
            if message:
                yield message
            message = []
        elif message or line.strip():
            message.append(line)
    if message:
        raise ValueError(f"The final commit has no {DELIMITER!r} line. Add it or regenerate the file with git log.")


def classify(header, body):
    match = HEADER.fullmatch(header)
    if match is None:
        return 0, None
    if match["breaking"]:
        return 3, "breaking_header"
    if any(BREAKING.match(line) for line in body):
        return 3, "breaking_footer"
    kind = match["type"].lower()
    return {"feat": 2, "fix": 1, "perf": 1}.get(kind, 0), kind


def next_release(current, prefix, parts, commits):
    highest = 0
    reasons = []
    unparsed = []
    for header, *body in commit_messages(commits):
        level, rule = classify(header, body)
        if rule is None:
            unparsed.append(header)
        if not level:
            continue
        if parts[0] == 0:
            level = 2 if level == 3 else 1
        if level > highest:
            highest = level
            reasons.clear()
        if level == highest:
            reasons.append({"header": header, "rule": rule})

    version = current
    if highest:
        changed = 3 - highest
        parts[changed] += 1
        parts[changed + 1:] = [0] * (2 - changed)
        version = prefix + ".".join(map(str, parts))
    return {"current": current, "next": version, "bump": BUMP_NAMES[highest],
            "reasons": reasons, "unparsed": unparsed}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Calculate a stable release version from Conventional Commits.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Input: UTF-8 commit messages, each ending with a separate --END-- line.
Reserve --END-- for the delimiter. To generate the input from a repository:
  git log --format="%B%n--END--" LAST_TAG..HEAD

Successful calculation writes one JSON object to stdout:
  current, next  Input and resulting version. A leading v is kept.
  bump           Effective bump: major, minor, patch, or none.
  reasons        Decisive commits as {header, rule} objects.
  unparsed       Unrecognized first lines excluded from the calculation.

Exit codes: 0 result (including none), 2 input error, 3 unsupported prerelease.
Errors go to stderr. --help prints this help and exits 0.""",
    )
    parser.add_argument("--current", required=True, metavar="VERSION", help="current version or tag")
    parser.add_argument("--commits", required=True, metavar="PATH", help="commit message file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        prefix, parts = parse_version(args.current)
        data = sys.stdin.buffer.read() if args.commits == "-" else Path(args.commits).read_bytes()
        result = next_release(args.current, prefix, parts, data.decode("utf-8-sig"))
    except PrereleaseVersion as error:
        print(error, file=sys.stderr)
        return 3
    except (OSError, UnicodeError) as error:
        print(f"Could not read {args.commits!r} as UTF-8: {error}. "
              "Pass a readable UTF-8 commits file or use --commits - for stdin.", file=sys.stderr)
        return 2
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

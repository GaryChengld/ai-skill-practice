"""Check three editorial conventions; this is not a schema validator."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "day-01/conventional-commits": 150,
    "day-02/release-notes": 40,
    "day-02/competitors/pr-description": None,
    "day-03/incident-postmortem": 80,
    "day-04/stale-branches": 60,
}


def inspect(folder, limit):
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    _, header, body = text.split("---", 2)
    descriptions = re.findall(r"^description: (.+)$", header, re.M)
    single = len(descriptions) == 1 and descriptions[0].strip() not in {">", ">-", "|", "|-"}
    # Continuation lines would violate this repository's single-line convention.
    if single:
        tail = header.split("description:", 1)[1].splitlines()[1:]
        single = not tail or not tail[0].startswith((" ", "\t"))
    description = descriptions[0] if descriptions else ""
    trigger = bool(re.search(r"\bUse (?:this skill )?when\b", description))
    lines = len(body.strip("\n").splitlines())
    cap = limit is None or lines <= limit
    return single, trigger, cap, lines


if __name__ == "__main__":
    failed = False
    for relative, limit in SKILLS.items():
        single, trigger, cap, lines = inspect(ROOT / relative, limit)
        print(f"{relative}: single={single}; use_when={trigger}; body={lines}/{limit or 'N/A'}")
        failed |= not (single and trigger and cap)
    raise SystemExit(int(failed))

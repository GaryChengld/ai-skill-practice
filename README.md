# ai-skill-practice

Daily hands-on practice for building **AI agent skills**: reusable folders of instructions, scripts and reference files that an AI agent loads when a task calls for them. The focus is the open Agent Skills format (`SKILL.md`), and the practice is not tied to any single vendor. The goal is skills that work across Claude, OpenAI Codex, GitHub Copilot, Cursor and other tools that support the format.

## How it works

A scheduled Claude task runs every morning at **9:54 (Toronto time)** and acts as a coach:

1. **Check:** It looks for the previous exercise's folder (`day-NN/`) on `main`.
2. **Gate:** If that exercise is missing or incomplete, **no new exercise is issued**. The run says what is missing and repeats the exercise brief instead.
3. **Review:** If it is complete, the run reviews it, lists what works, suggests concrete improvements, and gives a score from 1 to 5.
4. **Next exercise:** A new exercise (about 30 minutes) is posted in the task result, building on the curriculum and on weaknesses found in earlier reviews.

Exercises are delivered in the task result, not as files in this repo. Each answer goes in its own folder.

**Same-chat review:** After pushing an answer to `main`, I reply "done" in that morning's chat. The coach pulls the latest code, reviews it and suggests changes. I can revise and ask again as many times as needed. The next morning's run only confirms the final state before issuing the next exercise.

## Repository layout

```
ai-skill-practice/
├── README.md
├── .practice/            # Managed by the coach. Please don't edit by hand.
│   ├── curriculum.md     # Roughly 30-day staged syllabus
│   └── log.md            # Exercises issued, completion checks, reviews, scores
├── day-01/               # My answer to exercise 1
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── scripts/      # optional
│       └── references/   # optional
├── day-02/
└── ...
```

## Conventions

- **Folder name:** Use `day-NN` with two digits (`day-01`, `day-02`, …), matching the exercise number in the task result. The number is the exercise sequence, not the calendar day, so a missed day doesn't skip a number.
- **Language:** All skill content is written in **English**: names, `description`, instructions, scripts and comments. Coaching and reviews are in Chinese.
- **Done means:** Every item in the exercise's completion checklist is met and the work is committed and pushed to `main` before the next 9:54 run. Empty or placeholder files don't count.
- **Notes (optional):** Add a short `day-NN/NOTES.md` with what I tried, what was hard, and any open questions. The coach reads it during review.

## Skill format quick reference

A skill is a folder whose entry point is `SKILL.md`: YAML frontmatter followed by Markdown instructions.

```markdown
---
name: example-skill
description: One or two sentences saying what the skill does and exactly when an agent should use it.
---

# Example Skill

Step-by-step instructions the agent follows once the skill is loaded.
Point to files in references/ or scripts/ only when they are needed.
```

Principles practiced here:

- **The description does the triggering.** The agent decides whether to load a skill from its name and description alone, so they must be specific about *when* the skill applies.
- **Progressive disclosure.** Keep `SKILL.md` focused, and move long reference material into separate files that are loaded only when needed.
- **Scripts for deterministic work.** Use code for steps that must be exact, such as parsing, validation or formatting, rather than asking the model to improvise them.
- **Portability.** Avoid vendor-specific assumptions unless the exercise asks for them.
- **Test it.** Check that the skill triggers on the right requests, stays quiet on the wrong ones, and produces the expected output.

## Progress

See [`.practice/log.md`](.practice/log.md) for the full history of exercises, completion checks and review scores. The coach creates this file on its first run.

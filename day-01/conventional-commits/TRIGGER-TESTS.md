# Trigger Tests — Conventional Commits Skill

## Purpose

Verify that the `conventional-commits` skill activates when users request Conventional Commits messages and does not activate for unrelated Git operations or writing tasks.

## Positive Tests — Should Trigger

| ID | User Prompt | Reason | Actual |
| --- | --- | --- | --- |
| P01 | Write a commit message for my staged changes. | Explicitly requests a commit message based on staged changes. | LOAD (pass) |
| P02 | Suggest a Conventional Commits message for this git diff. | Directly requests a Conventional Commits message from a diff. | LOAD (pass) |
| P03 | What should my commit message be for these changes? | Requests help generating a commit message. | LOAD (pass) |
| P04 | Help me prepare a git commit message for my latest changes. | Explicitly asks for a git commit message. | LOAD (pass) |
| P05 | I fixed a null pointer exception in the authentication service. How should I commit this? | Implicitly asks for a commit message describing a bug fix. | LOAD (pass) |

## Negative Tests — Should NOT Trigger

| ID | User Prompt | Reason | Actual |
| --- | --- | --- | --- |
| N01 | Explain how git rebase works. | Requests an explanation of Git functionality, not a commit message. | SKIP (pass) |
| N02 | Write a pull request description for my changes. | Requests a PR description rather than a commit message. | SKIP (pass) |
| N03 | How can I undo my last git commit? | Requests Git troubleshooting, not message generation. | SKIP (pass) |
| N04 | Review my staged changes for potential bugs. | Requests code review, not a Conventional Commits message. | SKIP (pass) |
| N05 | Show me the differences between my current branch and main. | Requests a diff comparison without asking for a commit message. | SKIP (pass) |

## Recorded Run - 2026-10-19

- Tool: `collaboration.spawn_agent`, one fresh agent per case with `fork_turns: "none"`; task names `routing_p01` through `routing_p05` and `routing_n01` through `routing_n05`.
- Method: Give each agent only the updated skill name and description, one user prompt, and instructions to return `LOAD` or `SKIP` with a reason. Do not provide expected results or ask it to carry out the user request.
- Results: 10/10 metadata-routing decisions matched expectations. P05 was recognized as a request for a bug-fix commit message; N02 was skipped because PR descriptions are explicitly excluded.
- Limitation: `Actual` records metadata-routing decisions, not observed skill activation in the application. Agents did not load the skill body or execute Git operations. Full application activation testing remains pending; the installed skill copy was not updated by this run.

## Execution Instructions

1. Load the Agent with the `conventional-commits` skill available.
2. Run each test prompt in an independent conversation.
3. Record whether the skill was actually activated using observable skill-loading evidence. Identify the tool, date, and test method; distinguish metadata-routing decisions from application activation.
4. Compare the actual behavior against the expected behavior.
5. Investigate any incorrect activation or missed activation.
6. Refine the skill description if necessary and repeat the tests.

# Trigger Tests — Conventional Commits Skill

## Purpose

Verify that the `conventional-commits` skill activates when users request Conventional Commits messages and does not activate for unrelated Git operations or writing tasks.

## Positive Tests — Should Trigger

| ID  | User Prompt                                                                               | Reason                                                        |
| --- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| P01 | Write a commit message for my staged changes.                                             | Explicitly requests a commit message based on staged changes. |
| P02 | Suggest a Conventional Commits message for this git diff.                                 | Directly requests a Conventional Commits message from a diff. |
| P03 | What should my commit message be for these changes?                                       | Requests help generating a commit message.                    |
| P04 | Help me prepare a git commit message for my latest changes.                               | Explicitly asks for a git commit message.                     |
| P05 | I fixed a null pointer exception in the authentication service. How should I commit this? | Implicitly asks for a commit message describing a bug fix.    |

## Negative Tests — Should NOT Trigger

| ID  | User Prompt                                                 | Reason                                                              |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------- |
| N01 | Explain how git rebase works.                               | Requests an explanation of Git functionality, not a commit message. |
| N02 | Write a pull request description for my changes.            | Requests a PR description rather than a commit message.             |
| N03 | How can I undo my last git commit?                          | Requests Git troubleshooting, not message generation.               |
| N04 | Review my staged changes for potential bugs.                | Requests code review, not a Conventional Commits message.           |
| N05 | Show me the differences between my current branch and main. | Requests a diff comparison without asking for a commit message.     |

## Execution Instructions

1. Load the Agent with the `conventional-commits` skill available.
2. Run each test prompt in an independent conversation.
3. Record whether the skill was activated.
4. Compare the actual behavior against the expected behavior.
5. Investigate any incorrect activation or missed activation.
6. Refine the skill description if necessary and repeat the tests.

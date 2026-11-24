# Behavior checklist

Score each item independently using the final response. Match the meaning of the text and accept equivalent wording. A commit header must use standard Conventional Commits syntax with an optional scope.

| Input | ID | Pass criterion |
| --- | --- | --- |
| 1 | 1a | The commit header uses `fix`. |
| 1 | 1b | The message identifies refreshing an expired access token before retrying, or preventing the resulting 401 retry loop through token refresh. |
| 1 | 1c | The response puts the proposed message in a fenced code block. |
| 2 | 2a | The proposed message identifies the removal of `legacyMode`. |
| 2 | 2b | The proposed message uses `!` before the header colon or an uppercase `BREAKING CHANGE:` footer. |
| 2 | 2c | The proposed message says users must remove `legacyMode` from their config before upgrading or to use the new version. |
| 3 | 3a | The response recommends splitting the changes into separate commits. |
| 3 | 3b | The response proposes a `feat` header for CSV export. |
| 3 | 3c | The response proposes a `fix` header for the login timeout. |
| 4 | 4a | The response says the staged diff is empty. |
| 4 | 4b | The response asks for a diff or change summary before drafting. |
| 4 | 4c | The response proposes no commit message. |

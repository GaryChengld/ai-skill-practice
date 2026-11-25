# Follow-up evaluation rubric

Use the original `PLAN.md` criteria for inputs 1–4. Score these additional content checks for input 5 with the same model, ordinary prompt, and BEFORE, AFTER, and no-skill comparison. Commit this rubric and the fixture before those sessions.

| ID | Pass criterion |
| --- | --- |
| 5a | States that the table size is unknown and explicitly assesses the volatile-default rewrite as if the table were large until the size is confirmed. Merely noting that a rewrite might be expensive on large tables does not pass. |
| 5b | Asks the author to confirm whether deployed code, jobs, or other application consumers still use the column's old name. A generic compatibility warning alone does not pass. |
| 5c | Explains a compatible sequence if consumers still use the old name, such as adding the replacement first, migrating consumers, then retiring the old column. A suggestion to coordinate a rename without a transition sequence does not pass. |

Score report structure separately. An AFTER response passes the format check only if its title and metadata, findings table, rollout list, and author questions conform to the template, without standalone prose between sections. The matrix check verifies that the required rows were available in the tool result. The review may read the entire CSV.

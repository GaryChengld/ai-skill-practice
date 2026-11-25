# Day 10 validation and evaluation notes

The BEFORE text and behavior rubric were frozen in `c62bfd5` before the first evaluation. The sessions used identical fixture copies and the same model and behavior prompts. Session-local registries exposed either BEFORE, AFTER, or zero skills.

`agentskills` was unavailable. The official reference validator exited with code 0.

```text
> skills-ref validate day-10\migration-safety-review
Valid skill: day-10\migration-safety-review
```

The first AFTER runs selected the correct database reference but read the whole risk matrix. The [initial excerpts and manifest](migration-safety-review/tests/harness/initial-after/) record those reads. The revised body orders classification before asset access and requires a filtered or row-range read. The behavior fixtures and rubric stayed fixed.

Two revised MySQL runs fetched speculative matrix rows. The final body asks reviewers to record unverified conditions as questions and look up only the chosen size/effect pairs. One T1 run could not open the skill due to a Windows sandbox error, and one input 2 run ended before its fallback reader returned the SQL. The [retry evidence](migration-safety-review/tests/harness/retries/) retains these runs.

Input 3 gives the target type and leaves the source column definition unknown. Responses earn credit for identifying the blocking copy conditionally and asking for the source definition. That respects the evidence available in a standalone migration.

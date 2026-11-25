# Day 10 validation and evaluation notes

The BEFORE text and behavior rubric were frozen in `c62bfd5` before the first evaluation. The sessions used identical fixture copies and the same model and behavior prompts. Session-local registries exposed either BEFORE, AFTER, or zero skills.

`agentskills` was unavailable. The official reference validator exited with code 0.

```text
> skills-ref validate day-10\migration-safety-review
Valid skill: day-10\migration-safety-review
```

The first AFTER runs selected the correct database reference but read the whole risk matrix. The [initial excerpts and manifest](migration-safety-review/tests/harness/initial-after/) record those reads. The revised body orders classification before asset access and requires a filtered or row-range read. The behavior fixtures and rubric stayed fixed.

Two revised MySQL runs fetched speculative matrix rows during the original evaluation. One T1 run could not open the skill due to a Windows sandbox error, and one input 2 run ended before its fallback reader returned the SQL. The [retry evidence](migration-safety-review/tests/harness/retries/) retains these runs.

Input 3 gives the target type and leaves the source column definition unknown. Responses earn credit for identifying the blocking copy conditionally and asking for the source definition. That respects the evidence available in a standalone migration.

## Follow-up evaluation

The updated skill reads the small matrix as a normal file and applies the selected rows. The stricter template checker rejects the original MySQL answer in `da26c44` because it places a source paragraph outside the findings table. The five new AFTER answers passed the stricter check. The three unit tests also exercise a valid citation in the Why column, a nested SQL block, and invalid section content.

Inputs 1–4 reuse the original BEFORE and no-skill sessions. Input 5 compares three fresh sessions against criteria frozen in `72801c8`. All five AFTER sessions and three trigger sessions were run against the revised skill. The reference validator again returned `Valid skill: day-10\migration-safety-review`.

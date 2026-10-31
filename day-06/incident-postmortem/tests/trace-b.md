# INC-826 behavioral-test read trace

## Successful content reads, in exact order

1. `C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/SKILL.md`
   - Tool: `functions.exec` → `tools.exec_command`
   - Operation: `type C:\Workspaces\ai-skill-practice\day-06\incident-postmortem\SKILL.md`
   - Shell: `C:/Windows/System32/cmd.exe`; `login:false`; `sandbox_permissions:require_escalated`.
2. `C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/tests/input-b.md`
   - Tool: `functions.exec` → `tools.exec_command`
   - Operation: `type C:\Workspaces\ai-skill-practice\day-06\incident-postmortem\tests\input-b.md`
   - Shell: `C:/Windows/System32/cmd.exe`; `login:false`; `sandbox_permissions:require_escalated`.
3. `C:/Workspaces/ai-skill-practice/day-06/incident-postmortem/references/timezones.md`
   - Tool: `functions.exec` → `tools.exec_command`
   - Operation: `type C:\Workspaces\ai-skill-practice\day-06\incident-postmortem\references\timezones.md`
   - Shell: `C:/Windows/System32/cmd.exe`; `login:false`; `sandbox_permissions:require_escalated`.
   - Trigger: Sources span multiple timezones and a backward DST transition, with an ambiguous repeated-hour timestamp.

## Failed attempts

None.

## Directory listings

None.

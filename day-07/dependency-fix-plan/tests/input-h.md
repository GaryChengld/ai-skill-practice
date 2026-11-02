# Scanner finding: legacy schedule runner
This is a fictional repository and synthetic advisory data, not a live vulnerability report.
Files: requirements.in, requirements.txt, schedules/, tests/; CI uses pip on Python 3.9.
requirements.in directly pins fixture-calendar-engine==3.8.0.
The supplied resolved graph is calendar-engine 3.8.0 -> fixture-rule-eval 1.6.0, pinned exactly by the parent.
Synthetic advisory FIXTURE-H-06 affects rule-eval >=1.6.0,<2.0.0; the only fixed release is 2.0.0.
Scanner location: requirements.txt, runtime graph; this is the only affected path.
The supplied publisher metadata says rule-eval 2.0.0 requires Python >=3.11 and removes the API used by the parent.
No compatible calendar-engine release or backported rule-eval fix exists in the supplied release inventory.
This release must support Python 3.9; replacing the engine or migrating the interpreter is outside its approved scope.
The exploit requires enabling custom rule uploads; deployments can disable that feature while preserving built-in schedules.
The schedules team owns the component; the release review is scheduled for 2026-11-09.
What should we do for this release, and what evidence would let us revisit that decision?

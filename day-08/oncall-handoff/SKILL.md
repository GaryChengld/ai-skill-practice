---
name: oncall-handoff
description: Turn end-of-shift alerts, unfinished work, and watch notes into an on-call handoff for the next responder. Use when someone is handing over a shift or needs a handoff for an automation. Excludes incident postmortems and on-call rota planning.
---

# On-call handoff

Use the supplied shift notes, including any shift window, responders, alerts, and follow-up work they identify. Ask for the notes if none are supplied.

- Use facts from the notes. Preserve full service and person names, ticket IDs, timestamps with any supplied time zone, and declared severities. Use `Unknown` for missing details and ask specific open questions about gaps the next responder needs to resolve.
- Markdown is the default. For Markdown, open `assets/handoff-template.md` and copy it verbatim before filling every placeholder. Keep its headings, order, entry labels, and punctuation exactly as written. Repeat entry lines as needed and use `None reported` in sections with no entries.
- Only when the user asks for JSON, open `assets/handoff.schema.json` instead of the Markdown template. Return a raw JSON object. Check it against the schema before returning and use empty arrays for sections with no entries.
- For each open item without a declared severity, use the supplied impact and urgency to retrieve only the matching row from `assets/severity-matrix.csv`. Use a line filter with the exact impact and urgency as its first two columns. Use the row's severity. If either value is absent or the lookup has no match, use `Unknown` and add an open question naming the item and the missing or unrecognized value. Skip the lookup entirely if either value is absent.

Before returning, check that the output fits the requested format, the facts match the notes, and each unknown severity from missing lookup data has an open question.

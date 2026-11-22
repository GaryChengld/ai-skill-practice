---
name: oncall-handoff
description: Turn end-of-shift notes (alerts, open work, watch items) into an on-call handoff for the next responder, as Markdown or as JSON for a bot. Use when someone is ending an on-call shift and asks for a handoff or shift summary. Not for incident postmortems or on-call rota planning.
---

# On-call handoff

Use the supplied shift notes, including any shift window, responders, alerts, and follow-up work they identify. Ask for the notes if none are supplied.

- Use facts from the notes. Preserve full service and person names, ticket IDs, timestamps with any supplied time zone, and declared severities. Use `Unknown` for missing details and ask specific open questions about gaps the next responder needs to resolve.
- Markdown is the default. For Markdown, open `assets/handoff-template.md` and copy it verbatim before filling the placeholders. Preserve the headings, order, entry labels, and punctuation in every section. Put one entry on each line. For an empty list section, replace the entry line with the standalone sentence `None reported.`
- Only when the user asks for JSON, open `assets/handoff.schema.json` instead of the Markdown template. Return a raw JSON object. Check it against the schema before returning and use empty arrays for sections with no entries.
- For each open item without a declared severity, if impact or urgency is missing, skip the lookup, use `Unknown`, and add an open question naming the item and the missing value. Otherwise read only the row of `assets/severity-matrix.csv` whose impact and urgency match exactly and use its severity. If no row matches, use `Unknown` and ask for the item's impact and urgency to be confirmed.

Before returning, check that the output fits the requested format, the facts match the notes, and each unknown severity from missing lookup data has an open question.

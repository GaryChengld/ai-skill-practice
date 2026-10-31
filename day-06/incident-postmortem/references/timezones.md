# Timezone conversion

## Establish the basis
- Resolve each local timestamp using its date, region, and available numeric offset.
- Prefer an IANA zone such as `Europe/Berlin` over a seasonal abbreviation.
- Use date-specific timezone database rules; current offsets need not match historical ones.
- A fixed numeric offset identifies an instant but does not describe future DST behavior.
- If a region or date is unavailable, request it before asserting a conversion.
- Record the selected region and conversion basis in the timeline note.

## Convert and order
1. Convert each supported local instant independently; do not apply one offset to the whole incident.
2. Preserve the original timestamp alongside the converted event when needed for auditability.
3. Sort resolved events by their UTC instants, not by their local clock labels.
4. For unresolved events, record possible positions without implying a total order.
5. Calculate elapsed intervals between resolved instants, not by subtracting wall-clock labels.

## Spring gap: a nonexistent local time
During a forward clock change, some local labels never occur.
In `Europe/Berlin` on 2025-03-30, the clock jumps from 01:59:59 CET to 03:00:00 CEST.
A device log reporting `2025-03-30 02:20 Europe/Berlin` therefore has no valid local instant.
Do not silently shift it to 03:20; this would alter the source evidence.
Ask for the raw offset, clock configuration, or a correlated UTC event.
Some datetime libraries accept invalid wall times without raising an error.
Check validity by converting to UTC and back; a changed local label reveals the gap.

## Autumn fold: a repeated local time
During a backward clock change, one local label can represent two instants.
In `Europe/Berlin` on 2025-10-26, `02:20` occurs with both UTC+02:00 and UTC+01:00.
Those instants are `00:20Z` and `01:20Z`; neither is preferred without evidence.
Use an explicit offset, a recorded fold indicator, or a correlated event to disambiguate.
In libraries supporting a fold flag, fold 0 denotes the earlier occurrence and fold 1 the later.
A sequence number can constrain order but does not by itself supply an offset.

## Conversion review
- Verify which side of a transition each event occupies.
- Check whether two apparently identical labels are separate events or duplicate records.
- Note unsynchronized device clocks separately from DST ambiguity.
- Disclose unresolved order and avoid precise duration claims across unresolved endpoints.

Reference: [IANA timezone handling and folds](https://docs.python.org/3/library/zoneinfo.html).

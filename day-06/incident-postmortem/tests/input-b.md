# INC-826 source packet

Draft an internal post-incident review for the resolved document-search degradation.
The local date is 2026-11-01. The incident crossed the backward DST transition in America/New_York.
All clocks are synchronized; the supplied offsets are reliable.

- B1, 01:50 America/New_York (UTC-04:00): search replicas reported stale results after their update subscription stopped.
- B2, 14:05 Asia/Singapore (UTC+08:00): the operator confirmed the subscription lease had expired and enabled a new lease.
- B3, 01:12 America/New_York (UTC-05:00): all replicas reported current results.
- B4, 01:55 America/New_York, no offset recorded: a hand-written note says "replica check still stale." Its occurrence within the repeated hour is unverified.
- B5: the lease audit confirms no renewal was scheduled; the scheduler configuration omitted the lease-renewal task.
- B6: there was no lease-expiry alert. The affected document count is unknown.

Follow-up ownership and deadlines are unassigned.

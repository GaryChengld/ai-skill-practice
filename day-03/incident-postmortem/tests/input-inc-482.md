Slack export, #inc-482, 2026-10-14 (times in PT)
09:12 alert: checkout p95 latency 8s, error rate 23%
09:15 maria: I'm on it
09:21 maria: looks like db connection pool exhausted on orders-db
09:30 dev: rolled back deploy 7f3a (added retry loop to payment client)
09:34 errors dropping
09:41 all green
customers affected: ? maybe ~1.2k failed checkouts, finance to confirm
q: why didn't canary catch it? -> canary is only 2% traffic for 5 min

What should this commit say? Here's the staged diff summary:

- `src/auth/session.ts`: on the first 401 from an expired access token, refresh the token before retrying the request. Previously it retried with the expired token and got stuck in a 401 loop.
- `tests/auth/session.test.ts`: cover the successful retry after refresh.

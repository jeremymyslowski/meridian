# ID Format

All entity IDs in Meridian are **UUID v4** strings.

- Generated server-side via `gen_random_uuid()` in Postgres or `uuid4()` in Python
- Passed as strings in JSON API responses
- Never use integer auto-increment IDs
<!-- log-jam/README_player.md -->
# Log Jam (Misc)

A noisy web server is spewing logs. Somewhere in there is your flag.

## Your goal
1. Download logs from `/logs/` (this container is serving files on port **9999**).
2. Find **fragments** of a base64 message hidden across multiple log files.
3. Put fragments in order, concatenate, base64-decode → `CTF{...}`

## Where to start
- Search recursively for lines containing a fragment marker like `part-<n>/<N> data=<...>`.
- Expect decoys. Exact format matters.

Good luck & happy grepping!

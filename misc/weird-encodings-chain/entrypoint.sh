#!/usr/bin/env bash
set -euo pipefail

# 1) Choose/emit a flag
if [[ -z "${FLAG:-}" ]]; then
  # random 24-hex payload inside CTF{...}
  PAYLOAD=$(python - <<'PY'
import secrets,string
print(secrets.token_hex(12))
PY
)
  FLAG="CTF{${PAYLOAD}}"
fi

# 2) Persist the flag (private, never served directly)
mkdir -p /srv/app/app/challenge
echo -n "$FLAG" > /srv/app/app/challenge/flag.txt

# 3) Build weird.txt and hash.txt
python /srv/app/tools/build.py "$FLAG" >/dev/null

# 4) Launch the app
exec python /srv/app/app/app.py

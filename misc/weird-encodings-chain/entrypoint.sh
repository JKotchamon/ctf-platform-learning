#!/usr/bin/env bash
set -euo pipefail

# Always build challenge artifacts with the **static** flag
# Your tools/build.py should hard-code: CTF{onion_layers_are_fun}
python /srv/app/tools/build.py

# Launch the Flask app
# If your app.py already binds 0.0.0.0:8081, this just runs it.
# If it needs host/port args, uncomment the second line instead.
exec python /srv/app/app/app.py
# exec python /srv/app/app/app.py --host 0.0.0.0 --port "${PORT:-8081}"

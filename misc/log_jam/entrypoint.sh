#!/usr/bin/env bash
set -euo pipefail

# Ensure dirs exist
mkdir -p /app/logs

# Generate noisy logs + hidden fragments
python /app/generate_logs.py

# Create logs.zip with Python (no apt packages needed)
python - <<'PY'
import os, zipfile
root = "/app/logs"
zip_path = "/app/logs.zip"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for base, _, files in os.walk(root):
        for f in files:
            full = os.path.join(base, f)
            # include "logs/..." inside the zip
            zf.write(full, os.path.relpath(full, "/app"))
PY

echo "[*] Serving on http://0.0.0.0:9999 ..."
# Serve everything in /app (index.html, /logs/, README_player.md, logs.zip)
python -m http.server 9999 --directory /app

#!/usr/bin/env bash
# log-jam/entrypoint.sh
set -euo pipefail

mkdir -p /app/logs
python /app/generate_logs.py

# Optional: provide a quick landing page
cat > /app/index.html <<'HTML'
<!DOCTYPE html>
<html>
  <head><meta charset="utf-8"><title>Log Jam</title></head>
  <body>
    <h1>Log Jam</h1>
    <p>Download logs from <a href="/logs/">/logs/</a> and find the flag.</p>
    <p>Player brief: see <a href="/README_player.md">README_player.md</a>.</p>
  </body>
</html>
HTML

# Serve everything under /app (directory listing enabled)
echo "[*] Serving on http://0.0.0.0:8080 ..."
python -m http.server 8080 --directory /app
#!/bin/sh
set -e

# 1) Get the dynamic flag from GZCTF. (Injected by the platform.)
#    For local testing, you can override it when running `docker run -e GZCTF_FLAG=...`
FLAG="${GZCTF_FLAG:-flag{LOCAL_TEST}}"

# 2) Write the flag to a root-level file that's readable by the app user.
echo "$FLAG" >/flag.txt
chmod 644 /flag.txt

# (Optional cosmetics) ensure demo files exist in case the image builder forgot:
mkdir -p /app/files/manuals /app/files/logs
[ -f /app/files/manuals/readme.txt ] || echo "Welcome! These are public documents." >/app/files/manuals/readme.txt
[ -f /app/files/logs/app.log ] || printf "[info] boot ok\n" >/app/files/logs/app.log

# 3) Launch the app
exec gunicorn -w 2 -b 0.0.0.0:6666 app:app

#!/bin/sh
# Save dynamic flag into /flag.txt
echo "${GZCTF_FLAG}" > /flag.txt

# Start the app
exec python /app/app.py

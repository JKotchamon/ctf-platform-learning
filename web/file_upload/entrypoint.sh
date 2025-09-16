#!/bin/sh
set -eu

# Where uploads live in the image
UPLOAD_DIR="/var/www/html/uploads"

# Ensure uploads exists and is writable by Apache/PHP user
mkdir -p "$UPLOAD_DIR"
chown -R www-data:www-data "$UPLOAD_DIR"
chmod 775 "$UPLOAD_DIR"

# Dynamic flag (GZCTF provides GZCTF_FLAG at runtime; fallback for local testing)
FLAG_VALUE="${GZCTF_FLAG:-flag{LOCAL_TEST_FLAG}}"

# Write the flag inside uploads as 'flag'
printf '%s\n' "$FLAG_VALUE" > "$UPLOAD_DIR/flag"
chown www-data:www-data "$UPLOAD_DIR/flag"
chmod 440 "$UPLOAD_DIR/flag"

# Prevent env-leak solves (players must RCE and cat the file)
unset GZCTF_FLAG FLAG_VALUE 2>/dev/null || true

# Launch Apache in foreground
exec apache2-foreground

#!/usr/bin/env bash
set -e
: "${PORT:=6666}"
echo "[*] Starting Acme Intranet on 0.0.0.0:${PORT}"
exec python app.py

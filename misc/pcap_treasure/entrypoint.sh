#!/bin/sh
set -eu

# Run inside the web package so relative imports work
cd /app/web

# 1) Generate the PCAP (uses FLAG / PCAP_MODE / PCAP_DIR / PCAP_NAME)
python generate_pcap.py

# 2) Start Flask
export FLASK_APP=app:app
exec python -m flask run --host=0.0.0.0 --port=8080

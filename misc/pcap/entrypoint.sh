#!/bin/sh
set -eu

cd /app

# Generate PCAP (uses FLAG / PCAP_MODE / PCAP_DIR / PCAP_NAME)
python generate_pcap.py

# Start Flask
export FLASK_APP=app:app
exec python -m flask run --host=0.0.0.0 --port=8080

#!/usr/bin/env bash
set -euo pipefail

# 1) generate a pcap on every start (picks up env FLAG and mode)
python /app/web/generate_pcap.py

# 2) run the web app
exec python -m flask run --host=0.0.0.0 --port=8080

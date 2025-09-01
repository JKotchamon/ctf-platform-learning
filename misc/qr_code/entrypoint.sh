# entrypoint.sh
#!/usr/bin/env bash
set -euo pipefail
python generate_assets.py
python app.py

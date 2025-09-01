#!/usr/bin/env bash
set -euo pipefail

# Cross-platform Python resolver (prefer python, then python3, then py)
PYTHON_BIN=$(command -v python || true)
if [[ -z "${PYTHON_BIN}" ]]; then
  PYTHON_BIN=$(command -v python3 || true)
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  PYTHON_BIN=$(command -v py || true)
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "Python not found. Install Python 3 and ensure it is on PATH." >&2
  exit 1
fi

variant="${1:-}"
flag_default="CTF{hello_stego}"
flag="${2:-$flag_default}"

if [[ "$variant" != "medium" ]]; then
  echo "Usage: ./build.sh medium [FLAG]" >&2
  exit 1
fi

# Prepare dist
rm -rf dist && mkdir -p dist/files

# 1) Generate the artifact image (does NOT touch your HTML/CSS/JS)
"$PYTHON_BIN" generators/make_png_lsb.py --out dist/files/cover.png --flag "$flag"

# 2) Make sure your static files exist (you created these manually)
#    - dist/index.html
#    - dist/style.css
#    - dist/app.js

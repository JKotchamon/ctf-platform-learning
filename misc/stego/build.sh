#!/usr/bin/env bash
set -euo pipefail

# Cross‑platform Python resolver (prefer python, then python3, then py)
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

echo "Using Python at: ${PYTHON_BIN}"

variant="${1:-}"
flag_default="CTF{hello_stego}"
flag="${2:-$flag_default}"

if [[ "$variant" != "medium" ]]; then
  echo "Usage: ./build.sh medium [FLAG]" >&2
  exit 1
fi

# Clean dist
rm -rf dist && mkdir -p dist/files

# Generate artifact
"$PYTHON_BIN" generators/make_png_lsb.py --out dist/files/cover.png --flag "$flag"

# Page content
title="Pixels Speak (Medium)"
desc="Pixels rarely lie. Some speak very softly. Can you hear them?"
image="cover.png"
port=8081

# Create index.html
cat > dist/index.html <<HTML
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="robots" content="noindex,nofollow" />
    <title>CTF Stego – ${title}</title>
    <style>
      body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Helvetica,Arial,sans-serif;line-height:1.45;margin:0;background:#0b1020;color:#e8ecff}
      .wrap{max-width:820px;margin:48px auto;padding:0 20px}
      .card{background:#121936;border:1px solid #2a345f;border-radius:16px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
      h1{margin:.2em 0;font-size:28px}
      p{opacity:.9}
      a.btn{display:inline-block;margin-top:10px;padding:10px 14px;border-radius:10px;border:1px solid #314083;text-decoration:none;color:#e8ecff}
      code{background:#0a0f1f;padding:2px 6px;border-radius:6px;border:1px solid #1d274a}
      footer{opacity:.7;margin-top:18px;font-size:12px}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="card">
        <h1>${title}</h1>
        <p>${desc}</p>
        <p>Download the artifact: <a class="btn" href="files/${image}">files/${image}</a></p>
        <hr style="border-color:#2a345f;border-width:1px 0 0">
        <p><strong>Rules:</strong> Flag format is <code>CTF{...}</code>. No bruteforce needed. Standard desktop tools allowed.</p>
        <footer>Hosted by Dockerized Nginx. Good luck! 🕵️‍♂️</footer>
      </div>
    </div>
  </body>
</html>
HTML

# Build image (standard Dockerfile at project root)
DOCKER_BUILDKIT=1 docker build -t ctf-stego-medium .

echo "
Built image: ctf-stego-medium"
echo "Run with Compose: docker compose up -d"
echo "Or plain Docker: docker run --rm -p ${port}:80 ctf-stego-medium"
```bash
#!/usr/bin/env bash
set -euo pipefail

# Cross‑platform Python resolver (python3 → python → py)
PYTHON_BIN=$(command -v python || true)
if [[ -z "${PYTHON_BIN}" ]]; then
  PYTHON_BIN=$(command -v python3 || true)
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  PYTHON_BIN=$(command -v py || true)
fi

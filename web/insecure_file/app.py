from flask import Flask, request, send_file, render_template, abort, Response
import os
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"  # supposed “safe” directory

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download")
def download():
    # Vulnerable: trusts string prefix on a *non-normalized* join result.
    name = request.args.get("file", "")
    if not name:
        return Response("Missing 'file' parameter", status=400, mimetype="text/plain")

    # Join BEFORE normalization; allows '../../' to escape later.
    full = os.path.join(str(FILES_DIR), name)

    # Naive, string-based prefix check (bypassable with '../'):
    if not full.startswith(str(FILES_DIR)):
        # Blocks absolute paths like /etc/passwd, but not ../../ escapes.
        abort(403)

    try:
        # If traversal escaped FILES_DIR, OS will resolve it at open-time.
        return send_file(full, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/healthz")
def healthz():
    return "ok"

if __name__ == "__main__":
    # For local tests only; production uses gunicorn from start.sh
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "6666")))

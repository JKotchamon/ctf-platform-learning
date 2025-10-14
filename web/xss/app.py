import os
import sqlite3
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, Response
from datetime import datetime
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

DB_PATH = Path("comments.db")
EXFIL_LOG = []
app = Flask(__name__)

FLAG = os.environ.get("GZCTF_FLAG", "flag{this_is_a_static_flag}")

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()
init_db()

@app.get("/")
def root():
    return send_from_directory(".", "index.html")

@app.get("/style.css")
def style():
    return send_from_directory(".", "style.css")

@app.get("/healthz")
def health():
    return "ok"

@app.get("/api/comments")
def api_comments():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT id, name, content, created_at FROM comments ORDER BY id DESC LIMIT 50"
    ).fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

@app.post("/api/comment")
def api_comment_create():
    payload = request.form if request.form else (request.json or {})
    name = (payload.get("name") or "anon")[:32]
    content = (payload.get("content") or "").strip()
    if not content:
        return jsonify({"ok": False, "msg": "content required"}), 400
    if len(content) > 800:
        return jsonify({"ok": False, "msg": "content too long"}), 400

    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO comments(name, content, created_at) VALUES(?, ?, ?)",
        (name, content, datetime.utcnow().isoformat() + "Z"),
    )
    con.commit()
    con.close()
    return jsonify({"ok": True})

def admin_visit(base_url: str, path: str):
    """
    Visit {base_url}{path} with a headless admin browser that carries a readable cookie FLAG=<flag>.
    base_url includes scheme+host(+port), e.g. http://host:12345
    """
    if not path.startswith("/"):
        raise ValueError("Path must start with '/'")
    base = base_url.rstrip("/")
    target = f"{base}{path}"

    parsed = urlparse(base)
    cookie_domain = parsed.hostname or "127.0.0.1"

    with sync_playwright() as p:
        # Important flags for containers/sandboxes:
        # --no-sandbox: avoid sandbox requirement (CTF platforms often run as root in containers)
        # --disable-dev-shm-usage: avoid crashing on small /dev/shm
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
        )
        context = browser.new_context()
        context.add_cookies([{
            "name": "FLAG",
            "value": FLAG,
            "domain": cookie_domain,
            "path": "/"
        }])
        page = context.new_page()
        page.goto(target, wait_until="domcontentloaded", timeout=20000)
        # Give payloads time to run (e.g., async exfil)
        page.wait_for_timeout(5000)
        browser.close()

@app.get("/report")
def report():
    """
    Players click 'Report' -> we build base_url from the *actual* request host:port,
    unless ADMIN_BASE_URL is set to override (for reverse proxies).
    """
    path = request.args.get("path", "/")
    base_url = (os.environ.get("ADMIN_BASE_URL") or request.host_url).rstrip("/")
    try:
        admin_visit(base_url, path)
        return jsonify({"ok": True, "visited": f"{base_url}{path}"})
    except Exception as e:
        # Show exactly what we tried so you can see host:port
        return jsonify({"ok": False, "error": str(e), "target": f"{base_url}{path}"}), 500

@app.get("/x")
def collector():
    # Operator-only exfil view (players should exfil to their own host)
    q = dict(request.args)
    logline = {"time": datetime.utcnow().isoformat()+"Z", "data": q,
               "ua": request.headers.get("User-Agent", "")}
    EXFIL_LOG.append(logline)
    print("[EXFIL]", logline, flush=True)
    return Response(status=204)

if __name__ == "__main__":
    # Local dev only; use gunicorn in Docker
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8888")), debug=False)

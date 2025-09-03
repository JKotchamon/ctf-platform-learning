import os
import sqlite3
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, Response, make_response
from datetime import datetime

# Playwright (sync) for the admin bot
from playwright.sync_api import sync_playwright

DB_PATH = Path("comments.db")
EXFIL_LOG = []  # in-memory for operator visibility (players can't read this)

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

@app.after_request
def add_headers(resp):
    # Deliberately permissive CSP to allow inline JS for the challenge
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp

@app.get("/")
def root():
    # Serve the flat HTML file from current dir
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
    rows = con.execute("SELECT id, name, content, created_at FROM comments ORDER BY id DESC LIMIT 50").fetchall()
    con.close()
    data = [dict(r) for r in rows]
    return jsonify(data)

@app.post("/api/comment")
def api_comment_create():
    # Accept form or JSON
    name = (request.form.get("name") or (request.json or {}).get("name") or "anon")[:32]
    content = (request.form.get("content") or (request.json or {}).get("content") or "").strip()
    if not content:
        return jsonify({"ok": False, "msg": "content required"}), 400
    if len(content) > 800:
        return jsonify({"ok": False, "msg": "content too long"}), 400

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO comments(name, content, created_at) VALUES(?, ?, ?)",
                (name, content, datetime.utcnow().isoformat()+"Z"))
    con.commit()
    con.close()
    return jsonify({"ok": True})

def admin_visit(path: str):
    """
    Launch a headless Chromium that visits http://127.0.0.1:8888{path}
    with a readable cookie containing the flag (no HttpOnly).
    """
    if not path.startswith("/"):
        raise ValueError("Path must start with '/'")

    target = f"http://127.0.0.1:8888{path}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()  # default = not HttpOnly, readable by JS
        # Set cookie for 127.0.0.1
        context.add_cookies([{
            "name": "FLAG",
            "value": FLAG,
            "domain": "127.0.0.1",
            "path": "/"
        }])
        page = context.new_page()
        try:
            page.goto(target, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(4000)  # give payloads time to run
        finally:
            browser.close()

@app.get("/report")
def report():
    """
    Players call: /report?path=/  (or a specific path) to trigger an admin visit.
    The bot carries the FLAG cookie, which is readable by JS (no HttpOnly).
    """
    path = request.args.get("path", "/")
    try:
        admin_visit(path)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    return jsonify({"ok": True, "msg": "Admin will/has visited the page."})

@app.get("/x")
def collector():
    """
    A blind exfil endpoint for the ADMIN browser to hit (same-origin).
    Players won't see this output, but it's useful for operators to verify.
    Real players should exfiltrate to their own server.
    """
    q = dict(request.args)
    logline = {"time": datetime.utcnow().isoformat()+"Z", "data": q, "ua": request.headers.get("User-Agent","")}
    EXFIL_LOG.append(logline)
    print("[EXFIL]", logline, flush=True)
    return Response(status=204)

if __name__ == "__main__":
    # Dev server (use gunicorn in Docker)
    app.run(host="0.0.0.0", port=8888, debug=False)

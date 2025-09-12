import os
import time
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# --- Flag remains dynamic via GZCTF ---
FLAG = os.environ.get("GZCTF_FLAG", "flag{LOCAL_TEST_123}")

# --- Admin creds (PIN is now FIXED, not from env) ---
ADMIN_USER = "admin"
ADMIN_PIN = "042"  # <-- fixed 3-digit PIN; do not change from env
if not ADMIN_PIN.isdigit() or len(ADMIN_PIN) != 3:
    raise RuntimeError("ADMIN_PIN must be a 3-digit numeric string like '042'.")
ADMIN_HASH = hashlib.sha1(ADMIN_PIN.encode()).hexdigest()

# --- Toy / flawed rate-limit (MEDIUM) ---
ATTEMPTS = {}
MAX_ATTEMPTS_PER_MIN = 30
WINDOW_SECONDS = 60

def get_client_id(req):
    xff = req.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if xff:
        return f"xff:{xff}"
    return f"ip:{request.remote_addr}"

def allow_attempt(client_id):
    now = time.time()
    bucket = ATTEMPTS.setdefault(client_id, [])
    ATTEMPTS[client_id] = [t for t in bucket if now - t < WINDOW_SECONDS]
    if len(ATTEMPTS[client_id]) >= MAX_ATTEMPTS_PER_MIN:
        return False
    ATTEMPTS[client_id].append(now)
    return True

@app.route("/", methods=["GET"])
def home():
    if session.get("user") == ADMIN_USER:
        return redirect(url_for("flag"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    status = 200
    if request.method == "POST":
        client_id = get_client_id(request)
        if not allow_attempt(client_id):
            message = "Too many attempts. Please wait a moment."
            status = 429
        else:
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            time.sleep(0.04 + (hash(username + password) % 30) / 1000.0)

            h = hashlib.sha1(password.encode()).hexdigest()
            if username == ADMIN_USER and h == ADMIN_HASH:
                session["user"] = ADMIN_USER
                return redirect(url_for("flag"))
            else:
                message = "Wrong password for admin." if username == ADMIN_USER else "Account not found."
                status = 401

    resp = make_response(render_template("login.html", message=message))
    resp.headers["X-Auth-Hint"] = "admin uses a 3-digit numeric PIN"
    return resp, status

@app.route("/flag")
def flag():
    if session.get("user") != ADMIN_USER:
        abort(403)
    return render_template("flag.html", flag=FLAG)

@app.after_request
def security_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 6666)))

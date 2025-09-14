from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import send_from_directory
from config import SECRET_KEY, FLAG, LISTEN_HOST, LISTEN_PORT
from models import (
    init_db, create_user, get_user_by_username,
    verify_password, get_user_by_id, update_profile
)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Initialize DB once when the app starts (Flask 3.x safe)
with app.app_context():
    init_db()

# --- Subtle, user-discoverable hints ---
@app.route("/robots.txt")
def robots():
    # Base64 of "attacker@evil.test" → YXR0YWNrZXJAZXZpbC50ZXN0
    body = (
        "User-agent: *\n"
        "Disallow:\n"
        "# challenge: your profile must reflect our QA contact.\n"
        "# hint: Explore qa-contact-b64 and set your profile email to that address, then revisit your profile page.\n"
        "# qa-contact-b64: YXR0YWNrZXJAZXZpbC50ZXN0\n"
    )
    return body, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/poc/download")
def poc_download():
    return send_from_directory("static", "poc_attack.html", as_attachment=True, download_name="attack.html")


@app.after_request
def add_small_hint(resp):
    # Very small nudge visible in DevTools -> Network -> Headers
    resp.headers["X-Ops-Domain"] = "evil.test"
    return resp
# --------------------------------------

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "uid" not in session:
            flash("Please log in.")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    uid = session.get("uid")
    user = get_user_by_id(uid) if uid else None
    return render_template("index.html", user=user)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Username and password required.")
            return redirect(url_for("register"))
        try:
            create_user(username, password)
            flash("Registered. Please log in.")
            return redirect(url_for("login"))
        except Exception:
            flash("Username already taken.")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = get_user_by_username(username)
        if user and verify_password(user, password):
            session["uid"] = user["id"]
            flash("Logged in.")
            return redirect(url_for("profile"))
        flash("Invalid credentials.")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    user = get_user_by_id(session["uid"])
    show_flag = user["email"] == "attacker@evil.test"
    return render_template("profile.html", user=user, show_flag=show_flag, flag=FLAG)

# Vulnerable update endpoint (gameplay logic unchanged)
@app.route("/profile/update", methods=["POST"])
@login_required
def profile_update():
    email = request.form.get("email", "")
    display_name = request.form.get("display_name", "")
    update_profile(session["uid"], email=email, display_name=display_name)
    flash("Profile updated.")
    return redirect(url_for("profile"))

if __name__ == "__main__":
    app.run(host=LISTEN_HOST, port=LISTEN_PORT, debug=False)

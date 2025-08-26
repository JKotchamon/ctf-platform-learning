from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from pathlib import Path
from check_flag import verify_flag
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

ROOT = Path(__file__).resolve().parents[1]
CHAL_DIR = ROOT / "challenge"
EXECUTE_TO_VERIFY = os.environ.get("EXECUTE_TO_VERIFY", "false").lower() == "true"

@app.get("/")
def home():
    has_bin = (CHAL_DIR / "baby-re-1").exists()
    return render_template("index.html", has_bin=has_bin, also_exec=EXECUTE_TO_VERIFY)

@app.post("/submit")
def submit():
    flag = (request.form.get("flag") or "").strip()
    ok, reason = verify_flag(flag, EXECUTE_TO_VERIFY)
    flash("Correct! Nice work." if ok else f"Not yet. {reason}", "success" if ok else "error")
    return redirect(url_for("home"))

@app.get("/download/baby-re-1")
def download():
    return send_from_directory(CHAL_DIR, "baby-re-1", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

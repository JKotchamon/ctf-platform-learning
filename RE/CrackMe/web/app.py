from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import subprocess, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only")

CHECKER_PATH = "/app/checker/checker"

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/download")
def download():
    return send_file(CHECKER_PATH, as_attachment=True, download_name="aes_crackme")

@app.post("/submit")
def submit():
    flag = request.form.get("flag", "")
    try:
        p = subprocess.run(
            [CHECKER_PATH],
            input=(flag + "\n").encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        ok = b"Correct!" in p.stdout
        msg = p.stdout.decode(errors="ignore").strip()
        flash(msg, "success" if ok else "error")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

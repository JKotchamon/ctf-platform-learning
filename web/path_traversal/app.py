from flask import Flask, request, render_template, send_file, abort
import os

app = Flask(__name__)

# Get dynamic flag from environment
FLAG = os.environ.get("GZCTF_FLAG", "CTF{DUMMY_FLAG}")

# Save flag into hidden file
with open("/flag.txt", "w") as f:
    f.write(FLAG)

BASE_DIR = "/app/files"  # safe directory

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view")
def view_file():
    filename = request.args.get("file", "")
    target_path = os.path.join(BASE_DIR, filename)

    # 🔴 vulnerable: no proper sanitization
    try:
        return send_file(target_path)
    except Exception:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

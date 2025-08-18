from flask import Flask, render_template, send_file, make_response, request, jsonify
import os, hashlib

app = Flask(__name__)
BASE = os.path.join(os.path.dirname(__file__), "challenge")
CHALLENGE_PATH = os.path.join(BASE, "weird.txt")
FLAG_PATH = os.path.join(BASE, "flag.txt")
HASH_PATH = os.path.join(BASE, "hash.txt")

def read_text(p):
    try:
        with open(p, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

@app.after_request
def add_headers(resp):
    resp.headers["X-Encodings"] = "4-layers"
    resp.headers["X-Hint"] = "Onion layers. CyberChef helps."
    return resp

@app.route("/")
def index():
    pub_hash = read_text(HASH_PATH)
    return render_template("index.html", pub_hash=pub_hash)

@app.route("/download")
def download():
    return send_file(CHALLENGE_PATH, as_attachment=True, download_name="weird.txt")

@app.route("/robots.txt")
def robots():
    resp = make_response("User-agent: *\nDisallow:\n# Hint: Hex→Morse→ROT13→Base32")
    resp.mimetype = "text/plain"
    return resp

# Optional: simple verifier (POST JSON: {"flag":"CTF{...}"})
@app.route("/verify", methods=["POST"])
def verify():
    submitted = request.json.get("flag","")
    real = read_text(FLAG_PATH)
    ok = (submitted == real)
    return jsonify({"correct": ok})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

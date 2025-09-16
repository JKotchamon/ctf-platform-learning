from flask import Flask, request, render_template, Response
import requests
import os
import threading
from flask import Flask as InternalApp

app = Flask(__name__)

# Internal service hosting the flag
internal = InternalApp(__name__)

@internal.route("/secret")
def secret():
    return os.environ.get("GZCTF_FLAG", "flag{dummy_for_local}")

def run_internal():
    internal.run(host="127.0.0.1", port=5000, debug=False)

threading.Thread(target=run_internal, daemon=True).start()

# Basic filter (players must bypass it)
BLOCKLIST = ["127.0.0.1", "localhost", "169.254.169.254"]

@app.route("/", methods=["GET"])
def index():
    url = request.args.get("url")
    if url:
        for bad in BLOCKLIST:
            if bad in url:
                # Error Leak: intentionally disclose port info
                return "Error: Access to 127.0.0.1:5000 blocked by admin policy"
        try:
            r = requests.get(url, timeout=3)
            ctype = r.headers.get("content-type", "")
            if "image" in ctype:
                return f"<h3>Fetched Image:</h3><img src='{url}' style='max-width:400px;'>"
            else:
                return f"<h3>Fetched Response:</h3><pre>{r.text[:1000]}</pre>"
        except Exception as e:
            return f"Error fetching URL: {str(e)}"
    return render_template("index.html")

# Robots.txt to hint the path
@app.route("/robots.txt")
def robots():
    content = "User-agent: *\nDisallow: /secret\n"
    return Response(content, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)

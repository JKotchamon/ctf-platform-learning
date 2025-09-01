import os, base64
from flask import Flask, Response

app = Flask(__name__)

@app.get("/")
def index():
    flag = os.environ.get("GZCTF_FLAG", "flag{example}")
    b64 = base64.b64encode(flag.encode()).decode()
    html = f"""
    <h1>Decode Me</h1>
    <p>Decode this Base64 to get the flag:</p>
    <pre style="font-size:1.1rem">{b64}</pre>
    """
    return Response(html, mimetype="text/html")

@app.get("/health")
def health():
    return "ok"

if __name__ == "__main__":
    # GZ::CTF will map this internal port automatically; just listen on 0.0.0.0
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))

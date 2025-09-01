from flask import Flask, render_template_string

app = Flask(__name__, static_folder="static")

BASE = """
<!doctype html><html><head><meta charset="utf-8"><title>QR Challenge</title>
<style>
body{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;background:#0b1020;color:#e7eaf6;margin:0}
main{max-width:900px;margin:0 auto;padding:24px}
.card{background:#111735;border:1px solid #26304f;border-radius:14px;padding:16px;margin:16px 0}
a{color:#8bd0ff;text-decoration:none}
code,pre{background:#0b1020;border:1px solid #26304f;border-radius:8px;padding:10px}
</style></head><body><main>{{ body|safe }}</main></body></html>
"""

@app.get("/")
def index():
    body = """
    <div class="card">
      <h2>QR Challenge</h2>
      <p>Scan the QR to get a Base64 string. Decode it to reveal the flag.</p>
      <p><img src="/static/qr.png" alt="QR" style="max-width:280px;border-radius:12px;border:1px solid #26304f"></p>
      <p>You can also download the exact QR content: <a href="/static/payload.txt" download>payload.txt</a></p>
    </div>
    """
    return render_template_string(BASE, body=body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

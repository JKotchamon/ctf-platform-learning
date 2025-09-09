from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = os.getenv("FLAG", "CHALL{dev-flag}")

# Base email preview template
BASE_TEMPLATE = """
<!doctype html>
<html>
<head><title>Jinja Mailer</title></head>
<body>
  <h2>Email Preview</h2>
  <p>{{ content }}</p>
  <hr/>
  <small>-- Jinja Mailer Service</small>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content", "")
        # ❌ VULNERABLE: directly embedding attacker input into a Jinja template
        preview = BASE_TEMPLATE.replace("{{ content }}", content)
        return render_template_string(preview)
    return """
      <h2>Compose Email</h2>
      <form method="post">
        <textarea name="content" rows="5" cols="60"
          placeholder="Dear {{ user.name }}, ..."></textarea><br/>
        <button type="submit">Preview</button>
      </form>
    """

@app.route("/flag")
def flag():
    # Flag is only accessible if attacker achieves RCE and reads env
    return "Access denied"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

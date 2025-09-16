from flask import Flask, request, render_template_string, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "super_secret"

# Read flag from GZCTF environment variable
FLAG = os.getenv("GZCTF_FLAG", "CTF{DUMMY_FLAG}")

# Simulated database
users = {
    "alice": {"password": "alicepass", "id": "1001", "report": "Alice’s grades: A, B, C"},
    "bob": {"password": "bobpass", "id": "1002", "report": "Bob’s grades: B, C, D"},
    "admin": {"password": "adminpass", "id": "9999", "report": f"Admin secret report: {FLAG}"}
}

# ---------- HTML Templates ----------
login_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Student Portal</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
    .container { max-width: 400px; margin: auto; padding: 20px; background: white; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);}
    h2 { text-align: center; color: #333; }
    .info { font-size: 0.9em; color: #777; margin-bottom: 15px; }
    input, button { width: 100%; padding: 10px; margin: 6px 0; border-radius: 6px; border: 1px solid #ccc; }
    button { background: #007bff; color: white; border: none; }
    button:hover { background: #0056b3; }
  </style>
</head>
<body>
  <div class="container">
    <h2>🎓 Student Portal Login</h2>
    <p class="info">Test accounts:<br>
       Username: <b>alice</b> / Password: <b>alicepass</b><br>
       Username: <b>bob</b> / Password: <b>bobpass</b><br>
    </p>
    <form method="POST">
      <input name="username" placeholder="Username" required><br>
      <input type="password" name="password" placeholder="Password" required><br>
      <button type="submit">Login</button>
    </form>
  </div>
</body>
</html>
"""

dashboard_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; background: #eef2f3; }
    .container { max-width: 500px; margin: auto; padding: 20px; background: white; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);}
    h3 { color: #333; }
    a { display: inline-block; margin-top: 10px; padding: 8px 14px; background: #007bff; color: white; text-decoration: none; border-radius: 6px; }
    a:hover { background: #0056b3; }
  </style>
</head>
<body>
  <div class="container">
    <h3>Welcome, {{user}}</h3>
    <p>Your student ID is <b>{{uid}}</b></p>
    <a href='/report?id={{uid}}'>📄 View your report</a>
  </div>
</body>
</html>
"""

report_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; background: #fdfdfd; }
    .container { max-width: 600px; margin: auto; padding: 20px; background: white; border-radius: 12px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);}
    h2 { color: #333; }
    p { font-size: 1.1em; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Report for {{user}}</h2>
    <p>{{report}}</p>
  </div>
</body>
</html>
"""

# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user in users and users[user]["password"] == pwd:
            session["user"] = user
            return redirect(url_for("dashboard"))
        return "Invalid credentials"
    return render_template_string(login_page)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    uid = users[user]["id"]
    return render_template_string(dashboard_page, user=user, uid=uid)

@app.route("/report")
def report():
    if "user" not in session:
        return redirect(url_for("login"))
    rid = request.args.get("id")
    for u, data in users.items():
        if data["id"] == rid:
            return render_template_string(report_page, user=u, report=data["report"])
    return "Report not found. Valid IDs are between 1000 and 9999."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

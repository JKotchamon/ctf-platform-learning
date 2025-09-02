from flask import Flask, request, render_template_string, send_from_directory
import sqlite3, os

app = Flask(__name__)
DB_PATH = "/data/app.db"

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

# Load HTML once from file
with open("index.html", "r", encoding="utf-8") as f:
    INDEX_HTML = f.read()

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML, msg=None, success=None)

@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username","")
    p = request.form.get("password","")
    q = f"SELECT username, password FROM users WHERE username = '{u}' AND password = '{p}' LIMIT 1"
    con = get_db()
    try:
        row = con.execute(q).fetchone()
    finally:
        con.close()
    if row:
        if row["username"] == "admin":
            return f"Welcome admin! Your password is the flag: {row['password']}"
        return f"Welcome {row['username']}! But only admin sees the flag."
    return render_template_string(INDEX_HTML, msg="Invalid credentials", success=None)

@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css", mimetype="text/css")

from flask import Flask, request, render_template
import sqlite3, os

app = Flask(__name__)
DB_PATH = "/data/app.db"

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", msg=None)

@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username","")
    p = request.form.get("password","")
    # VULNERABLE: string interpolation -> SQL Injection
    q = f"SELECT username, password FROM users WHERE username = '{u}' AND password = '{p}' LIMIT 1"
    con = get_db()
    try:
        row = con.execute(q).fetchone()
    finally:
        con.close()
    if row:
        # If first row is admin, prints the flag (admin’s password IS the flag)
        if row["username"] == "admin":
            return f"Welcome admin! Your password is the flag: {row['password']}"
        return f"Welcome {row['username']}! But only admin sees the flag."
    return render_template("index.html", msg="Invalid credentials")

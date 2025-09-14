import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
from config import SQLITE_PATH

@contextmanager
def db():
    con = sqlite3.connect(SQLITE_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()

def init_db():
    with db() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT DEFAULT '',
            display_name TEXT DEFAULT ''
        );
        """)
        # Optional: seed a demo user (non-admin; admin not required for this challenge)
        try:
            con.execute(
                "INSERT INTO users (username, password_hash, email, display_name) VALUES (?,?,?,?)",
                ("demo", generate_password_hash("demo123"), "demo@example.com", "Demo User")
            )
        except sqlite3.IntegrityError:
            pass

def create_user(username, password):
    with db() as con:
        con.execute(
            "INSERT INTO users (username, password_hash) VALUES (?,?)",
            (username, generate_password_hash(password))
        )

def get_user_by_username(username):
    with db() as con:
        cur = con.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

def get_user_by_id(uid):
    with db() as con:
        cur = con.execute("SELECT * FROM users WHERE id = ?", (uid,))
        return cur.fetchone()

def verify_password(user_row, password):
    return check_password_hash(user_row["password_hash"], password)

def update_profile(uid, email=None, display_name=None):
    with db() as con:
        if email is not None and display_name is not None:
            con.execute("UPDATE users SET email = ?, display_name = ? WHERE id = ?",
                        (email, display_name, uid))
        elif email is not None:
            con.execute("UPDATE users SET email = ? WHERE id = ?", (email, uid))
        elif display_name is not None:
            con.execute("UPDATE users SET display_name = ? WHERE id = ?", (display_name, uid))

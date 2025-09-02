import os
import sqlite3

def init_db():
    # Ensure /data directory exists (absolute path)
    os.makedirs("/data", exist_ok=True)
    db_path = "/data/app.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Reset users table
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (username TEXT, password TEXT)")

    # Admin password = dynamic flag (provided by GZ::CTF), fallback if not set
    flag = os.environ.get("GZCTF_FLAG", "CTF{default_flag}")
    cur.execute("INSERT INTO users VALUES (?, ?)", ("admin", flag))
    cur.execute("INSERT INTO users VALUES (?, ?)", ("guest", "guest"))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

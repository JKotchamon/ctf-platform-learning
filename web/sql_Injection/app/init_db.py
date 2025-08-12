import os, sqlite3

FLAG = os.environ.get("FLAG", "HTB{dummy_flag}")
DB_PATH = "/data/app.db"

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS users")
cur.execute("CREATE TABLE users(username TEXT, password TEXT)")
# admin password is the flag
cur.execute("INSERT INTO users VALUES('admin', ?)", (FLAG,))
cur.execute("INSERT INTO users VALUES('guest', 'guest')")
con.commit()
con.close()
print("DB initialized at", DB_PATH)

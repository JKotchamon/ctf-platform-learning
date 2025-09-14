# Static config (no env vars) to satisfy "permanent flag" requirement.
SECRET_KEY = "please_change_this_in_real_ctf_but_static_for_challenge"
FLAG = "CTF{CSRF_STATE_CHANING}"  # <-- exact spelling per request
SQLITE_PATH = "db.sqlite3"
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8000  # container internal port

import os
from urllib.parse import urlparse, urljoin
from flask import Flask, request, redirect, render_template, make_response, abort

app = Flask(__name__)

# Dynamic flag for GZ::CTF
FLAG = os.environ.get("GZCTF_FLAG", "flag{LOCAL_TEST_ONLY}")
PORT = int(os.environ.get("PORT", 6666))

# Challenge config (intentionally naive)
# The app *intends* to only redirect to this partner domain, but does a flawed check.
WHITELIST_PREFIX = "https://safe.example.com"

@app.after_request
def add_headers(resp):
    # Helpful for participants inspecting responses
    resp.headers["X-Challenge"] = "Open-Redirect-GZCTF"
    resp.headers["X-Hint"] = "check next= and how it's validated"
    return resp

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/promo")
def promo():
    """
    Pretend "partner promo" endpoint:
    - Takes ?next= and "validates" it with a naive startswith
    - If it "passes", it appends ?code=<FLAG> and redirects the user there
    - Otherwise, falls back to homepage
    Bypass this to leak the flag to your controlled domain.
    """
    next_url = request.args.get("next", "").strip()

    # --- Intentionally flawed validation ---
    # 1) Using startswith() on the string allows domains like:
    #    https://safe.example.com.evil.tld/...
    # 2) Also accepts scheme-relative URLs: //evil.tld/...
    if next_url.startswith(WHITELIST_PREFIX):
        # If "validated", append code=<FLAG> (the bounty code 😈)
        sep = "&" if "?" in next_url else "?"
        return redirect(f"{next_url}{sep}code={FLAG}", code=302)

    # Try another flawed idea: "join" relative URLs to our host—but still allow schemeless
    # NOTE: urljoin("https://our.app", "//evil.tld") => "https://evil.tld"
    # This makes it even more bypassable if someone provides //evil.tld
    if next_url.startswith("/") or next_url.startswith("//"):
        joined = urljoin(request.host_url, next_url)
        if joined.startswith(WHITELIST_PREFIX):
            sep = "&" if "?" in joined else "?"
            return redirect(f"{joined}{sep}code={FLAG}", code=302)

    # Fallback
    return redirect("/", code=302)

@app.route("/reward")
def reward():
    """
    A decoy page claiming you need to visit our partner link.
    Provides a small hint in the HTML encouraging users to inspect.
    """
    resp = make_response(render_template("promo.html"))
    # Subtle: set a cookie—pure fluff for realism; not needed to solve
    resp.set_cookie("promo_user", "guest", httponly=True, samesite="Lax")
    return resp

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    # Bind to 0.0.0.0 for Docker and use port 6666 by default
    app.run(host="0.0.0.0", port=PORT, debug=False)

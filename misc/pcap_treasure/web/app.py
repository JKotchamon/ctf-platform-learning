import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from .flags import check_flag  # package-relative import (because we're in web/):contentReference[oaicite:9]{index=9}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

PCAP_DIR = os.environ.get("PCAP_DIR", "/app/challenge")
PCAP_NAME = os.environ.get("PCAP_NAME", "sample.pcap")

CHALLENGE_CARD = {
    "title": "PCAP Treasure Hunt",
    "filetype": ".pcap",
    "trick": "Extra data hidden in the padding bytes of packets (or DNS TXT records).",
    "why_fun": "Practice Wireshark filtering and packet inspection.",
    "difficulty": "Hard — requires exploring network layers carefully."
}

@app.get("/")
def index():
    return render_template("index.html", card=CHALLENGE_CARD, pcap_name=PCAP_NAME)

@app.get("/download")
def download():
    return send_from_directory(PCAP_DIR, PCAP_NAME, as_attachment=True)

@app.post("/submit")
def submit():
    flag = (request.form.get("flag") or "").strip()
    if check_flag(flag):
        flash("Correct! You found the flag.", "success")
    else:
        flash("Nope. Keep digging in that PCAP.", "error")
    return redirect(url_for("index"))

import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

PCAP_DIR = os.environ.get("PCAP_DIR", "/app/challenge")
PCAP_NAME = os.environ.get("PCAP_NAME", "sample.pcap")

CHALLENGE_CARD = {
    "title": "PCAP Treasure Hunt",
    "filetype": ".pcap",
    "trick": "Extra data hidden in the padding bytes of packets.",
    "why_fun": "Practice Wireshark filtering and packet inspection.",
    "difficulty": "Easy — requires exploring network layers carefully."
}

@app.get("/")
def index():
    return render_template("index.html", card=CHALLENGE_CARD, pcap_name=PCAP_NAME)

@app.get("/download")
def download():
    return send_from_directory(PCAP_DIR, PCAP_NAME, as_attachment=True)

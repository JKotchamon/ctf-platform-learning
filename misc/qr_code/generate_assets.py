# generate_assets.py
import os, base64
from pathlib import Path
import qrcode

OUT = Path("static")
OUT.mkdir(exist_ok=True)

flag = os.getenv("FLAG_QR", "CTF{Mike_QR_Code}")

# Create the challenge payload (Base64 of the flag)
payload = base64.b64encode(flag.encode()).decode()

# Save for direct download (neutral name)
(OUT / "payload.txt").write_text(payload, encoding="utf-8")

# QR contains the same payload
img = qrcode.make(payload)
img.save(OUT / "qr.png")

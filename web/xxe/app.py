from flask import Flask, request, render_template
from lxml import etree
import os

app = Flask(__name__)

# Dynamic flag injection (from GZ::CTF)
FLAG = os.environ.get("GZCTF_FLAG", "flag{DUMMY_LOCAL_FLAG}")

# Save flag into file for XXE exfiltration
with open("/flag.txt", "w") as f:
    f.write(FLAG)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        xml_data = request.form["xml"]

        # ❌ Vulnerable XML parser (intentional for CTF)
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        doc = etree.fromstring(xml_data.encode(), parser)

        name = doc.findtext("name", default="(missing)")
        email = doc.findtext("email", default="(missing)")

        return render_template("index.html", result={"name": name, "email": email})

    except Exception as e:
        return render_template("index.html", error=str(e), result=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

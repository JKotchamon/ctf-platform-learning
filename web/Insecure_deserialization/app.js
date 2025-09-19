const express = require("express");
const bodyParser = require("body-parser");
const serialize = require("node-serialize");

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

// ✅ Load dynamic flag from env
const FLAG = process.env.GZCTF_FLAG || "CTF{LOCAL_TEST_FLAG}";

app.get("/", (req, res) => {
  res.send(`
    <h2>Welcome to Profile Restore Service</h2>
    <p>Upload your profile to restore your session.</p>
    <form action="/upload" method="POST">
      <textarea name="data" rows="5" cols="60"></textarea><br>
      <button type="submit">Upload</button>
    </form>
    <p><b>Hint:</b> Profiles are Base64 encoded serialized objects.<br>
    Can you restore the <code>admin</code> profile?</p>
  `);
});

app.post("/upload", (req, res) => {
  try {
    const data = req.body.data || "";
    const raw = Buffer.from(data, "base64").toString();
    const obj = serialize.unserialize(raw); // 🚨 Insecure Deserialization

    if (obj && obj.username === "admin") {
      res.send(`<p>Welcome back, admin! Here is your flag: ${FLAG}</p>`);
    } else {
      res.send(`<p>Restored profile: ${JSON.stringify(obj)}</p>`);
    }
  } catch (err) {
    res.send(`<p>Error: ${err}</p>`);
  }
});

app.listen(5000, () => {
  console.log("Server running on http://0.0.0.0:5000");
});

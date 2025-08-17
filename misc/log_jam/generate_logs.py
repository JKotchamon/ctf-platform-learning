# log-jam/generate_logs.py
import base64, os, random, string, time, uuid
from datetime import datetime, timedelta

OUT_DIR = "/app/logs"

# >>> Set your real flag here <<<
FLAG = "CTF{log_mastery_rocks}"

# Encode & split into parts (tune PARTS for difficulty)
PARTS = 6
b64 = base64.b64encode(FLAG.encode()).decode()
part_size = (len(b64) + PARTS - 1) // PARTS
frags = [b64[i:i+part_size] for i in range(0, len(b64), part_size)]
if len(frags) < PARTS:
    # pad with empty strings to hit PARTS count
    frags += [""] * (PARTS - len(frags))

# Files we’ll populate
FILES = [
    "access.log", "auth.log", "app.log",
    "syslog.log", "events.log", "cron.log"
]

# Noise helpers
ips = [f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
       for _ in range(200)]
agents = ["curl/7.88.1","Mozilla/5.0","Googlebot/2.1","+http://www.google.com/bot.html",
          "python-requests/2.31.0","Wget/1.21.2"]
paths  = ["/", "/login", "/api/v1/ping", "/admin", "/robots.txt", "/healthz"]
levels = ["INFO","WARN","DEBUG","ERROR","NOTICE","CRITICAL"]

def ts(i=0):
    # Spread timestamps over last hour for realism
    t = datetime.utcnow() - timedelta(minutes=random.randint(0,59), seconds=random.randint(0,59))
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def randstr(n=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def write_noise_line(fh, fname):
    typ = random.choice(["http","auth","sys","app"])
    if typ == "http":
        line = f'{random.choice(ips)} - - [{datetime.utcnow():%d/%b/%Y:%H:%M:%S +0000}] "GET {random.choice(paths)} HTTP/1.1" {random.choice([200,200,200,301,302,403,404,500])} {random.randint(20,5000)} "-" "{random.choice(agents)}"'
    elif typ == "auth":
        line = f'{ts()} {fname} sshd[{random.randint(1000,5000)}]: Failed password for invalid user {randstr(5)} from {random.choice(ips)} port {random.randint(1000,65000)} ssh2'
    elif typ == "sys":
        line = f'{ts()} kernel: [{random.uniform(10.0,9999.9):.3f}] CPU{random.randint(0,7)}: {random.choice(["soft lockup","process hung","NET: packet drop","audit: denied"])}'
    else:
        line = f'{ts()} app[{random.randint(100,999)}] {random.choice(levels)} trace_id={uuid.uuid4()} msg="{random.choice(["task done","retrying","cache miss","db timeout","rate limited"])}"'
    fh.write(line + "\n")

def embed_fragment(fh, idx, total, data):
    # Legit fragments: label "part-<n>/<total> data=<base64>"
    # Decoys will look similar but won’t match our grep/sed rule cleanly.
    line = (f'{ts()} collector[{random.randint(1000,9999)}]:'
            f' correlate id={uuid.uuid4()} part-{idx}/{total} data={data} status=ok')
    fh.write(line + "\n")

def write_decoy(fh):
    # Lookalike noise: wrong label order, unicode, or broken token
    styles = [
        lambda: f'{ts()} collector: data-part {randstr(3)}:{randstr(8)}',
        lambda: f'{ts()} correlate id={uuid.uuid4()} PART {random.randint(1,9)} of {random.randint(2,9)} dat={randstr(10)}',
        lambda: f'{ts()} collector[{random.randint(1000,9999)}]: part={randstr(2)} data="{randstr(16)}"'
    ]
    fh.write(styles[random.randint(0,len(styles)-1)]() + "\n")

def make_file(path, legit_frag=None):
    with open(path, "w", encoding="utf-8") as fh:
        # Total lines per file (tune for difficulty/size)
        total = random.randint(3000, 6000)
        legit_drop_line = random.randint(500, total-500) if legit_frag else None

        for i in range(1, total+1):
            if legit_frag and i == legit_drop_line:
                idx, tot, data = legit_frag
                embed_fragment(fh, idx, tot, data)
            elif random.random() < 0.02:
                write_decoy(fh)
            else:
                write_noise_line(fh, os.path.basename(path))

# Assign each real fragment to a different file randomly
random.seed(42)
targets = random.sample(FILES, k=min(PARTS, len(FILES)))

os.makedirs(OUT_DIR, exist_ok=True)

# Create files; put exactly one legit fragment into PARTS of them
placed = 0
for fname in FILES:
    fpath = os.path.join(OUT_DIR, fname)
    if placed < PARTS and fname in targets:
        make_file(fpath, legit_frag=(placed+1, PARTS, frags[placed]))
        placed += 1
    else:
        make_file(fpath, legit_frag=None)

# Small extra hint (not too explicit)
with open(os.path.join(OUT_DIR, "README_hint.txt"), "w") as fh:
    fh.write(
        "Hint: hunt lines containing 'part-<n>/<N> data=<...>' across files.\n"
        "Order by the numeric <n>, concatenate the base64 fragments, then base64 decode.\n"
    )

print(f"[*] Generated logs in {OUT_DIR} with {PARTS} legit fragments.")

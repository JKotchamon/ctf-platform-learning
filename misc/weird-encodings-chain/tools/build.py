#!/usr/bin/env python3
import base64, codecs, binascii, os, sys, hashlib, textwrap

MORSE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.'
}

def to_morse(s: str) -> str:
    return " / ".join(MORSE[ch] for ch in s)

def main():
    if len(sys.argv) != 2:
        print("Usage: build.py 'CTF{flag}'", file=sys.stderr)
        sys.exit(1)
    flag = sys.argv[1]

    # Base32 → ROT13 → Morse
    b32  = base64.b32encode(flag.encode()).decode()
    r13  = codecs.decode(b32, "rot_13")
    morse = to_morse(r13).encode()

    # === Spaced hex output ===
    # Optional: wrap every N bytes per line for readability (default 32)
    wrap_bytes = int(os.getenv("HEX_BYTES_PER_LINE", "32"))
    chunks = [morse[i:i+wrap_bytes] for i in range(0, len(morse), wrap_bytes)]
    lines = [" ".join(f"{b:02x}" for b in chunk) for chunk in chunks]
    hexd_spaced = "\n".join(lines)

    base = os.path.join(os.path.dirname(__file__), "..", "app", "challenge")
    os.makedirs(base, exist_ok=True)
    with open(os.path.join(base, "weird.txt"), "w", encoding="utf-8") as f:
        f.write(hexd_spaced + "\n")

    # Hash for scoreboard
    h = hashlib.sha256(flag.encode()).hexdigest()
    with open(os.path.join(base, "hash.txt"), "w", encoding="utf-8") as f:
        f.write(h + "\n")

    # Persist flag if missing
    fp = os.path.join(base, "flag.txt")
    if not os.path.exists(fp):
        with open(fp, "w", encoding="utf-8") as f:
            f.write(flag)

    print("OK: wrote spaced-hex weird.txt and hash.txt")

if __name__ == "__main__":
    main()

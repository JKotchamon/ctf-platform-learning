#!/usr/bin/env python3

import base64, codecs, binascii, os, hashlib, textwrap

# --- Permanent flag ---
FLAG = "CTF{onion_layers_are_fun}"

MORSE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.'
}

def to_morse(s: str) -> str:
    return " / ".join(MORSE[ch] for ch in s)

def main():
    # ../app/challenge relative to this file
    base = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "app", "challenge"))
    os.makedirs(base, exist_ok=True)

    flag = FLAG

    # flag -> Base32 (no '=') -> ROT13 -> Morse -> hex
    b32 = base64.b32encode(flag.encode()).decode().rstrip("=")
    rot13_text = codecs.encode(b32, "rot_13").upper()
    morse = to_morse(rot13_text)
    hexb = binascii.hexlify(morse.encode()).decode()

    # pretty: pairs with spaces, wrapped lines
    pairs = [hexb[i:i+2] for i in range(0, len(hexb), 2)]
    spaced = " ".join(pairs)
    wrapped = "\n".join(textwrap.wrap(spaced, width=32*3))

    # weird.txt
    with open(os.path.join(base, "weird.txt"), "w", encoding="utf-8") as f:
        f.write(wrapped + "\n")

    # hash.txt
    h = hashlib.sha256(flag.encode()).hexdigest()
    with open(os.path.join(base, "hash.txt"), "w", encoding="utf-8") as f:
        f.write(h + "\n")

    # flag.txt (always overwrite to enforce permanence)
    with open(os.path.join(base, "flag.txt"), "w", encoding="utf-8") as f:
        f.write(flag)

    print("OK: wrote weird.txt, hash.txt, and flag.txt with permanent static flag.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import base64, codecs, binascii, sys, re

REV_MORSE = {
    '.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G','....':'H','..':'I','.---':'J',
    '-.-':'K','.-..':'L','--':'M','-.':'N','---':'O','.--':'P','--.-':'Q','.-.':'R','...':'S','-':'T',
    '..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z',
    '-----':'0','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6','--...':'7','---..':'8','----.':'9'
}

def main(path):
    with open(path, "r", encoding="utf-8") as f:
        hexd = f.read()

    # Accept 'aa bb\ncc' or 'aabbcc'
    hexd = re.sub(r'[^0-9a-fA-F]', '', hexd)
    morse = binascii.unhexlify(hexd).decode()

    # Accept " / " or plain spaces between tokens
    tokens = [t for t in re.split(r'(?:\s*/\s*|\s+)', morse) if t]

    rot13_text = "".join(REV_MORSE[t] for t in tokens)
    b32 = codecs.decode(rot13_text, "rot_13")
    flag = base64.b32decode(b32.encode()).decode()
    print(flag)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../app/challenge/weird.txt")
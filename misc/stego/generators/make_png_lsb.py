#!/usr/bin/env python3
import argparse, struct
from PIL import Image

MAGIC = b'STEG1'  # 5 bytes

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--flag', required=True)
args = parser.parse_args()

secret = args.flag.encode('utf-8')
header = MAGIC + struct.pack('>I', len(secret))
payload = header + secret

# Create cover image deterministically (no external assets)
W, H = 512, 512
img = Image.new('RGB', (W, H))
for y in range(H):
    for x in range(W):
        r = (x * 255) // (W - 1)
        g = (y * 255) // (H - 1)
        b = ((x ^ y) & 0xFF)
        img.putpixel((x, y), (r, g, b))

# Embed bits in R channel LSB
pixels = img.load()
capacity_bits = W * H  # 1 bit per pixel (R channel only)
needed_bits = len(payload) * 8
if needed_bits > capacity_bits:
    raise SystemExit(f"Not enough capacity: need {needed_bits} bits, have {capacity_bits}")

bit_idx = 0
for y in range(H):
    for x in range(W):
        if bit_idx >= needed_bits:
            break
        r, g, b = pixels[x, y]
        byte = payload[bit_idx // 8]
        bit = (byte >> (7 - (bit_idx % 8))) & 1
        r = (r & 0xFE) | bit
        pixels[x, y] = (r, g, b)
        bit_idx += 1
    if bit_idx >= needed_bits:
        break

img.save(args.out, optimize=True)
print(f"Wrote {args.out} with {needed_bits} embedded bits")
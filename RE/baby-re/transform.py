flag = "CTF{babyre_xor_123}"  # change me
target = [((ord(ch) ^ 0x37) - 3) & 0xFF for ch in flag]
print(','.join(f'0x{b:02X}' for b in target))
 # -> CTF{babyre_xor_123}
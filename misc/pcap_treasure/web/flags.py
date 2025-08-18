import os
FLAG = os.environ.get("FLAG", "CTF{example_flag_change_me}")

def check_flag(s: str) -> bool:
    return s == FLAG

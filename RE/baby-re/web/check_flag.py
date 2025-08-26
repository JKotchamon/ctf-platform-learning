import subprocess
from pathlib import Path
import shlex

# ----- Stage 1: pure-python check -----
# same transform your C uses:  ((ch ^ 0x37) - 3)  -> bytes must match target
TARGET = [
    0x71,0x60,0x6E,0x49,0x52,0x53,0x52,0x4B,0x42,0x4F,0x65,0x4C,0x55,0x42,0x65,0x03,0x02,0x01,0x47
]

def python_check(s: str) -> bool:
    if len(s) != len(TARGET):
        return False
    try:
        for i, ch in enumerate(s):
            t = ((ord(ch) ^ 0x37) - 3) & 0xFF
            if t != TARGET[i]:
                return False
        return True
    except Exception:
        return False

# ----- Stage 2 (optional): execute the ELF to double-check -----
def exec_check(s: str) -> tuple[bool, str]:
    bin_path = Path(__file__).resolve().parents[1] / "challenge" / "baby-re-1"
    if not bin_path.exists():
        return False, "binary not found"
    try:
        proc = subprocess.run(
            [str(bin_path)],
            input=(s + "\n").encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=2.0
        )
        out = proc.stdout.decode(errors="ignore")
        # your C prints this on success:
        # puts("Correct! 🎉");
        return ("Correct!" in out), out.strip()
    except subprocess.TimeoutExpired:
        return False, "timed out"
    except Exception as e:
        return False, f"exec error: {e}"

def verify_flag(flag: str, also_exec: bool = False) -> tuple[bool, str]:
    if not python_check(flag):
        return False, "Python check failed"
    if not also_exec:
        return True, "ok"
    ok, reason = exec_check(flag)
    return (ok, "ok" if ok else f"ELF check failed: {reason}")

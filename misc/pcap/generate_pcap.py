# generate_pcap.py — static Base64 flag, exactly 5 DNS TXT transactions
import sys, base64
from pathlib import Path

# ----- STATIC SETTINGS (edit these in-code) -----
FLAG = "CTF{Only_Base64}"          # <- put your static flag here
NUM_TX = 5                         # number of DNS transactions (query+response pairs)
PCAP_DIR = Path("/app/challenge")  # output folder
PCAP_NAME = "sample.pcap"          # output file name
# -----------------------------------------------

PCAP_DIR.mkdir(parents=True, exist_ok=True)
PCAP_PATH = PCAP_DIR / PCAP_NAME


def _split_into_n(s: str, n: int):
    """Split string s into n near-equal pieces (no empty tails)."""
    if n <= 0: return [s]
    q, r = divmod(len(s), n)
    sizes = [(q + 1 if i < r else q) for i in range(n)]
    out, idx = [], 0
    for size in sizes:
        out.append(s[idx:idx+size])
        idx += size
    return out


def make_dns_txt_pcap_base64(flag_text: str, out: Path, n_tx: int):
    from scapy.all import Ether, IP, UDP, DNS, DNSQR, DNSRR, wrpcap

    # 1) Base64-encode the static flag
    b64 = base64.b64encode(flag_text.encode()).decode()

    # 2) Split into exactly n_tx pieces
    pieces = _split_into_n(b64, n_tx)

    # 3) Build packets: query + response per piece
    packets = []
    client_ip, server_ip = "10.0.0.10", "10.0.0.53"
    client_port, server_port = 33333, 53

    for i, part in enumerate(pieces):
        qname = f"piece{i}.treasure.local"

        # Query (qr=0)
        q_dns = DNS(id=0x2000 + i, qr=0, qdcount=1, qd=DNSQR(qname=qname, qtype="TXT"))
        q = Ether()/IP(src=client_ip, dst=server_ip)/UDP(sport=client_port, dport=server_port)/q_dns
        packets.append(q)

        # Response (qr=1)
        r_dns = DNS(
            id=0x2000 + i, qr=1, aa=1, qdcount=1, ancount=1,
            qd=DNSQR(qname=qname, qtype="TXT"),
            an=DNSRR(rrname=qname, type="TXT", ttl=60, rdata=part),
        )
        r = Ether()/IP(src=server_ip, dst=client_ip)/UDP(sport=server_port, dport=client_port)/r_dns
        packets.append(r)

    wrpcap(str(out), packets)
    print(f"[OK] Generated {out} with {n_tx} DNS TXT transactions (Base64). Flag length={len(flag_text)}; b64 length={len(b64)}")


def main():
    try:
        make_dns_txt_pcap_base64(FLAG, PCAP_PATH, NUM_TX)
    except Exception as e:
        print(f"[ERROR] PCAP generation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

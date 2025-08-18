import os, textwrap, sys, base64
from pathlib import Path

MODE = os.getenv("PCAP_MODE", "DNS_TXT").upper()  # DNS_TXT, DNS_BASE64, or ETH_PADDING
FLAG = os.getenv("FLAG", "CTF{pcap_padding_fun}")
PCAP_DIR = Path(os.getenv("PCAP_DIR", "/app/challenge"))
PCAP_NAME = os.getenv("PCAP_NAME", "sample.pcap")
CHUNK = int(os.getenv("DNS_CHUNK", "8"))  # smaller chunk size = more pieces

PCAP_DIR.mkdir(parents=True, exist_ok=True)
PCAP_PATH = PCAP_DIR / PCAP_NAME

def make_dns_txt_pcap(flag: str, out: Path, chunk: int, base64_encode=False):
    from scapy.all import Ether, IP, UDP, DNS, DNSQR, DNSRR, wrpcap
    data = flag
    if base64_encode:
        data = base64.b64encode(flag.encode()).decode()
    packets = []
    for i, part in enumerate(textwrap.wrap(data, chunk)):
        dns = DNS(
            id=0x2000 + i, qr=1, aa=1, qdcount=1, ancount=1,
            qd=DNSQR(qname=f"piece{i}.treasure.local", qtype="TXT"),
            an=DNSRR(rrname=f"piece{i}.treasure.local", type="TXT", ttl=60, rdata=part)
        )
        p = Ether()/IP(src="10.0.0.53", dst="10.0.0.10")/UDP(sport=53, dport=33333)/dns
        packets.append(p)
    wrpcap(str(out), packets)

def make_eth_padding_pcap(flag: bytes, out: Path, chunk: int):
    from scapy.all import Ether, IP, UDP, Padding, wrpcap
    packets = []
    src = "10.0.0.10"; dst = "10.0.0.20"
    idx = 0
    count = max(6, (len(flag) + chunk - 1) // chunk + 1)
    for i in range(count):
        payload = f"hello{i}".encode()
        p = Ether()/IP(src=src, dst=dst)/UDP(sport=40000+i, dport=50000)/payload
        extra = flag[idx:idx+chunk]
        idx += len(extra)
        if extra:
            p = p / Padding(extra)
        packets.append(p)
    wrpcap(str(out), packets)

def main():
    if MODE == "DNS_TXT":
        make_dns_txt_pcap(FLAG, PCAP_PATH, CHUNK)
    elif MODE == "DNS_BASE64":
        make_dns_txt_pcap(FLAG, PCAP_PATH, CHUNK, base64_encode=True)
    elif MODE == "ETH_PADDING":
        make_eth_padding_pcap(FLAG.encode(), PCAP_PATH, CHUNK)
    else:
        print(f"[WARN] Unknown PCAP_MODE={MODE}; defaulting to DNS_TXT")
        make_dns_txt_pcap(FLAG, PCAP_PATH, CHUNK)
    print(f"[OK] Generated {PCAP_PATH} for flag='{FLAG}' (mode={MODE})")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] PCAP generation failed: {e}", file=sys.stderr)
        sys.exit(1)

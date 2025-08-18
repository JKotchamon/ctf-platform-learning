FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 FLASK_APP=web.app

# copy source
COPY web/ /app/web/
COPY challenge/ /app/challenge/
COPY requirements.txt /app/requirements.txt
COPY entrypoint.sh /app/entrypoint.sh

RUN pip install --no-cache-dir -r /app/requirements.txt \
 && chmod +x /app/entrypoint.sh

# default env (override in compose)
ENV PCAP_DIR=/app/challenge \
    PCAP_NAME=sample.pcap \
    PCAP_MODE=DNS_TXT \
    DNS_CHUNK=12 \
    ETH_CHUNK=6

EXPOSE 8080
ENTRYPOINT ["/app/entrypoint.sh"]

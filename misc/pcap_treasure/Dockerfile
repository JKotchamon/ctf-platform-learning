FROM python:3.11-slim

WORKDIR /app

# (Optional) small base utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata ca-certificates && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # flask, scapy:contentReference[oaicite:2]{index=2}

# App code
COPY . .

# Normalize Windows line-endings and make entrypoint executable
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/app/entrypoint.sh"]

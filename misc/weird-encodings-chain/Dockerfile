# syntax=docker/dockerfile:1
FROM python:3.11-slim

# System deps (optional but handy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tini && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/app

# Install Python deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Normalize line endings and ensure executability
RUN sed -i 's/\r$//' /srv/app/entrypoint.sh /srv/app/tools/*.py /srv/app/app/app.py && \
    chmod +x /srv/app/entrypoint.sh

# The Flask app listens on 8081 (see app.py):contentReference[oaicite:1]{index=1}
EXPOSE 8081

# Use tini to handle signals cleanly
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/srv/app/entrypoint.sh"]

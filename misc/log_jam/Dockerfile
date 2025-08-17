FROM python:3.11-slim

# Prevent Python from writing .pyc and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# We’ll use only stdlib; no extra deps
COPY generate_logs.py entrypoint.sh README_player.md /app/
RUN chmod +x /app/entrypoint.sh

# Expose simple HTTP to let players download logs
EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
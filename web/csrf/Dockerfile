# Simple, reproducible container for GZ::CTF deployment (no env flag).
FROM python:3.11-slim

# Prevents Python from writing .pyc and enables unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create the sqlite file at build/run time by touching; app will init schema on first request
RUN python - <<'PY'
open('db.sqlite3','a').close()
PY

EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]

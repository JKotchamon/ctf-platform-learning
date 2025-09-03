# Dockerfile
# Python + Playwright (Chromium) base
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps for Playwright/Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libnss3 libx11-6 libxkbcommon0 libdrm2 libgbm1 libasound2 \
    libatk1.0-0 libatk-bridge2.0-0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libpango-1.0-0 libpangocairo-1.0-0 libcairo2 \
    fonts-liberation libjpeg62-turbo libpng16-16 \
    ca-certificates curl wget gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Install Chromium for Playwright
RUN python -m playwright install --with-deps chromium

# App files
COPY app.py index.html style.css ./

EXPOSE 8888

# ✅ Concurrency so /report doesn't block the admin visit
#  - 2 workers
#  - gthread worker class with 4 threads each (total up to 8 concurrent requests)
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "-b", "0.0.0.0:8888", "app:app"]

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# Minimal libs; playwright will add the rest with --with-deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Chromium for Playwright (this pulls OS deps, too)
RUN python -m playwright install --with-deps chromium

COPY app.py index.html style.css ./
EXPOSE 8888
CMD ["gunicorn","-w","2","-k","gthread","--threads","4","-b","0.0.0.0:8888","app:app"]

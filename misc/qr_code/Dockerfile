FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py generate_assets.py entrypoint.sh ./
RUN mkdir -p static && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
ENTRYPOINT ["bash", "entrypoint.sh"]

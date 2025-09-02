FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /data

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && flask run --host=0.0.0.0 --port=5000"]

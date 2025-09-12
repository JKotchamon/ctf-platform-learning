FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py entrypoint.sh ./ 
COPY templates ./templates

RUN useradd -ms /bin/bash ctf && chown -R ctf:ctf /app
USER ctf

EXPOSE 6666
ENTRYPOINT ["./entrypoint.sh"]

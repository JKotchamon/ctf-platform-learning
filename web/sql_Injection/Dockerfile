FROM python:3.12-slim

# Safety + smaller image
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m ctf
WORKDIR /challenge

# Copy app
COPY app/ ./app/
RUN mkdir -p /data && chown -R ctf:ctf /data

# Install deps
RUN pip install --no-cache-dir -r app/requirements.txt

# Init DB at container start if empty
COPY --chown=ctf:ctf app/init_db.py ./init_db.py

USER ctf

# Start script: init DB once then run Flask
CMD [ "bash", "-lc", "if [ ! -f /data/app.db ]; then python init_db.py; fi && FLASK_APP=app/app.py flask run --host=0.0.0.0 --port=8080" ]

EXPOSE 8080

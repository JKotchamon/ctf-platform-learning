FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8081

WORKDIR /srv/app

# Create non-root user
RUN adduser --disabled-password --gecos '' app

# Deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code and give it to `app`
COPY --chown=app:app app ./app
COPY --chown=app:app tools ./tools
COPY --chown=app:app entrypoint.sh ./entrypoint.sh
RUN chmod +x /srv/app/entrypoint.sh \
    && mkdir -p /srv/app/app/challenge \
    && chown -R app:app /srv/app

EXPOSE 8081
USER app
ENTRYPOINT ["/srv/app/entrypoint.sh"]

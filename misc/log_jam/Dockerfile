FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Normalize CRLF on Windows and ensure script is executable
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh \
    && mkdir -p /app/logs

EXPOSE 9999
CMD ["/bin/bash", "/app/entrypoint.sh"]

FROM python:3.11-slim

# Security + reliability basics
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Non-root user
RUN useradd -m ctf && chown -R ctf /app
USER ctf

# No EXPOSE here; GZ::CTF maps the port for you.
CMD ["python", "app.py"]

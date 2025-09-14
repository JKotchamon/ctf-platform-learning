# Use a slim Python base
FROM python:3.11-slim

# Security basics
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# Install deps
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py /app/
COPY templates/ /app/templates/

# Expose the challenge port
EXPOSE 6666

# Default envs (GZCTF will override GZCTF_FLAG at runtime)
ENV PORT=6666

# Run
CMD ["python", "app.py"]

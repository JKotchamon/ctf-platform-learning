FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

# Install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 # sanity check: make the build fail if Flask isn't present
 && python - <<'PY'
import importlib, sys
m = importlib.import_module("flask")
print("Flask OK:", getattr(m, "__version__", "unknown"))
PY

# App code
COPY app ./app
COPY tools ./tools
COPY entrypoint.sh .
RUN chmod +x /srv/app/entrypoint.sh

EXPOSE 8081
ENTRYPOINT ["./entrypoint.sh"]

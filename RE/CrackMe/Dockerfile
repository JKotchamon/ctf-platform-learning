# ---------- build stage ----------
FROM alpine:3.20 AS build
RUN apk add --no-cache build-base openssl-dev
WORKDIR /src
COPY checker/ ./checker/
# Build checker with FLAG env at build time
# Example: docker build --build-arg FLAG="CTF{AES_is_more_fun}" ...
ARG FLAG
ENV FLAG=${FLAG}
WORKDIR /src/checker
RUN make clean && make all

# ---------- run stage ----------
FROM python:3.11-alpine
WORKDIR /app
RUN apk add --no-cache libcrypto3 curl
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY web/ /app/
COPY --from=build /src/checker/checker /app/checker/checker
EXPOSE 8000
CMD ["python", "app.py"]

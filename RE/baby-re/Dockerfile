# Build stage: compile the challenge
FROM debian:stable-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app/challenge
COPY challenge/ ./
RUN make && strip baby-re-1

# Run stage: python web app + compiled binary
FROM python:3.11-slim
WORKDIR /app
# copy challenge binary
COPY --from=build /app/challenge /app/challenge
# copy web app
COPY web /app/web
RUN pip install --no-cache-dir flask
ENV EXECUTE_TO_VERIFY=false
ENV FLASK_SECRET=change-me
EXPOSE 8000
CMD ["python", "web/app.py"]

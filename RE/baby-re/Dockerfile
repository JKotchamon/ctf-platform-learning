# Build stage
FROM debian:stable-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY challenge/ /src/
RUN make

# Runtime stage
FROM python:3.11-slim
WORKDIR /srv
# Copy artifacts only
COPY --from=build /src/baby-re-1 /srv/baby-re-1
COPY --from=build /src/README.md /srv/README.md
# Optional: show an index page
RUN printf '%s\n' \
  "<h1>baby-re-1</h1>" \
  "<p>Download the binary and README:</p>" \
  "<ul><li><a href=\"/baby-re-1\">baby-re-1</a></li><li><a href=\"/README.md\">README.md</a></li></ul>" \
  > /srv/index.html
EXPOSE 8080
CMD ["python", "-m", "http.server", "8080"]

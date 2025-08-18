# Stage 1: build assets (optional; you already did via build.sh)
FROM alpine:3.20 AS builder
WORKDIR /app
# (If you need pip to run generator inside the image, keep these lines.
# In your current flow, build.sh already generated dist/, so this stage is optional.)

# Final stage: static server
FROM nginx:alpine
# Copy your built site
COPY dist/ /usr/share/nginx/html/
# Nginx serves on 80 in-container
EXPOSE 80

FROM nginx:alpine

# Copy static site
COPY index.html /usr/share/nginx/html/index.html
COPY about.html /usr/share/nginx/html/about.html
COPY resources.html /usr/share/nginx/html/resources.html
COPY styles.css /usr/share/nginx/html/styles.css

# Optional hardening / cosmetics
RUN sed -i 's/# server_tokens off;/server_tokens off;/' /etc/nginx/nginx.conf

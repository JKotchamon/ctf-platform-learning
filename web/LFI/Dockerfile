FROM alpine:3.20

# Install nginx + PHP 8.2 (CLI+FPM)
RUN apk add --no-cache \
    nginx \
    php82 php82-fpm php82-opcache php82-session php82-mbstring php82-ctype php82-json

# App files
COPY src/ /var/www/html/
COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY deploy/start.sh /start.sh

# Permissions & prep
RUN adduser -D -g '' www \
 && chown -R www:www /var/www/html \
 && chmod +x /start.sh \
 && mkdir -p /run/nginx /run/php

EXPOSE 80
CMD ["/start.sh"]

#!/bin/sh
set -e

# Dynamic flag (GZ::CTF injects GZCTF_FLAG at container start)
FLAG="${GZCTF_FLAG:-flag{LOCAL_TEST}}"

# Write to webroot so 'ls' (default CWD) reveals it post-RCE
echo "$FLAG" > /var/www/html/flag
chmod 644 /var/www/html/flag
chown www:www /var/www/html/flag || true

# PHP-FPM on TCP; keep env
sed -i 's|^;daemonize = yes|daemonize = no|' /etc/php82/php-fpm.conf
sed -i 's|^listen = .*|listen = 127.0.0.1:9000|' /etc/php82/php-fpm.d/www.conf
sed -i 's|^;clear_env = no|clear_env = no|' /etc/php82/php-fpm.d/www.conf || true

php-fpm82 -D
nginx -g 'daemon off;'

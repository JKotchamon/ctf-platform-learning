FROM php:8.2-apache

# Configure Apache + PHP execution for extra extensions and listen on 6666
RUN set -eux; \
  echo 'AddType application/x-httpd-php .php .phtml .php5' > /etc/apache2/conf-available/phtml.conf; \
  a2enconf phtml; \
  sed -ri 's/^Listen 80$/Listen 6666/' /etc/apache2/ports.conf; \
  sed -ri 's!<VirtualHost \*:80>!<VirtualHost *:6666>!g' /etc/apache2/sites-available/000-default.conf; \
  \
  # Deny direct HTTP access to dotfiles and flag* inside /uploads (forces RCE path)
  printf '%s\n' \
  '<Directory "/var/www/html/uploads">' \
  '  Options -Indexes' \
  '  <FilesMatch "^\..*|^flag(\..*)?$">' \
  '    Require all denied' \
  '  </FilesMatch>' \
  '</Directory>' \
  > /etc/apache2/conf-available/uploads-protect.conf; \
  a2enconf uploads-protect; \
  \
  # Folders for app data
  mkdir -p /var/www/html/uploads /var/www/html/data; \
  chown -R www-data:www-data /var/www/html/uploads /var/www/html/data; \
  chmod 775 /var/www/html/uploads /var/www/html/data

# App code
COPY src/ /var/www/html/

# Dynamic-flag entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 6666
CMD ["/entrypoint.sh"]

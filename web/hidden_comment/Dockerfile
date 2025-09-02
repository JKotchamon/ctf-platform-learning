# Dockerfile
FROM nginx:alpine

# For the tiny entrypoint script
RUN apk add --no-cache bash

# Put the site where nginx serves from
WORKDIR /usr/share/nginx/html

# Copy your static site
COPY index.html about.html resources.html styles.css ./

# Copy our start script that will inject the per-instance flag
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# nginx listens on 80 in the container
EXPOSE 80

# On start: inject the flag, then run nginx in the foreground
CMD ["/bin/sh","-c","/entrypoint.sh && nginx -g 'daemon off;'"]

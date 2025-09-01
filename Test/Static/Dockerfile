FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY index.html ./index.html

# Nginx normally listens on 80, so we replace it with 8080
RUN sed -i 's/listen       80;/listen 8080;/g' /etc/nginx/conf.d/default.conf



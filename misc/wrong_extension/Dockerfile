# Use a small Nginx image
FROM nginx:1.27-alpine

# Copy our nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static assets into the html directory
COPY index.html style.css script.js picture.jpg /usr/share/nginx/html/

EXPOSE 80

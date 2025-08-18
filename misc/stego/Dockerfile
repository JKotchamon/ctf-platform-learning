FROM nginx:alpine
# Static site generated into ./dist by build.sh
COPY dist/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
FROM nginx:1.19.6


COPY nginx.conf /etc/nginx/nginx.conf

VOLUME [ "/html" ]
EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]
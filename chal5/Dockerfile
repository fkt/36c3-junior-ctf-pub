FROM ubuntu:18.04 as base

RUN apt -y update && \
    apt -y install nginx && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf /nginx/index.html
COPY flag /

CMD ["nginx"]

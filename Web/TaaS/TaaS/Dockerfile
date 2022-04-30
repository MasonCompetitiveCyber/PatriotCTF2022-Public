FROM alpine:latest

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN apk add --no-cache python3 py3-pip
RUN pip3 install -r requirements.txt
RUN rm /usr/bin/nc

COPY . .

EXPOSE 5000

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]
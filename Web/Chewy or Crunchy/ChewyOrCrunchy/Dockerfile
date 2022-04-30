FROM alpine:latest

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

COPY /app/bot/geckodriver  /usr/local/bin/geckodriver
RUN chmod 777 /usr/local/bin/geckodriver

RUN apk add --no-cache python3 py3-pip firefox
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]
FROM nickgryg/alpine-pandas:latest

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN apk add --no-cache --update python3 py3-pip libreoffice

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]
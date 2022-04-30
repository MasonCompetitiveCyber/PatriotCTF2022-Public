FROM furritos/pycryptodome:3.8-alpine

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN apk add --no-cache python3 py3-pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]
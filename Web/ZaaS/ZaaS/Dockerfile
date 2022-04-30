FROM alpine:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN addgroup pctf && adduser pctf --disabled-password --ingroup pctf

WORKDIR /app
RUN chown -R pctf:pctf /app

COPY --chown=pctf:pctf ./requirements.txt /app/requirements.txt

RUN apk add --no-cache python3 py3-pip
RUN rm /usr/bin/nc
USER pctf
RUN pip3 install --user -r requirements.txt

COPY --chown=pctf:pctf . .

EXPOSE 5000

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]

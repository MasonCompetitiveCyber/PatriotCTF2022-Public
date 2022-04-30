FROM ubuntu:18.04

RUN apt update -y || true
RUN apt install -y curl wget socat --no-install-recommends

RUN rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/webmaster -m -p verylongandveryverygoood123456789passwordthatisverystrongandgood webmaster

WORKDIR /www

COPY flag /www
RUN chmod 644 flag
COPY index.html /www
COPY mcchttp /www

USER webmaster

CMD /www/mcchttp 8080

from ubuntu:latest

RUN apt update -y || true
RUN apt install -y socat --no-install-recommends

RUN rm -rf /var/lib/apt/lists/*

COPY flag .
RUN chmod 644 flag

RUN useradd -d /home/shellbox -m -p 1c25420c0a900db04533a2448fa276e9b9c5f3b15f080d9f37de5d26b6862cfda Koopa

WORKDIR shellbox/
COPY grnshll .
RUN chmod +x grnshll

USER Koopa
CMD socat TCP4-LISTEN:3839,reuseaddr,fork EXEC:./grnshll

from ubuntu:latest

RUN apt update -y || true
RUN apt install -y socat qemu-system-x86 --no-install-recommends

RUN rm -rf /var/lib/apt/lists/*

COPY initramfs.cpio.gz .
COPY vmlinuz .
COPY run.sh .
COPY run_qemu.sh .

RUN chmod +x run.sh
RUN chmod +x run_qemu.sh

CMD /run.sh
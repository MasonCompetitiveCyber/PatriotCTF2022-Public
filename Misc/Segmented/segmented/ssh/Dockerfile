FROM alpine:3

RUN \
	apk add --no-cache openssh-server && \
	adduser -D -s /sbin/nologin worker && \
	echo worker:lNdZTPtUWHaKO3TRMGhLHxJIyvhL1Y | chpasswd &&\
	mkdir /home/worker/.ssh && \
	chmod 700 /home/worker/.ssh

COPY --chown=worker id_ed25519 id_ed25519.pub /home/worker/.ssh/

RUN \
	chmod 600 /home/worker/.ssh/id_* && \
	cp /home/worker/.ssh/id_ed25519.pub /home/worker/.ssh/authorized_keys && \
	chown worker:worker /home/worker/.ssh -R && \
	ssh-keygen -A && \
	echo "Welcome to WeDigTunnels, Inc." > /etc/motd && \
	echo "This is a secure system. NO UNAUTHORIZED ACCESS!" >> /etc/motd && \
	sed -i 's/AllowTcpForwarding no/AllowTcpForwarding local/g' /etc/ssh/sshd_config

EXPOSE 22

CMD /usr/sbin/sshd -D -e -p 22

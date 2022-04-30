FROM alpine:3.15.0
RUN apk add samba-server attr && rm -rf /var/cache/apk/* && mkdir /share && chmod 777 /share
COPY smb.conf /etc/samba/smb.conf
COPY run.sh /
EXPOSE 445/tcp
CMD sh /run.sh
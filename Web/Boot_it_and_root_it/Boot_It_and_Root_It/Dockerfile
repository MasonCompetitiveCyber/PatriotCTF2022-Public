FROM ubuntu

RUN apt update -y && apt upgrade -y
RUN apt install default-jre default-jdk -y
RUN apt install netcat curl -y

COPY /secret/flag.txt /root/.flag.txt

RUN echo 'root:august11' | chpasswd

RUN useradd -ms /bin/bash regi
WORKDIR /home/regi
COPY . .
RUN mkdir -p /home/.someuser/...
RUN cp /etc/shadow /home/.someuser/.../shadow
RUN chown regi:  /home/.someuser/.../shadow
RUN chown regi: -R /home/regi
RUN rm -rf /home/regi/secret
USER regi
RUN touch test.mv.db
EXPOSE 8080
EXPOSE 5555
CMD ["./mvnw","spring-boot:run"]

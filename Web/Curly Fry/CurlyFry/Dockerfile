FROM golang:alpine
RUN apk --no-cache add gcc g++ make git
WORKDIR /go/src/app
COPY . .
RUN mv ./recipe.txt /root/recipe.txt
RUN GOOS=linux go build -ldflags="-s -w" -o /go/bin/web-app ./main.go
EXPOSE 80
ENTRYPOINT /go/bin/web-app
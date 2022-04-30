docker build . --tag mcchttp:latest
docker run --rm -d -p8080:8080 mcchttp:latest

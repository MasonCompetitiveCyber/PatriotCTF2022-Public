docker build . --tag greenshell:latest
docker run --rm -d -p3839:3839 greenshell:latest

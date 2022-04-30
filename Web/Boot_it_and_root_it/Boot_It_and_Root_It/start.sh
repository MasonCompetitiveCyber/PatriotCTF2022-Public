#!/bin/bash

sudo docker stop rce
sudo docker rm rce
sudo docker build . -t rce 
sudo docker run -p 8080:8080 -p 5555:5555 -d --name rce rce

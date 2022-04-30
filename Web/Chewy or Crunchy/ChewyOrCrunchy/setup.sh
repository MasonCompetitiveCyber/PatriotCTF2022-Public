#!/bin/bash
apt install -y sqlite3
wget -O "/tmp/geckodriver.tar.gz" "https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz"
gunzip /tmp/geckodriver.tar.gz
tar xvf /tmp/geckodriver.tar -C /tmp
mv /tmp/geckodriver /usr/local/bin/geckodriver
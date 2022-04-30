FROM php:apache

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y python3.9

COPY --chown=www-data:www-data . /var/www/html
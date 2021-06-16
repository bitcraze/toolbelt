FROM python:3.9-alpine

ENV PYTHONIOENCODING UTF-8

# RUN apt-get update && apt-get install -y curl
RUN apk add --no-cache curl git openssh

# Install docker
ENV DOCKER_VERSION 19.03.1
RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz && tar --strip-components=1 -xvzf docker-${DOCKER_VERSION}.tgz -C /usr/local/bin

# /tb-module is where the current dir in the docker host is mounted.
WORKDIR /tb-module

# /module is used for releases when we check out code in the toolbelt container
# It is passed on to the builder with --volumes-from
# Make sure it is accessible for all users
RUN mkdir /module && chmod 777 /module
VOLUME /module

ENTRYPOINT ["/toolbelt/toolbelt.py"]

ADD toolbelt /toolbelt

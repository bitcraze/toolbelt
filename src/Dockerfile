FROM debian

RUN apt-get update && apt-get install curl python3 git -y
ENV PYTHONIOENCODING UTF-8

# Install docker (see https://github.com/docker-library/docker)
ENV DOCKER_VERSION 17.04.0-ce
RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-${DOCKER_VERSION}.tgz && tar --strip-components=1 -xvzf docker-${DOCKER_VERSION}.tgz -C /usr/local/bin

# /tb-module is where the current dir in the docker host is mounted.
WORKDIR /tb-module

# /module is used for releases when we check out code in the toolbelt container
# It is passed on to the builder with --volumes-from
# Make sure it is accessible for all users
RUN mkdir /module && chmod 777 /module
VOLUME /module

ENTRYPOINT ["/toolbelt/toolbelt.py"]

ADD toolbelt /toolbelt

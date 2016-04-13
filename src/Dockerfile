FROM debian

RUN apt-get update && apt-get install curl python3 -y

# Install docker (see https://github.com/docker-library/docker)
ENV DOCKER_BUCKET get.docker.com
ENV DOCKER_VERSION 1.10.3
ENV DOCKER_SHA256 d0df512afa109006a450f41873634951e19ddabf8c7bd419caeb5a526032d86d
RUN curl -fSL "https://${DOCKER_BUCKET}/builds/Linux/x86_64/docker-$DOCKER_VERSION" -o /usr/local/bin/docker \
	&& echo "${DOCKER_SHA256}  /usr/local/bin/docker" | sha256sum -c - \
	&& chmod +x /usr/local/bin/docker

# /tb-module is where the current dir in the docker host is mounted.
WORKDIR /tb-module

# /module is used for releases. when we check out code in the toolbelt container
# It is passed on to the builder with --volumes-from
VOLUME /module

ENTRYPOINT ["/toolbelt/toolbelt.py"]

ADD toolbelt /toolbelt

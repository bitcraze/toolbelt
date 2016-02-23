FROM debian

RUN apt-get update && apt-get install curl python3 -y
RUN curl -sSL https://get.docker.com/ | sh

# /tb-module is where the current dir in the docker host is mounted.
WORKDIR /tb-module

# /module is used for releases. when we check out code in the toolbelt container
# It is passed on to the builder with --volumes-from
VOLUME /module

ENTRYPOINT ["/toolbelt/toolbelt.py"]

ADD toolbelt /toolbelt

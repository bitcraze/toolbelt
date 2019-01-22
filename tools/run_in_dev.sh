#!/usr/bin/env bash
set -e

scriptDir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

docker run --rm -it -e "HOST_CW_DIR=${PWD}" -v ${scriptDir}/../src/toolbelt:/toolbelt -v ${scriptDir}/..:/tb-module -v /var/run/docker.sock:/var/run/docker.sock my_toolbelt "$@"
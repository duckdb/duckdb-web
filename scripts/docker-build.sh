#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the repository root
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

. scripts/docker-vars.sh

docker build . \
    --tag ${JEKYLL_DOCKER_IMAGE_NAME} \
    --build-arg UID=$(id -u) \
    --build-arg UNAME=$(id -un) \
    --build-arg GID=$(id -g) \
    --build-arg GNAME=$(id -gn)

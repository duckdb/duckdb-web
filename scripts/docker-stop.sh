#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the repository root
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

. scripts/docker-vars.sh

docker rm --force \
    ${JEKYLL_DOCKER_CONTAINER_NAME=duckdb-jekyll}

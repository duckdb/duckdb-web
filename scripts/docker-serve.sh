#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the repository root
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

scripts/docker-stop.sh

. scripts/docker-vars.sh

docker run \
    --rm \
    --interactive \
    --name ${JEKYLL_DOCKER_CONTAINER_NAME} \
    --user "$(id -un):$(id -gn)" \
    --volume="${PWD}:/srv/jekyll:Z" \
    --publish 4000:4000 \
    --publish 35729:35729 \
    ${JEKYLL_DOCKER_IMAGE_NAME} \
    bundle exec jekyll serve \
        --host 0.0.0.0 \
        --incremental \
        --livereload \
        $@

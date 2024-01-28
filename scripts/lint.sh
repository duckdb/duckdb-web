#!/usr/bin/env bash

set -xeuo pipefail

fix=''
check='--check --diff'
while getopts "f" opt; do
    case $opt in
        f) fix="--fix"
           check='';;
        *) exit
    esac
done

npx markdownlint-cli docs/ dev/ _posts/ --config .markdownlint.jsonc --ignore docs/archive $fix || echo 'mdlit failed'

black scripts --skip-string-normalization $check  || echo 'black failed'

if ! $(which vale); then
    echo "Vale binary not found, please install it from https://vale.sh/docs/vale-cli/installation/"
    exit 1
fi

vale sync
vale docs/ dev/ _posts/ --glob "!docs/archive/*"


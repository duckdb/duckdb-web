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

npx markdownlint-cli docs/stable/ docs/preview/ _posts/ --config .markdownlint.jsonc $fix || echo 'markdownlint failed'

black scripts --skip-string-normalization $check || echo 'black failed'

if ! $(which vale); then
    echo "Vale binary not found, please install it from https://vale.sh/docs/vale-cli/installation/"
    exit 1
fi

vale sync
vale docs/stable/ docs/preview/ _posts/

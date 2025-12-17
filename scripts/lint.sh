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

npx markdownlint-cli docs/stable/ _posts/ --config .markdownlint.jsonc ${fix} || echo 'markdownlint failed'

black scripts --skip-string-normalization $check || echo 'black failed'

if ! $(which vale); then
    echo "Vale binary not found, please install it from https://vale.sh/docs/vale-cli/installation/"
    exit 1
fi

vale sync
vale docs/stable/ _posts/ _media/ _science/

if ag --md -l "https://www.youtube.com/embed/"; then
    echo 'Found "https://www.youtube.com/embed/ strings, please use "https://www.youtube-nocookie.com/embed/" instead'

    if [[ "${fix}" == "--fix" ]]; then
        ag --md -l "https://www.youtube.com/embed/" | xargs sed -i 's|https://www.youtube.com/embed/|https://www.youtube-nocookie.com/embed/|g'
    fi
    exit 1
fi

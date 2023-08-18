#!/usr/bin/env bash

set -xeuo pipefail

fix=${1-}

npx markdownlint-cli docs/ dev/ _posts/ --config .markdownlint.jsonc --ignore docs/archive $fix

check=''
if [ -z $fix ]; then
    check='--check --diff'
fi
black scripts --skip-string-normalization $check

vale sync
vale docs/ dev/ _posts/ --glob "!docs/archive/*"


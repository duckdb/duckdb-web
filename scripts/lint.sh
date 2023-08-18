#!/usr/bin/env bash

set -xeuo pipefail

npx markdownlint-cli docs/ --config .markdownlint.jsonc --ignore docs/archive
# --fix

black scripts --skip-string-normalization

vale sync
vale docs/ --glob "!docs/archive/*"

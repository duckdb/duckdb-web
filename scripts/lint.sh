#!/usr/bin/env bash

set -xeuo pipefail


npx markdownlint-cli docs/ dev/ _posts/ --config .markdownlint.jsonc --ignore docs/archive

black scripts --skip-string-normalization

vale sync
vale docs/ dev/ _posts/ --glob "!docs/archive/*"


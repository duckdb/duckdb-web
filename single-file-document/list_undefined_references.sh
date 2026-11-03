#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the directory of the script
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

./generate_latex.sh

export max_print_line=1000
for document in duckdb-docs duckdb-blog; do
    latexmk -xelatex ${document}.tex

    # grep returns a non-zero exit code if there are no missing references
    grep '^LaTeX Warning: Hyper reference' ${document}.log | tee ${document}-missing-references.log || true
done

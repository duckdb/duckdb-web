#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the directory of the script
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

./generate_latex.sh

latexmk -xelatex duckdb-docs.tex

grep -C 2 '^LaTeX Warning: Hyper reference' duckdb-docs.log | tee duckdb-docs-missing-references.log

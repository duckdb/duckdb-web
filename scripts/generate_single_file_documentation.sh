#!/usr/bin/env bash

set -xeuo pipefail

# requires pandoc to be installed

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

rm -f duckdb-docs.pdf

python3 ./scripts/concatenate_files.py

pandoc duckdb-docs.md \
    --from=markdown_github+header_attributes \
    --metadata-file=single-file-document/metadata.yaml \
    --output=duckdb-docs.tex \
    --table-of-contents \
    --variable=urlcolor:blue \
    --data-dir=single-file-document \
    --template=eisvogel2.tex \
    --variable=titlepage

pandoc duckdb-docs.md \
    --from=markdown_github+header_attributes \
    --to=pdf \
    --metadata-file=single-file-document/metadata.yaml \
    --output=duckdb-docs.pdf \
    --pdf-engine=xelatex \
    --table-of-contents \
    --variable=urlcolor:blue \
    --data-dir=single-file-document \
    --template=eisvogel2.tex \
    --variable=titlepage

#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the directory of the script
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pandoc \
    duckdb-docs.md \
    --output duckdb-docs-cleaned.md \
    --from markdown_github+header_attributes+tex_math_dollars-smart+markdown_in_html_blocks \
    --to markdown_github+header_attributes+tex_math_dollars-raw_html \
    --wrap=preserve

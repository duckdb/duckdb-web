#!/usr/bin/env sh

set -xeuo pipefail

pandoc \
    duckdb-docs.md \
    --output duckdb-docs-cleaned.md \
    --from markdown_github+header_attributes+tex_math_dollars-smart+markdown_in_html_blocks \
    --to markdown_github+header_attributes+tex_math_dollars-raw_html \
    --wrap=preserve

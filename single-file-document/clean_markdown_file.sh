#!/usr/bin/env sh

set -xeuo pipefail

for document in duckdb-docs duckdb-blog; do
    pandoc \
        ${document}.md \
        --output ${document}-cleaned.md \
        --from markdown_github+header_attributes+tex_math_dollars-smart+markdown_in_html_blocks \
        --to markdown_github+header_attributes+tex_math_dollars-raw_html \
        --wrap=preserve
done

#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the repository root
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

shopt -s extglob
rm -rf docs/!(stable)
find . -name '*.md' | xargs -I {} sed -E -i 's|\{% link ([^\}]*) %\}|https://duckdb.org/\1|g' {}
find . -name '*.md' | xargs -I {} sed -E -i 's|\{% post_url ([^\}]*) %\}|https://duckdb.org/\1.md|g' {}
cp *.md _site/
cp -r docs/stable _site/docs
cp -r _posts/* _site/

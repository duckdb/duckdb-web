#!/usr/bin/env bash
set -euo pipefail

bundler exec jekyll serve --incremental --livereload

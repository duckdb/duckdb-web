#!/usr/bin/env bash
set -euo pipefail

bundler exec jekyll serve --incremental --livereload --config _config.yml,_config_exclude_archive.yml

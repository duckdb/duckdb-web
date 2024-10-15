#!/usr/bin/env bash

set -xeuo pipefail

duckdb -markdown -c "SELECT format('[{}]({{% link extensions/{}.md %}})', name, name) as 'Name', format('[<span class=\"github\">GitHub</span>](https://github.com/{})', repo) as 'GitHub',  #4 as 'Description' FROM 'extensions/community_extensions.csv';" > extensions/list_extensions.md

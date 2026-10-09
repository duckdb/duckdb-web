#!/usr/bin/env bash

set -xeuo pipefail

# navigate to the directory of the script
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# set up the Python virtual environment
if [ ! -d venv ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --quiet --requirement requirements.txt

python3 concatenate_to_single_file.py
rm -f duckdb-docs.pdf

if [ $# -ge 1 ] && [ $1 == "--docker" ]; then
    docker run \
        --volume "$(pwd)/..:/data" \
        --workdir /data/single-file-document \
        pandoc/extra:3.6-ubuntu \
        --defaults pandoc-configuration.yaml
else
    pandoc --defaults pandoc-configuration.yaml
fi

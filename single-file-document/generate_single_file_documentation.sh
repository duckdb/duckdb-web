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

# generate the PDFs for the documentation (duckdb-docs) and the blog (duckdb-blog)
for document in duckdb-docs duckdb-blog; do
    rm -f ${document}.pdf
    pandoc_arguments=(
        --defaults pandoc-configuration.yaml
        --metadata-file metadata/${document}.yaml
        --output ${document}.pdf
        ${document}.md
    )

    if [ $# -ge 1 ] && [ $1 == "--docker" ]; then
        docker run \
            --volume "$(pwd)/..:/data" \
            --workdir /data/single-file-document \
            pandoc/extra:3.6-ubuntu \
            "${pandoc_arguments[@]}"
    else
        pandoc "${pandoc_arguments[@]}"
    fi
done

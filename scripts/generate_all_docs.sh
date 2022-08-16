#!/usr/bin/env sh

python3 ./scripts/generate_config_docs.py
python3 ./scripts/generate_descriptions.py
python3 ./scripts/generate_docs.py
python3 ./scripts/generate_python_docs.py
node ./scripts/generate_nodejs_docs.js

# generate search index last, once all the docs are generated
python3 ./scripts/generate_search.py

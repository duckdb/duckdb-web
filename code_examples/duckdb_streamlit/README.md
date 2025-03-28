# Introduction

These are the scripts used in the [blog post]().

## Local execution
Go to `code_examples/duckdb_streamlit` and:
1. Create a virtual env: `python -m venv venv_duckdb_streamlit`
2. Activate the virtual env: `source ./venv_duckdb_streamlit/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. Run Streamlit application: `streamlit run app.py` 
5. Go to the address specified in the log (it will take around 1 minute to spin up)

## Cleanup

1. Deactivate venv `deactivate`
2. Remove venv: `rm -rf venv_duckdb_streamlit`


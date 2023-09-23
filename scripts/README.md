# DuckDB-Web scripts

## `generate_all_docs.sh`

### Prerequisites

Build DuckDB in `debug` mode. Install the Python client as well as the `httpfs` and `icu` extensions:

```bash
# build DuckDB CLI binary
GEN=ninja BUILD_HTTPFS=1 BUILD_ICU=1 OPENSSL_ROOT_DIR=/opt/homebrew/bin/ make debug
# install extensions to DuckDB CLI binary
build/debug/duckdb -c "INSTALL 'build/debug/extension/httpfs/httpfs.duckdb_extension';"
build/debug/duckdb -c "INSTALL 'build/debug/extension/icu/icu.duckdb_extension';"

# build DuckDB Python client
python3 tools/pythonpkg/setup.py install
# install extensions to Python client
python3 -c "import duckdb; duckdb.sql(\"INSTALL 'build/debug/extension/httpfs/httpfs.duckdb_extension';\")"
python3 -c "import duckdb; duckdb.sql(\"INSTALL 'build/debug/extension/icu/icu.duckdb_extension';\")"
```

Install the NodeJS and Python dependencies:

```bash
npm install
python -m pip install -r requirements.txt
```

### Running the script

Run the script as follows:

```bash
scripts/generate_all_docs.sh <path_to_duckdb_dir>
```

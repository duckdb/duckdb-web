# DuckDB-Web scripts

## `generate_all_docs.sh`

### Prerequisites

Build DuckDB in `debug` mode. Install the Python client as well as the `httpfs` and `icu` extensions:

```bash
# build the DuckDB CLI client
GEN=ninja BUILD_HTTPFS=1 BUILD_ICU=1 OPENSSL_ROOT_DIR=/opt/homebrew/bin/ make debug
# install extensions to the DuckDB CLI client
build/debug/duckdb -c "INSTALL 'build/debug/extension/httpfs/httpfs.duckdb_extension';"
build/debug/duckdb -c "INSTALL 'build/debug/extension/icu/icu.duckdb_extension';"

# build the DuckDB Python client
pip install -e tools/pythonpkg
# extensions are shared across clients so there is no need to install them to Python
```

Install the NodeJS and Python dependencies:

```bash
npm install
pip install -r requirements.txt
```

### Running the script

Run the script as follows:

```bash
./scripts/generate_all_docs.sh <path_to_duckdb_dir>
```

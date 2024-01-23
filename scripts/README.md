# DuckDB-Web scripts

## `generate_all_docs.sh`

### Prerequisites

Install the NodeJS and Python dependencies in the `duckdb-web directory`:

```bash
npm install
pip install -r requirements.txt
```

### Using DuckDB Nightly Build

Download the Nightly DuckDB distribution. Run the script as follows:

```bash
./scripts/generate_all_docs.sh <path_to_duckdb_binary>
```

### Using DuckDB `main`

Build DuckDB and install the `httpfs` and `icu` extensions. Go to the DuckDB directory and run:

```bash
GEN=ninja BUILD_HTTPFS=1 BUILD_ICU=1 make
build/debug/duckdb -c "INSTALL 'build/debug/extension/httpfs/httpfs.duckdb_extension';"
build/debug/duckdb -c "INSTALL 'build/debug/extension/icu/icu.duckdb_extension';"
```

Run the script as follows:

```bash
./scripts/generate_all_docs.sh <path_to_duckdb_source_directory>
```

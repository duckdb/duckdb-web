# DuckDB-Web scripts

## `generate_all_docs.sh`

### Prerequisites

Build DuckDB in `debug` mode and install the `httpfs` and `icu` extensions:

```bash
GEN=ninja BUILD_HTTPFS=1 BUILD_ICU=1 make debug
build/debug/duckdb -c "INSTALL 'build/debug/extension/httpfs/httpfs.duckdb_extension'; INSTALL 'build/debug/extension/icu/icu.duckdb_extension';"
```

Install the NodeJS dependencies:

```bash
npm install
```

### Running the script

Run the script as follows:

```bash
scripts/generate_all_docs.sh <path_to_duckdb_dir>
```

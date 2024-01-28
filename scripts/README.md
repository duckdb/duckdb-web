# DuckDB-Web scripts

## `generate_all_docs.sh`

### Prerequisites

Install the NodeJS and Python dependencies in the `duckdb-web` directory:

```bash
npm install
pip install -r requirements.txt
```

### Using DuckDB Nightly Build

Download the [Nightly DuckDB distribution](https://duckdb.org/docs/installation/?version=main), extract the `duckdb` file and move it to the directory expected by the scripts:

```bash
mkdir -p duckdb/build/release
mv duckdb duckdb/build/release
```

Run the script as follows:

```bash
./scripts/generate_all_docs.sh <path_to_duckdb_directory>
```

### Using DuckDB `main`

Build DuckDB and install the `httpfs` and `icu` extensions. Go to the DuckDB directory and run:

```bash
GEN=ninja BUILD_HTTPFS=1 BUILD_ICU=1 make
build/release/duckdb -c "INSTALL 'build/release/extension/httpfs/httpfs.duckdb_extension';"
build/release/duckdb -c "INSTALL 'build/release/extension/icu/icu.duckdb_extension';"
```

If you want to include the `spatial` extension, [build it](https://github.com/duckdb/duckdb_spatial#building-from-source) and install it:

```bash
cd duckdb_spatial
build/release/duckdb -c "INSTALL 'build/release/extension/icu/icu.duckdb_extension';"
```

Run the script as follows:

```bash
./scripts/generate_all_docs.sh <path_to_duckdb_source_directory>
```

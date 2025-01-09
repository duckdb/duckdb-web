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
mkdir -p build/release
mv duckdb build/release
```

Run the script as follows:

```bash
./scripts/generate_all_docs.sh <path_to_duckdb_directory>
```

### Using DuckDB `main`

Build DuckDB and install the in-tree extensions.

Go to the DuckDB directory and run:

```bash
GEN=ninja EXTENSION_CONFIGS=".github/config/in_tree_extensions.cmake" make
cd build/release/extension/
for EXTENSION in *; do
    ../duckdb -c "INSTALL '${EXTENSION}/${EXTENSION}.duckdb_extension';"
done
```

Run the script as follows:

```bash
./scripts/generate_all_docs.sh <path_to_duckdb_source_directory>
```

For a detailed guide on how to disable/enable extensions during build, see [Building and Installing Extensions from Source](https://duckdb.org/dev/building#building-and-installing-extensions-from-source).

---
layout: docu
title: Working with Extensions
---

## Downloading Extensions Directly from S3

Downloading an extension directly could be helpful when building a [lambda service](https://aws.amazon.com/pm/lambda/) or container that uses DuckDB.
DuckDB extensions are stored in public S3 buckets, but the directory structure of those buckets is not searchable.
As a result, a direct URL to the file must be used.
To directly download an extension file, use the following format:  

```text
http://extensions.duckdb.org/v{duckdb_version}/{platform_name}/{extension_name}.duckdb_extension.gz
```

For example:

```text
http://extensions.duckdb.org/v{{ site.currentduckdbversion }}/windows_amd64/json.duckdb_extension.gz
```

## Platforms

Extension binaries must be built for each platform. We distribute pre-built binaries for several platforms (see below).
For platforms where packages for certain extensions are not available, users can build them from source and [install the resulting binaries manually](#installing-extensions-from-an-explicit-path).

All official extensions are distributed for the following platforms.

<div class="narrow_table"></div>

| Platform name      | Description                              |
|--------------------|------------------------------------------|
| `linux_amd64`      | Linux AMD64 (Node.js packages, etc.)     |
| `linux_amd64_gcc4` | Linux AMD64 (Python packages, CLI, etc.) |
| `linux_arm64`      | Linux ARM64 (e.g., AWS Graviton)         |
| `osx_amd64`        | macOS (Intel CPUs)                       |
| `osx_arm64`        | macOS (Apple Silicon: M1, M2, M3 CPUs)   |
| `windows_amd64`    | Windows on Intel and AMD CPUs (x86_64)   |

Some extensions are distributed for the following platforms:

* `windows_amd64_rtools`
* `wasm_eh` and `wasm_mvp` (see [DuckDB-Wasm's extensions](../api/wasm/extensions))

For platforms outside of the ones listed above, we do not officially distribute extensions.

## Using a Custom Extension Repository

To load extensions from a custom extension repository, set the following configuration option.

### Local Files

```sql
SET custom_extension_repository = 'path/to/folder';
```

This assumes the pointed folder has a structure similar to:

```text
folder
└── 0fd6fb9198
    └── osx_arm64
        ├── autocomplete.duckdb_extension
        ├── httpfs.duckdb_extension
        ├── icu.duckdb_extension.gz
        ├── inet.duckdb_extension
        ├── json.duckdb_extension
        ├── parquet.duckdb_extension
        ├── tpcds.duckdb_extension
        ├── tpcds.duckdb_extension.gz
        └── tpch.duckdb_extension.gz
```

With at the first level the DuckDB version, at the second the DuckDB platform, and then extensions either as `name.duckdb_extension` or gzip-compressed files `name.duckdb_extension.gz`.

```sql
INSTALL icu;
```

for example will look for either `icu.duckdb_extension.gz` (first) or `icu.duckdb_extension` (second) in the repository structure, and install it to the `extension_directory` (that defaults to `~/.duckdb/extensions`), if file is compressed, decompression will be handled at this step.

### Remote File over http

```sql
SET custom_extension_repository = 'http://nightly-extensions.duckdb.org';
```

They work the same as local ones, and expect a similar folder structure.

### Remote Files over https or s3 Protocol

```sql
SET custom_extension_repository = 's3://bucket/your-repository-name/';
```

Remote extension repositories act similarly to local ones, as in the file structure should be the same and either gzipped or non-gzipped file are supported.

Only special case here is that `httpfs` extension should be available locally. You can get it for example doing:

```sql
RESET custom_extension_repository;
INSTALL httpfs;
```

That will install the official `httpfs` extension locally.

This is since httpfs extension will be needed to actually access remote encrypted files.

### `INSTALL x FROM y`

You can also use the `INSTALL` command's `FROM` clause to specify the path of the custom extension repository. For example:

```sql
FORCE INSTALL azure FROM 'http://nightly-extensions.duckdb.org';
```

This will [force install](#force-installing-extensions) the `azure` extension from the specified URL.

## Loading and Installing an Extension from Explicit Paths

### Installing Extensions from an Explicit Path

`INSTALL` can be used with the path to either a `.duckdb_extension` file or a `.duckdb_extension.gz` file.
For example, if the file was available into the same directory as where DuckDB is being executed, you can install it as follows:

```sql
-- uncompressed file
INSTALL 'path/to/httpfs.duckdb_extension';
-- gzip-compressed file
INSTALL 'path/to/httpfs.duckdb_extension.gz';
```

These will have the same results.

It is also possible to specify remote paths.

## Force Installing Extensions

When DuckDB installs an extension, it is copied to a local directory to be cached, avoiding any network traffic.
Any subsequent calls to `INSTALL extension_name` will use the local version instead of downloading the extension again. To force re-downloading the extension, run:

 by default in `~/.duckdb/extensions` but configurable via `SET extension_directory = path/to/existing/directory;`.

```sql
FORCE INSTALL extension_name;
```

## Loading Extension from a Path

`LOAD` can be used with the path to a `.duckdb_extension`.
For example, if the file was available at the (relative) path `path/to/httpfs.duckdb_extension`, you can load it as follows:

```sql
-- uncompressed file
LOAD 'path/to/httpfs.duckdb_extension';
```

This will skip any currently installed file in the specifed path.

Using remote paths for compressed files is currently not possible.

## Building and Installing Extensions

For building and installing extensions from source, see the [building guide](/dev/building#building-and-installing-extensions-from-source).

## Statically Linking Extensions

To statically link extensions, follow the [developer documentation's "Using extension config files" section](https://github.com/duckdb/duckdb/blob/main/extension/README.md#using-extension-config-files).

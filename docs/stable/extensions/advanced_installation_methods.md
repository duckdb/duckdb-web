---
layout: docu
title: Advanced Installation Methods
---

## Downloading Extensions Directly from S3

Downloading an extension directly can be helpful when building a [Lambda service](https://aws.amazon.com/pm/lambda/) or container that uses DuckDB.
DuckDB extensions are stored in public S3 buckets, but the directory structure of those buckets is not searchable.
As a result, a direct URL to the file must be used.
To download an extension file directly, use the following format:

```sql
http://extensions.duckdb.org/v⟨duckdb_version⟩/⟨platform_name⟩/⟨extension_name⟩.duckdb_extension.gz
```

For example:

```text
http://extensions.duckdb.org/v{{ site.current_duckdb_version }}/windows_amd64/json.duckdb_extension.gz
```

## Installing an Extension from an Explicit Path

The `INSTALL` command can be used with the path to a `.duckdb_extension` file:

```sql
INSTALL 'path/to/httpfs.duckdb_extension';
```

Note that compressed `.duckdb_extension.gz` files need to be decompressed beforehand. It is also possible to specify remote paths.

## Loading an Extension from an Explicit Path

`LOAD` can be used with the path to a `.duckdb_extension`.
For example, if the file was available at the (relative) path `path/to/httpfs.duckdb_extension`, you can load it as follows:

```sql
LOAD 'path/to/httpfs.duckdb_extension';
```

This will skip any currently installed extensions and load the specified extension directly.

Note that using remote paths for compressed files is currently not possible.

## Building and Installing Extensions from Source

For building and installing extensions from source, see the [Building DuckDB guide]({% link docs/stable/dev/building/overview.md %}).

### Statically Linking Extensions

To statically link extensions, follow the [developer documentation's “Using extension config files” section](https://github.com/duckdb/duckdb/blob/main/extension/README.md#using-extension-config-files).

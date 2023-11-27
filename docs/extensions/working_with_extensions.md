---
layout: docu
title: Working with Extensions
---

## Downloading Extensions Directly from S3

Downloading an extension directly could be helpful when building a lambda or container that uses DuckDB.
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
For platforms where packages for certain extensions are not available, users can build them from source and [install the resulting binaries manually](#loading-and-installing-an-extension-from-local-storage).

All official extensions are distributed for the following platforms:

* `linux_amd64`
* `linux_amd64_gcc4`
* `linux_arm64`
* `osx_amd64`
* `osx_arm64`
* `windows_amd64`

Only core extensions are distributed for the following platforms:

* `windows_amd64_rtools`
* `wasm_eh` and `wasm_mvp` (see [DuckDB-Wasm's extensions](../api/wasm/extensions))

We currently do not distribute binaries for extensions on the `linux_arm64_gcc4` platform.

## Using a Custom Extension Repository

To load extensions from a custom extension repository, set the following configuration option:

```sql
SET custom_extension_repository='bucket.s3.<region>.amazonaws.com/<your_extension_name>/latest';
```

## Loading and Installing an Extension from Local Storage

### Building Extensions

Build the extension following the instructions provided in the extension's README.

### Decompressing gzip Files

Extensions are stored in gzip format, so they must be decompressed prior to use. There are many methods to decompress gzip, including the command line `gunzip` tool available on most UNIX platforms.
The following code snippet uses Python to decompress a `.gz` file:

```python
import gzip
import shutil

with gzip.open('httpfs.duckdb_extension.gz','rb') as f_in:
   with open('httpfs.duckdb_extension', 'wb') as f_out:
     shutil.copyfileobj(f_in, f_out)
```

### Installing Extensions

After decompression, the `INSTALL` and `LOAD` commands can be used with the path to the `.duckdb_extension` file.
For example, if the file was unzipped into the same directory as where DuckDB is being executed, you can install it as follows:

```sql
INSTALL 'httpfs.duckdb_extension';
LOAD 'httpfs.duckdb_extension';
```

## Force Installing Extensions

When DuckDB installs an extension, they are copied to a local directory, by default in `~/.duckdb`. Any subsequent calls to `INSTALL <extension>` will use the local version instead of downloading the extension again. To force re-downloading the extension, run:

```sql
FORCE INSTALL extension_name;
```

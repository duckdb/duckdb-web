---
layout: docu
redirect_from:
- docs/archive/0.9.2/extensions/working_with_extensions
title: Working with Extensions
---

## Downloading Extensions Directly from S3

Downloading an extension directly could be helpful when building a lambda or container that uses DuckDB.
DuckDB extensions are stored in public S3 buckets, but the directory structure of those buckets is not searchable. 
As a result, a direct URL to the file must be used. 
To directly download an extension file, use the following format:  

```text
http://extensions.duckdb.org/v{release_version_number}/{platform_name}/{extension_name}.duckdb_extension.gz
```

For example:

```text
http://extensions.duckdb.org/v{{ site.currentduckdbversion }}/windows_amd64/json.duckdb_extension.gz
```

The list of supported platforms may increase over time, but the current list of platforms includes:

* linux_amd64_gcc4
* linux_amd64
* linux_arm64
* osx_amd64
* osx_arm64
* wasm_eh [DuckDB-Wasm's extensions](../api/wasm/extensions)
* wasm_mvp [DuckDB-Wasm's extensions](../api/wasm/extensions)
* windows_amd64
* windows_amd64_rtools

See above for a list of extension names and how to pull the latest list of extensions.

## Loading an Extension from Local Storage

Extensions are stored in gzip format, so they must be unzipped prior to use. 
There are many methods to decompress gzip. Here is a Python example:

```python
import gzip
import shutil

with gzip.open('httpfs.duckdb_extension.gz','rb') as f_in:
   with open('httpfs.duckdb_extension', 'wb') as f_out:
     shutil.copyfileobj(f_in, f_out)
```

After unzipping, the install and load commands can be used with the path to the `.duckdb_extension` file. 
For example, if the file was unzipped into the same directory as where DuckDB is being executed:

```sql
INSTALL 'httpfs.duckdb_extension';
LOAD 'httpfs.duckdb_extension';
```
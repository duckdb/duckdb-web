---
layout: docu
title: Using fsspec Filesystems
---

DuckDB support for [`fsspec`](https://filesystem-spec.readthedocs.io) filesystems allows querying data in filesystems that DuckDB's [`httpfs` extension]({% link docs/archive/1.1/extensions/httpfs/overview.md %}) does not support. `fsspec` has a large number of [inbuilt filesystems](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations), and there are also many [external implementations](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations). This capability is only available in DuckDB's Python client because `fsspec` is a Python library, while the `httpfs` extension is available in many DuckDB clients.

## Example

The following is an example of using `fsspec` to query a file in Google Cloud Storage (instead of using their S3-compatible API).

Firstly, you must install `duckdb` and `fsspec`, and a filesystem interface of your choice.

```bash
pip install duckdb fsspec gcsfs
```

Then, you can register whichever filesystem you'd like to query:

```python
import duckdb
from fsspec import filesystem

# this line will throw an exception if the appropriate filesystem interface is not installed
duckdb.register_filesystem(filesystem('gcs'))

duckdb.sql("SELECT * FROM read_csv('gcs:///bucket/file.csv')")
```

> These filesystems are not implemented in C++, hence, their performance may not be comparable to the ones provided by the `httpfs` extension.
> It is also worth noting that as they are third-party libraries, they may contain bugs that are beyond our control.
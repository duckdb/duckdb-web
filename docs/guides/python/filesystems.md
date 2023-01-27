---
title: Filesystems
layout: docu
---

> NOTICE: This feature is experimental, and is subject to change

DuckDB support for [`fsspec`](https://filesystem-spec.readthedocs.io) filesystems allows querying data in filesystems that DuckDB's `httpfs` extension does not support (eg, Azure, Alibaba).

The following is an example of using `fsspec` to query a file in Google Cloud Storage (instead of using their s3 inter-compatibility api).

Firstly, you must install `duckdb` and `fsspec`, and a filesystem interface of your choice
```sh
$ pip install duckdb fsspec gcsfs
```

then you can register whichever filesystem you'd like to query

```python
import duckdb
from fsspec import filesystem

conn = duckdb.connect()
conn.register_filesystem(filesystem('gcs'))  # this line will throw an exception if the appropriate filesystem interface is not installed

conn.execute('select * from 'gcs:///bucket/file.csv')

data = conn.fetchall()
```

# Potential issues

Please also note, that as these filesystems are not implemented in C++, their performance may not be comparable to the ones provided by the `httpfs` extension.
It's also worth noting that as they are third party libraries, they may contain bugs that are beyond our control.

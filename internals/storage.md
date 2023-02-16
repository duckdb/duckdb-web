---
layout: docu
title: Storage
---

The DuckDB internal storage format is currently in flux, and is expected to change with each release until we reach v1.0.0.

DuckDB files start with a `uint64_t` which contains a checksum for the main header, followed by four magic bytes (`DUCK`), followed by the storage version number in a `uint64_t`.
A simple example of reading the storage version using python is below.

```py
import struct

pattern = struct.Struct('<8x4sQ')

with open('test/sql/storage_version/storage_version.db', 'rb') as fh:
    print(pattern.unpack(fh.read(pattern.size)))
```

For changes in each given release, check out the [changelog](https://github.com/duckdb/duckdb/releases) on GitHub.
To see the commits that changed each storage version, see the [commit log](https://github.com/duckdb/duckdb/commits/master/src/storage/storage_info.cpp)

| Storage version | DuckDB versions                                             |
|-----------------|-------------------------------------------------------------|
| 43              | v0.7.0                                                      |
| 42              | [#5544](https://github.com/duckdb/duckdb/pull/5544) onwards |
| 41              | [#5768](https://github.com/duckdb/duckdb/pull/5768) onwards |
| 40              | [#5491](https://github.com/duckdb/duckdb/pull/5491) onwards |
| 39              | v0.6.0, v0.6.1                                              |
| 38              | v0.5.0, v0.5.1                                              |
| 37              | [#3985](https://github.com/duckdb/duckdb/pull/3985) onwards |
| 36              | [#4022](https://github.com/duckdb/duckdb/pull/4022) onwards |
| 35              |                                                             |
| 34              |                                                             |
| 33              | v0.3.3, v0.3.4, v0.4.0                                      |
| 32              | [#3084](https://github.com/duckdb/duckdb/pull/3084)         |
| 31              | v0.3.2                                                      |
| 30              |                                                             |
| 29              |                                                             |
| 28              |                                                             |
| 27              | v0.3.1                                                      |
| 26              |                                                             |
| 25              | v0.3.0                                                      |
| 24              |                                                             |
| 23              |                                                             |
| 22              |                                                             |
| 21              | v0.2.9                                                      |
| 20              |                                                             |
| 19              |                                                             |
| 18              | v0.2.8                                                      |
| 17              | v0.2.7                                                      |
| 16              |                                                             |
| 15              | v0.2.6                                                      |
| 14              |                                                             |
| 13              | v0.2.5                                                      |
| 12              |                                                             |
| 11              | v0.2.4                                                      |
| 10              |                                                             |
| 9               |                                                             |
| 8               |                                                             |
| 7               |                                                             |
| 6               | v0.2.3                                                      |
| 5               |                                                             |
| 4               | v0.2.2                                                      |
| 3               |                                                             |
| 2               |                                                             |
| 1               | v0.2.1 and prior                                            |

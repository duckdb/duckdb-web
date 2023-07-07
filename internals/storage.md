---
layout: docu
title: Storage
expanded: Development
---

The DuckDB internal storage format is currently in flux, and is expected to change with each release until we reach v1.0.0.

## How to move between storage formats

When you update duckdb and open a database file, you might encounter an error message about incompatible storage formats, pointing to this page.
To move your database(s) to newer format you only need the older and the newer duckdb executable.

Opening your database file with the older duckdb and using the SQL statement `"EXPORT DATABASE 'tmp';"` allows you to save the whole state of the current database in use inside folder `tmp`.
`tmp` content will be overridden, so choose an empty/non yet existing folder.

Then starting the newer duckdb and execute `"IMPORT DATABASE 'tmp';"` (pointing to the previously populated folder) allows you to load the database, which can be then saved to the file you pointed duckdb to.

A bash two-liner (to be adapted with the right file names and executable locations) is:
```bash
$ /older/version/duckdb mydata.db -c "EXPORT DATABASE 'tmp';"
$ /newer/duckdb mydata.new.db -c "IMPORT DATABASE 'tmp';"
```

After this `mydata.db` will be untouched with the old format, `mydata.new.db` will contain the same data but in a format accessible from more recent duckdb, and folder `tmp` will old the same data in an universal format as different files.

Check [EXPORT documentation](../docs/sql/statements/export) for more details on the syntax.

## Storage header

DuckDB files start with a `uint64_t` which contains a checksum for the main header, followed by four magic bytes (`DUCK`), followed by the storage version number in a `uint64_t`.

```bash
$ hexdump -n 20 -C mydata.db
00000000  01 d0 e2 63 9c 13 39 3e  44 55 43 4b 2b 00 00 00  |...c..9>DUCK+...|
00000010  00 00 00 00                                       |....|
00000014
```

A simple example of reading the storage version using python is below.

```py
import struct

pattern = struct.Struct('<8x4sQ')

with open('test/sql/storage_version/storage_version.db', 'rb') as fh:
    print(pattern.unpack(fh.read(pattern.size)))
```

## Storage version table

For changes in each given release, check out the [changelog](https://github.com/duckdb/duckdb/releases) on GitHub.
To see the commits that changed each storage version, see the [commit log](https://github.com/duckdb/duckdb/commits/master/src/storage/storage_info.cpp)

| Storage version | DuckDB versions                                             |
|-----------------|-------------------------------------------------------------|
| 51              | v0.8.0                                                      |
| 50              | [#7270](https://github.com/duckdb/duckdb/pull/7270) onwards |
| 49              | [#6841](https://github.com/duckdb/duckdb/pull/6841) onwards |
| 48              | [#6715](https://github.com/duckdb/duckdb/pull/6715) onwards |
| 47              |                                                             |
| 46              | [#6621](https://github.com/duckdb/duckdb/pull/6621) onwards |
| 45              | [#6560](https://github.com/duckdb/duckdb/pull/6560) onwards |
| 44              | [#6499](https://github.com/duckdb/duckdb/pull/6499) onwards |
| 43              | v0.7.0, v0.7.1                                              |
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

---
layout: docu
title: Storage
---

## Compatibility

### Backward Compatibility

_Backward compatibility_ refers to the ability of a newer DuckDB version to read storage files created by an older DuckDB version. Version 0.10 is the first release of DuckDB that supports backward compatibility in the storage format. DuckDB v0.10 can read and operate on files created by the previous DuckDB version – DuckDB v0.9.

For future DuckDB versions, our goal is to ensure that any DuckDB version released **after** can read files created by previous versions, starting from this release. We want to ensure that the file format is fully backward compatible. This allows you to keep data stored in DuckDB files around and guarantees that you will be able to read the files without having to worry about which version the file was written with or having to convert files between versions.

### Forward Compatibility

_Forward compatibility_ refers to the ability of an older DuckDB version to read storage files produced by a newer DuckDB version. DuckDB v0.9 is [**partially** forward compatible with DuckDB v0.10](/2024/02/13/announcing-duckdb-0100#forward-compatibility). Certain files created by DuckDB v0.10 can be read by DuckDB v0.9.

Forward compatibility is provided on a **best effort** basis. While stability of the storage format is important – there are still many improvements and innovations that we want to make to the storage format in the future. As such, forward compatibility may be (partially) broken on occasion.

## How to Move Between Storage Formats

When you update DuckDB and open an old database file, you might encounter an error message about incompatible storage formats, pointing to this page.
To move your database(s) to newer format you only need the older and the newer DuckDB executable.

Open your database file with the older DuckDB and run the SQL statement `EXPORT DATABASE 'tmp'`. This allows you to save the whole state of the current database in use inside folder `tmp`.
The content of the `tmp` folder will be overridden, so choose an empty/non yet existing location. Then, start the newer DuckDB and execute `IMPORT DATABASE 'tmp'` (pointing to the previously populated folder) to load the database, which can be then saved to the file you pointed DuckDB to.

A bash two-liner (to be adapted with the file names and executable locations) is:

```bash
$ /older/version/duckdb mydata.db -c "EXPORT DATABASE 'tmp'"
$ /newer/duckdb mydata.new.db -c "IMPORT DATABASE 'tmp'"
```

After this `mydata.db` will be untouched with the old format, `mydata.new.db` will contain the same data but in a format accessible from more recent DuckDB, and folder `tmp` will old the same data in an universal format as different files.

Check [`EXPORT` documentation](../docs/sql/statements/export) for more details on the syntax.

## Storage Header

DuckDB files start with a `uint64_t` which contains a checksum for the main header, followed by four magic bytes (`DUCK`), followed by the storage version number in a `uint64_t`.

```bash
$ hexdump -n 20 -C mydata.db
00000000  01 d0 e2 63 9c 13 39 3e  44 55 43 4b 2b 00 00 00  |...c..9>DUCK+...|
00000010  00 00 00 00                                       |....|
00000014
```

A simple example of reading the storage version using Python is below.

```python
import struct

pattern = struct.Struct('<8x4sQ')

with open('test/sql/storage_version/storage_version.db', 'rb') as fh:
    print(pattern.unpack(fh.read(pattern.size)))
```

## Storage Version Table

For changes in each given release, check out the [change log](https://github.com/duckdb/duckdb/releases) on GitHub.
To see the commits that changed each storage version, see the [commit log](https://github.com/duckdb/duckdb/commits/main/src/storage/storage_info.cpp).

<div class="narrow_table"></div>

| Storage version | DuckDB version(s)               |
|----------------:|---------------------------------|
| 64              | v0.9.x, v0.10.x                 |
| 51              | v0.8.0, v0.8.1                  |
| 43              | v0.7.0, v0.7.1                  |
| 39              | v0.6.0, v0.6.1                  |
| 38              | v0.5.0, v0.5.1                  |
| 33              | v0.3.3, v0.3.4, v0.4.0          |
| 31              | v0.3.2                          |
| 27              | v0.3.1                          |
| 25              | v0.3.0                          |
| 21              | v0.2.9                          |
| 18              | v0.2.8                          |
| 17              | v0.2.7                          |
| 15              | v0.2.6                          |
| 13              | v0.2.5                          |
| 11              | v0.2.4                          |
| 6               | v0.2.3                          |
| 4               | v0.2.2                          |
| 1               | v0.2.1 and prior                |

## Compression

DuckDB uses [lightweight compression](/2022/10/28/lightweight-compression).
Note that compression is only applied to persistent databases and is **not applied to in-memory instances**.

### Compression Algorithms

The compression algorithms supported by DuckDB include the following:

* [Constant Encoding](/2022/10/28/lightweight-compression#constant-encoding)
* [Run-Length Encoding (RLE)](/2022/10/28/lightweight-compression#run-length-encoding-rle)
* [Bit Packing](/2022/10/28/lightweight-compression#bit-packing)
* [Frame of Reference (FOR)](/2022/10/28/lightweight-compression#frame-of-reference)
* [Dictionary Encoding](/2022/10/28/lightweight-compression#dictionary-encoding)
* [Fast Static Symbol Table (FSST)](/2022/10/28/lightweight-compression#fsst) – [VLDB 2020 paper](https://www.vldb.org/pvldb/vol13/p2649-boncz.pdf)
* [Adaptive Lossless Floating-Point Compression (ALP)](/2024/02/13/announcing-duckdb-0100#adaptive-lossless-floating-point-compression-alp) – [SIGMOD 2024 paper](https://ir.cwi.nl/pub/33334/33334.pdf)
* [Chimp](/2022/10/28/lightweight-compression#chimp--patas) – [VLDB 2022 paper](https://www.vldb.org/pvldb/vol15/p3058-liakos.pdf)
* [Patas](/2022/11/14/announcing-duckdb-060#compression-improvements)

## Disk Usage

The disk usage of DuckDB's format depends on a number of factors, including the data type and the data distribution, the compression methods used, etc.
As a rough approximation, loading 100 GB of uncompressed CSV files into a DuckDB database file will require 25 GB of disk space, while loading 100 GB of Parquet files will require 120 GB of disk space.

## Row Groups

DuckDB's storage format stores the data in _row groups,_ i.e., horizontal partitions of the data.
This concept is equivalent to [Parquet's row groups](https://parquet.apache.org/docs/concepts/).
Several features in DuckDB, including [parallelism](/docs/guides/performance/how_to_tune_workloads) and [compression](/2022/10/28/lightweight-compression) are based on row groups.

## Troubleshooting

### Error Message When Opening an Incompatible Database File

When opening a database file that has been written by a different DuckDB version from the one you are using, the following error message may occur:

```text
Error: unable to open database "...": Serialization Error: Failed to deserialize: ...
```

The message implies that the database file was created with a newer DuckDB version and uses features that are backward incompatible with the DuckDB version used to read the file.

There are two potential workarounds:

1. Update your DuckDB version to the latest stable version.
2. Open the database with the latest version of DuckDB, export it to a standard format (e.g., Parquet), then import it using to any version of DuckDB. See the [`EXPORT/IMPORT DATABASE` statements](../docs/sql/statements/export) for details.

---
layout: docu
title: Parquet Encryption
---

Starting with version 0.10.0, DuckDB supports reading and writing encrypted Parquet files.
DuckDB broadly follows the [Parquet Modular Encryption specification](https://github.com/apache/parquet-format/blob/master/Encryption.md) with some [limitations](#limitations).

## Reading and Writing Encrypted Files

Using the `PRAGMA add_parquet_key` function, named encryption keys of 128, 192, or 256 bits can be added to a session. These keys are stored in-memory.

```sql
PRAGMA add_parquet_key('key128', '0123456789112345');
PRAGMA add_parquet_key('key192', '012345678911234501234567');
PRAGMA add_parquet_key('key256', '01234567891123450123456789112345');
```

### Writing Encrypted Parquet Files

After specifying the key (e.g., `key256`), files can be encrypted as follows:

```sql
COPY tbl TO 'tbl.parquet' (ENCRYPTION_CONFIG {footer_key: 'key256'});
```

### Reading Encrpyted Parquet Files

An encrypted Parquet file using a specific key (e.g., `key256`), can then be read as follows:

```sql
COPY tbl FROM 'tbl.parquet' (ENCRYPTION_CONFIG {footer_key: 'key256'});
```

Or:

```sql
SELECT *
FROM read_parquet('tbl.parquet', encryption_config = {footer_key: 'key256'});
```

## Limitations

DuckDB's Parquet encryption currently has the following limitations.

1. It is not compatible with the encryption of, e.g., PyArrow, until the missing details are implemented.

2. DuckDB encrypts the footer and all columns using the `footer_key`. The Parquet specification allows encryption of individual columns with different keys, e.g.:

    ```sql
    COPY tbl TO 'tbl.parquet'
        (ENCRYPTION_CONFIG {
            footer_key: 'key256',
            column_keys: {key256: ['col0', 'col1']}
        });
    ```

    However, this is unsupported at the moment and will cause an error to be thrown (for now):

    ```text
    Not implemented Error: Parquet encryption_config column_keys not yet implemented
    ```

## Performance Implications

Note that encryption has some performance implications.
Without encryption, reading/writing the `lineitem` table from [`TPC-H`](../../extensions/tpch) at SF1, which is 6M rows and 15 columns, from/to a Parquet file takes 0.26 and 0.99 seconds, respectively.
With encryption, this takes 0.64  and 2.21 seconds, both approximately 2.5× slower than the unencrypted version.

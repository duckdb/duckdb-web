---
layout: docu
title: Lakehouse Formats
---

Lakehouse formats, often referred to as open table formats, are specifications for storing data in object storage while maintaining some guarantees such as ACID transactions or keeping snapshot history. Over time, multiple lakehouse formats have emerged, each one with its own unique approach to managing its metadata (a.k.a. catalog). In this page, we will go over the support that DuckDB offers for some of these formats as well as some workarounds that you can use to still use DuckDB and get close to full interoperability with these formats.

## DuckDB Lakehouse Support Matrix

DuckDB supports Iceberg, Delta and DuckLake as first-class citizens. The following matrix represents what DuckDB natively supports out of the box through core extensions.

|                              | DuckLake                                                              | Iceberg                                                                 | Delta                                                      |
| ---------------------------- | :-------------------------------------------------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------- |
| Extension                    | [`ducklake`](https://ducklake.select/docs/stable/duckdb/introduction) | [`iceberg`]({% link docs/preview/core_extensions/iceberg/overview.md %}) | [`delta`]({% link docs/preview/core_extensions/delta.md %}) |
| Read                         | ✅                                                                    | ✅                                                                      | ✅                                                         |
| Write                        | ✅                                                                    | ✅                                                                      | ✅                                                         |
| Deletes                      | ✅                                                                    | ✅                                                                      | ❌                                                         |
| Updates                      | ✅                                                                    | ✅                                                                      | ❌                                                         |
| Upserting                    | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Create table                 | ✅                                                                    | ✅                                                                      | ❌                                                         |
| Create table with partitions | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Attaching to a catalog       | ✅                                                                    | ✅                                                                      | ✅ \*                                                     |
| Rename table                 | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Rename columns               | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Add/drop columns             | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Alter column type            | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Compaction and maintenance   | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Encryption                   | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Manage table properties      | ✅                                                                    | ❌                                                                      | ❌                                                         |
| Time travel                  | ✅                                                                    | ✅                                                                      | ✅                                                         |
| Query table changes          | ✅                                                                    | ❌                                                                      | ❌                                                         |

\* Through the [`unity_catalog`](https://github.com/duckdb/unity_catalog) extension.

DuckDB aims to build native extensions with minimal dependencies. The `iceberg` extension for example, has no dependencies on third-party Iceberg libraries, which means all data and metadata operations are implemented natively in the DuckDB extension. For the `delta` extension, we use the [`delta-kernel-rs` project](https://github.com/delta-io/delta-kernel-rs), which is meant to be a lightweight platform for engines to build delta integrations that are as close to native as possible.

> **Why do native implementations matter?** Native implementations allow DuckDB to do more performance optimizations such as complex filter pushdowns (with file-level and row-group level pruning) and improve memory management.

## Workarounds for Unsupported Features

If the DuckDB core extension does not cover your use case, you can still use DuckDB to process the data and use an external library to help you with the unsupported operations. If you are using the Python client, there are some very good off-the-shelf libraries that can help you. These examples will have one thing in common, they use Arrow as an efficient, zero-copy data interface with DuckDB.

### Using PyIceberg with DuckDB

In this example, we will use [PyIceberg](https://py.iceberg.apache.org/) to create and alter the schema of a table and DuckDB to read and write to the table.

<!-- markdownlint-disable MD040 MD046 -->

<details markdown='1'>
<summary markdown='span'>
Click here to see the full example.
</summary>

```python
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import (
    TimestampType,
    FloatType,
    DoubleType,
    StringType,
    NestedField,
)
import duckdb

# Create a table with PyIceberg
catalog = load_catalog(
    "docs",
    **{
        "uri": "http://127.0.0.1:8181",
        "s3.endpoint": "http://127.0.0.1:9000",
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": "admin",
        "s3.secret-access-key": "password",
    }
)
schema = Schema(
    NestedField(field_id=1, name="datetime", field_type=TimestampType(), required=True),
    NestedField(field_id=2, name="symbol", field_type=StringType(), required=True),
    NestedField(field_id=3, name="bid", field_type=FloatType(), required=False),
    NestedField(field_id=4, name="ask", field_type=DoubleType(), required=False)
)
catalog.create_table(
    identifier="default.bids",
    schema=schema,
    partition_spec=partition_spec,
)

# Write and read the table with DuckDB
with duckdb.connect() as conn:
    conn.execute("""
        CREATE SECRET (
            TYPE S3,
            KEY_ID 'admin',
            SECRET 'password',
            ENDPOINT '127.0.0.1:9000',
            URL_STYLE 'path',
            USE_SSL false
        );
        ATTACH '' AS my_datalake (
            TYPE ICEBERG,
            CLIENT_ID 'admin',
            CLIENT_SECRET 'password',
            ENDPOINT 'http://127.0.0.1:8181'
        );
    """)
    conn.execute("""
        INSERT INTO my_datalake.default.bids VALUES ('2024-01-01 10:00:00', 'AAPL', 150.0, 150.5);
    """)
    conn.sql("SELECT * FROM my_datalake.default.bids;").show()

# Alter schema with PyIceberg
table = catalog.load_table("default.bids")
with table.update_schema() as update:
    update.add_column("retries", IntegerType(), "Number of retries to place the bid")
```

</details>

<!-- markdownlint-enable MD040 MD046 -->

### Using delta-rs with DuckDB

In this example, we create a Delta table with the `delta-rs` Python binding, then we use the `delta` extension of DuckDB to read it. We also showcase how to do other read operations with DuckDB, like reading the change data feed using the Arrow zero-copy integration. This operation can also be lazy if reading bigger data by using [Arrow Datasets](https://delta-io.github.io/delta-rs/integrations/delta-lake-arrow/).

<!-- markdownlint-disable MD040 MD046 -->

<details markdown='1'>
<summary markdown='span'>
Click here to see the full example.
</summary>

```python
import deltalake as dl
import pyarrow as pa

# Create a delta table and read it with DuckDB Delta extension
dl.write_deltalake(
    "tmp/some_table",
    pa.table({
        "id": [1, 2, 3],
        "value": ["a", "b", "c"]
    })
)
with duckdb.connect() as conn:
    conn.execute("""
        INSTALL delta;
        LOAD delta;
    """)
    conn.sql("""
        SELECT * FROM delta_scan('tmp/some_table')
    """).show()

# Append some data and read the data change feed using the PyArrow integration
dl.write_deltalake(
    "tmp/some_table",
    pa.table({
        "id": [4, 5],
        "value": ["d", "e"]
    }),
    mode="append"
)
table = dl.DeltaTable("tmp/some_table").load_cdf(starting_version=1, ending_version=2)
with duckdb.connect() as conn:
    conn.register("t", table)
    conn.sql("SELECT * FROM t").show()
```

</details>

<!-- markdownlint-enable MD040 MD046 -->

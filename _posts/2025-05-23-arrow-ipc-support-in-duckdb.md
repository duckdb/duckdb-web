---
layout: post
title: "Arrow IPC Support in DuckDB"
author: "Pedro Holanda (DuckDB Labs), Ian Cook (Columnar), Dewey Dunnington (Wherobots), Bryce Mecum (Voltron Data)"
thumb: "/images/blog/thumbs/duckdb-arrow.svg"
image: "/images/blog/thumbs/duckdb-arrow.png"
excerpt: "DuckDB now supports consuming and producing the Arrow IPC Serialization Format through the `arrow` community extension."
tags: ["extensions"]
---

## DuckDB and Arrow

In recent years, the [Apache Arrow project](https://arrow.apache.org/docs/) has gained a lot of traction in the data world, thanks to its columnar format that allows for easy interchange of data between different systems – mostly with a zero-copy approach.
Apache Arrow powers, among others, the integration between DuckDB and Polars.
In practice, when DuckDB produces or consumes a Polars DataFrame, it is actually using the [Arrow columnar format](https://arrow.apache.org/docs/format/Columnar.html) underneath.

The importance of having such a format is also one of the main reasons DuckDB was among the pioneers in [integrating with Arrow]({% post_url 2021-12-03-duck-arrow %}) and implementing an [Arrow Database Connectivity (ADBC)](https://arrow.apache.org/adbc/) [interface]({% link docs/stable/clients/adbc.md %}) – particularly because Arrow makes this possible with no additional dependencies, thanks to its [C data interface](https://arrow.apache.org/docs/format/CDataInterface.html).

But one limitation of Arrow's C data interface is that it exchanges data using pointers (memory addresses). This limits the possibilities if you want to exchange Arrow data between different processes or systems. To overcome this limitation, the Arrow project also specifies the [Arrow IPC format](https://arrow.apache.org/docs/format/Columnar.html#format-ipc), which allows users to efficiently serialize Arrow columnar data and pass it between processes or over a network. This data can be consumed as a stream, either directly from a memory buffer or from a file.

We're thrilled to announce that DuckDB is now able to consume and produce these Arrow streams via the new [`arrow` community extension]({% link community_extensions/extensions/arrow.md %}). In this post, we will describe the Arrow IPC serialization format in more detail, show how to install the new `arrow` community extension for DuckDB, and give a demo showing how to use it.

## Arrow Interprocess Communication (Arrow IPC)

The Arrow IPC format provides a way of serializing (and optionally compressing) Arrow-formatted data, enabling you to transfer data over a network or store it on disk while keeping it in Arrow format, avoiding the overhead of converting it to a different format. Arrow IPC supports LZ4 and ZSTD compression, and when stored as a file, it also supports a file footer that can be used to speed up retrieval and processing by allowing parts of the data to be skipped (similar to the approach used by the Parquet format). When compared to Parquet, the Arrow IPC format has two main benefits:

1. **Ease of implementation:** Writing a low-level Arrow IPC consumer/producer is less complex than writing a Parquet one, especially if the system already integrates with the Arrow format.
2. **Faster encoding and decoding:** The process of encoding and decoding (serializing and deserializing) Arrow data is much simpler and faster than with Parquet. This can yield faster processing times—especially if you are streaming data that does not need to be stored on disk afterwards.

Arrow and Parquet are complementary formats. Parquet's sophisticated system of encoding and compression options typically yields much smaller files, making Parquet a better choice for archival storage. Arrow's ability to eliminate encoding and decoding overheads typically yields faster and more efficient data interchange, making Arrow a better choice for query result transfer and ephemeral caching.

To give you an illustration of just how simple the Arrow IPC format is, consider the following illustration. In the Arrow IPC format, a table is serialized as a sequence of record batches (a collection of records organized in a columnar layout), preceded by their shared schema:

![An illustration of an Arrow IPC stream transmitting data from a table with three columns. The first record batch contains the values for the first three rows, the second record batch contains the values for the next three rows, and so on. Actual Arrow record batches might contain thousands to millions of rows.](/images/blog/arrow_ipc_fig1.png)

*Figure from [Apache Arrow Blog: How the Apache Arrow Format Accelerates Query Result Transfer](https://arrow.apache.org/blog/2025/01/10/arrow-result-transfer).*

Note that in realistic scenarios, record batches are much larger and the figure above is simplified for illustrative purposes.

## The Arrow Community Extension

DuckDB has included an integration with the Arrow IPC format for many years, via the [(now-deprecated) Arrow core extension](https://github.com/duckdb/arrow). However, the main purpose of this support was to allow DuckDB interoperability with JavaScript, hence it was designed only to read in-memory serialized buffers, and not Arrow IPC files. The extension's code complexity and maintainability were very high, because working with Arrow IPC required having the entire Arrow C++ library as a dependency, as we did not want to write our own serialization and deserialization code for the Arrow IPC format.

More recently, a much smaller Arrow C++ implementation started to gain popularity as a way to interact with Arrow IPC data: the [nanoarrow library](https://arrow.apache.org/nanoarrow/). Using nanoarrow, we completely redesigned the old DuckDB Arrow extension to have a much smaller dependency, a cleaner codebase, and the ability to scan Arrow IPC files. We also took the opportunity to shift the Arrow DuckDB extension from a core extension to a community extension. This change was made for two main reasons. The first is to enable the Arrow developer and user community to be more involved in building and supporting the extension. The second is to have a release schedule that is not tied to the DuckDB release schedule. In practice, this means that members of the core Arrow developer community can decide when a new version of the extension will be released.

Installing and loading the new Arrow extension is very simple:

```sql
INSTALL arrow FROM community;
LOAD arrow;
```

## Demo

In this demo, we will use the new Arrow DuckDB extension to generate the `lineitem` TPC-H table with scale factor 10 as an Arrow IPC file. While our demo will focus on Arrow IPC data stored in a file, the extension itself also allows you to consume and produce the Arrow IPC format directly as buffers. You can find detailed examples of usage and accepted parameters in the extension's [README](https://github.com/paleolimbot/duckdb-nanoarrow/blob/main/README.md).

We start off by loading the `arrow` extension and generating our TPC-H tables.

```sql
LOAD arrow;

CALL dbgen(sf = 10);
```

To generate the Arrow IPC files we can simply use the `COPY ... TO ...` clause, as follows. We use the [recommended file extension `.arrows`](https://arrow.apache.org/faq/#mime-types-iana-media-types-for-arrow-data) since this file is in the Arrow IPC stream format.

```sql
COPY lineitem TO 'lineitem.arrows';
```

> In this demo, for simplicity, we wrote our table in a single file. However, our Arrow `COPY ... TO ...` clause allows us to set the `chunk_size` and the number of `row_groups` per file. These options allow us to produce data optimized for the best possible performance for your use case. For example, a smaller `chunk_size` may reduce overall performance but benefit streaming scenarios.

We can now run TPC-H query 6 directly on our file using the `read_arrow` function:

```sql
SELECT
    sum(l_extendedprice * l_discount) AS revenue
FROM
    read_arrow('lineitem.arrows')
WHERE
    l_shipdate >= CAST('1994-01-01' AS date)
    AND l_shipdate < CAST('1995-01-01' AS date)
    AND l_discount BETWEEN 0.05
    AND 0.07
    AND l_quantity < 24;
```

which prints:

```text
┌─────────────────┐
│     revenue     │
│  decimal(38,4)  │
├─────────────────┤
│ 1230113636.0101 │
│ (1.23 billion)  │
└─────────────────┘
```

Thanks to [replacement scans]({% link docs/preview/sql/dialect/friendly_sql.md %}#data-import), you can omit the function `read_arrow` if the filename ends with `.arrow` or `.arrows`. For example:

```sql
SELECT count(*) FROM 'lineitem.arrows';
```

which prints:

```text
┌─────────────────┐
│  count_star()   │
│      int64      │
├─────────────────┤
│    59986052     │
│ (59.99 million) │
└─────────────────┘
```

> For simplicity, we focus on the scenario of reading a single file, but our reader supports multi-file reading, with functionality on par with the DuckDB Parquet reader.

What if you want to fetch an Arrow IPC stream directly from a server into DuckDB? To demonstrate this, we can start an HTTP file server in the same directory where we saved `lineitem.arrows`. We use the Node.js package [serve](https://www.npmjs.com/package/serve) to do this (instead of Python's built-in `http.server`) because it supports [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests):

```batch
npx serve -l 8008
```

Then you can use [DuckDB's `httpfs` extension]({% link docs/stable/core_extensions/httpfs/https.md %}) to query the Arrow data over the HTTP(S) protocol:

```sql
INSTALL httpfs;
LOAD httpfs;
LOAD arrow;

SELECT count(*) FROM read_arrow('http://localhost:8008/lineitem.arrows');
```

which prints the same result:

```text
┌─────────────────┐
│  count_star()   │
│      int64      │
├─────────────────┤
│    59986052     │
│ (59.99 million) │
└─────────────────┘
```

Alternatively, you can use a tool like `curl` to fetch Arrow IPC data from a server and pipe it to DuckDB in the terminal:

```batch
URL="http://localhost:8008/lineitem.arrows"
SQL="LOAD arrow; FROM read_arrow('/dev/stdin') SELECT count(*);"

curl -s "$URL" | duckdb -c "$SQL"
```

which prints the same result. For other demos of the `arrow` extension, see our [arrow-ipc demo](https://github.com/pdet/arrow-ipc-demo) repository.

## Bonus: Cool Use Cases for Arrow IPC

Running a DuckDB query against data in Arrow IPC format like in the demo above is a pretty neat trick, and it works so well because DuckDB and Arrow are a natural pair due to both using a columnar data layout. However, you may be wondering what else you can do with Arrow IPC data. One of Arrow's main goals is interoperability, and by saving our data in Arrow IPC format, we've opened up many options for connecting with other tools.

For example, we can now work with our data with [PyArrow](https://arrow.apache.org/docs/python/):

```python
import pyarrow as pa

with open('lineitem.arrows', 'rb') as source:
   stream = pa.ipc.open_stream(source)
   tbl = stream.read_all()
```

or [Polars](https://pola.rs):

```python
import polars as pl

tbl = pl.read_ipc_stream("lineitem.arrows")
```

or [ClickHouse](https://clickhouse.com):

```sql
CREATE TABLE
    lineitem
ENGINE MergeTree()
ORDER BY tuple()
AS
    SELECT * FROM file('lineitem.arrows', 'ArrowStream');
```

or any of the numerous other Arrow libraries (available in a dozen different languages) or Arrow-compatible systems.

The benefits of Arrow IPC don't stop there: Arrow IPC is also ideal for larger-than-memory use cases. Using [PyArrow](https://arrow.apache.org/docs/python/), we can [memory-map](https://en.wikipedia.org/wiki/Memory-mapped_file) our `lineitem.arrows` file and work with it without reading the entire thing into memory:

```python
import pyarrow as pa

with pa.memory_map('lineitem.arrows', 'rb') as source:
    stream = pa.ipc.open_stream(source)
    tbl = stream.read_all()

tbl.num_rows
# => 59986052
```

Then, we can check that PyArrow didn't have to allocate any buffers to hold the data because it all lives on disk:

```python
pa.total_allocated_bytes()
# => 0
```

Now we can perform the same query we did in the demo above and show we get the same result:

```python
import datetime
import pyarrow.compute as pc

subset = tbl.filter(
    (pc.field("l_shipdate") >= datetime.datetime(1994, 1, 1)) &
    (pc.field("l_shipdate") < datetime.datetime(1995, 1, 1)) &
    (pc.field("l_discount") >= 0.05) &
    (pc.field("l_discount") <= 0.07) &
    (pc.field("l_quantity") < 24.)
)
pc.sum(pc.multiply(subset.column("l_extendedprice"), subset.column("l_discount")))
# => <pyarrow.Decimal128Scalar: Decimal('1230113636.0101')>
```

And, despite `lineitem.arrows` being over 10 GB, PyArrow only had to allocate a fraction of the memory:

```python
pa.total_allocated_bytes()
# => 201594240 (192MB)
```

## Conclusion & What's Next

In this blog post, we presented the new Arrow community extension, which enables DuckDB users to interact with Arrow IPC streaming buffers and files. 
Special thanks to [Voltron Data](https://voltrondata.com/) for enabling this extension by working with [DuckDB Labs](https://duckdblabs.com/).
Below we list our future plans for this extension:

* Support for both `ZSTD` and `LZ4` compression when writing Arrow IPC. DuckDB currently only supports writing uncompressed buffers.
* Support for `LZ4` compression when reading Arrow buffers. The reader currently only supports `ZSTD` or uncompressed buffers.
* Support for writing the Arrow IPC file format containing the file footer, and using the footer to speed up reads.
* Implementation of C API DuckDB functions to produce and consume Arrow IPC data.

If you'd like to work on any of these planned features or suggest other features, or if you find any bugs, feel free to log them in our [issue tracker](https://github.com/paleolimbot/duckdb-nanoarrow/issues). Happy hacking!

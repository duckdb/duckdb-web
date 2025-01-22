---
layout: post
title: "Query Engines: Gatekeepers of the Parquet File Format"
author: "Laurens Kuiper"
thumb: "/images/blog/thumbs/parquet-encodings.svg"
image: "/images/blog/thumbs/parquet-encodings.png"
excerpt: "Mainstream query engines do not support reading newer Parquet encodings, forcing systems like DuckDB to default to writing older encodings, thereby sacrificing compression."
tags: ["parquet"]
---

## The Apache® Parquet™ Format

Apache Parquet is a popular, free, open-source, column-oriented data storage format.
Whereas database systems typically load data from formats such as CSV and JSON into database tables before analyzing them, Parquet is designed to be efficiently queried directly.
Parquet considers that users often only want to read some of the data, not all of it.
To accommodate this, Parquet is designed to read individual columns instead of always having to read all of them.
Furthermore, statistics can be used to filter out parts of files without fully reading them (this is also referred to as [zone maps](https://www.vldb.org/conf/1998/p476.pdf)).
Furthermore, storing data in Parquet typically results in a much smaller file than CSV or JSON due to a combination of [lightweight columnar compression](https://ir.cwi.nl/pub/15564/15564B.pdf) and general-purpose compression.

Many query engines implement reading and writing Parquet files.
Therefore, it is also useful as a _data interchange_ format.
For example, Parquet files written by Spark in a large distributed data pipeline can later be analyzed using DuckDB.
Because so many systems can read and write Parquet, it is the data format of choice for data lake solutions like [Delta Lake™](https://delta.io) and [Iceberg™](https://iceberg.apache.org).
While Parquet certainly has flaws, which [researchers](https://github.com/cwida/FastLanes) and [companies](https://github.com/facebookincubator/nimble) are trying to address with new data formats, like it or not, it seems like Parquet is here to stay, at least for a while.

So, while we're here, we might try to make the best of it, right?
SQL also has its flaws, and while researchers have certainly tried to create [different query languages](https://en.wikipedia.org/wiki/QUEL_query_languages), we're still stuck with SQL.
DuckDB embraces this and tries to [make]({% post_url 2022-05-04-friendlier-sql %}) the [best]({% post_url 2023-08-23-even-friendlier-sql %}) of [it]({% post_url 2024-03-01-sql-gymnastics %}).
The Parquet developers are doing the same for their format by updating it occasionally, bringing [new features](https://github.com/apache/parquet-format/blob/master/CHANGES.md) that make the format better.

## Updates

If DuckDB adds a new compression method to its internal file format in a release, all subsequent releases must be able to read it.
Otherwise, you couldn't read a database file created by DuckDB 1.1.0 after updating it to 1.2.0.
This is called _backward compatibility_, and it can be challenging for developers.
It sometimes requires holding onto legacy code and creating conversions from old to new.
It is important to keep supporting older formats because updating DuckDB is much easier than rewriting entire database files.

Backward compatibility is also valuable for Parquet: it should be possible to read a Parquet file written years ago today.
Luckily, most mainstream query engines can still read files in the Parquet 1.0 format, which was released in 2013, over ten years ago.
Updates to the format do not threaten backward compatibility, as query engines simply need to continue being able to read the old files.
However, it is also important that query engines add support for _reading_ newer files alongside the older ones so that we can start _writing_ new and improved Parquet files as well.

Here's where it gets tricky.
We cannot expect query engines to be able to read the bleeding-edge Parquet format _tomorrow_ if Parquet developers roll out an update _today_.
We cannot start writing the new format for some time because many query engines will not be able to read it.
The [robustness principle](https://en.wikipedia.org/wiki/Robustness_principle) states, “Be conservative in what you send, be liberal in what you accept.”
If we apply this to Parquet files, query engines should strive to read new Parquet files but not write them yet, at least by default.

## Encodings

DuckDB really likes [lightweight compression]({% post_url 2022-10-28-lightweight-compression %}).
So, for the upcoming DuckDB 1.2.0 version, we're excited to have implemented the `DELTA_BINARY_PACKED`, `DELTA_LENGTH_BYTE_ARRAY` (added in Parquet 2.2.0 in 2015), and `BYTE_STREAM_SPLIT` (added in Parquet 2.8.0 in 2019) encodings in our Parquet writer.
DuckDB, initially created in 2018, has been able to read Parquet since [2020](https://github.com/duckdb/duckdb/pull/556), and has been able to read the encodings `DELTA_BINARY_PACKED` and `DELTA_LENGTH_BYTE_ARRAY` since [2022](https://github.com/duckdb/duckdb/pull/5457), and `BYTE_STREAM_SPLIT` since [2023](https://github.com/duckdb/duckdb/pull/9240).

However, despite these new encodings being available in 1.2.0, DuckDB will not write them by default.
If DuckDB did this, many of our users would have a frustrating experience because some mainstream query engines still do not support reading these encodings.
Having a good compression ratio does not help users if their downstream application cannot read the file.
Therefore, we had to disable writing these encodings by default.
They are only used when setting `PARQUET_VERSION V2` in a `COPY` command.

> DuckDB versions as old as 0.9.1 (released in late 2023) can already read files serialized with the setting `PARQUET_VERSION V2`.

Compressing data is almost always a trade-off between file size and the time it takes to write.
Let's take a look at the following example (ran on a MacBook Pro with an M1 Max):

```sql
-- Generate TPC-H scale factor 1
INSTALL tpch;
LOAD tpch;
CALL dbgen(sf = 1);

-- Export to Parquet using Snappy compression
COPY lineitem TO 'snappy_v1.parquet'
    (COMPRESSION snappy, PARQUET_VERSION V1); -- 244 MB, ~0.46s
COPY lineitem TO 'snappy_v2.parquet'
    (COMPRESSION snappy, PARQUET_VERSION V2); -- 170 MB, ~0.39s

-- Export to Parquet using zstd compression
COPY lineitem TO 'zstd_v1.parquet'
    (COMPRESSION zstd, PARQUET_VERSION V1); -- 152 MB, ~0.58s
COPY lineitem TO 'zstd_v2.parquet'
    (COMPRESSION zstd, PARQUET_VERSION V2); -- 135 MB, ~0.44s
```

When using [Snappy](https://github.com/google/snappy), DuckDB's default page compression algorithm for Parquet, which focuses mostly on speed, not compression ratio, the file is ~30% smaller and writing is ~15% faster with the encodings enabled.
When using [zstd](https://github.com/facebook/zstd), which focuses more on compression ratio than speed, the file is ~11% smaller, and writing is ~24% faster with the encodings enabled.

The compression ratio highly depends on how well data can be compressed.
Here are some more extreme examples:

```sql
CREATE TABLE range AS FROM range(1e9::BIGINT);
COPY range TO 'v1.parquet' (PARQUET_VERSION V1); -- 3.7 GB, ~2.96s
COPY range TO 'v2.parquet' (PARQUET_VERSION V2); -- 1.3 MB, ~1.68s
```

The integer sequence 0, 1, 2, ... compresses extremely well with `DELTA_BINARY_PACKED`.
In this case, the file is ~99% smaller, and writing is almost twice as fast.

[Compressing floating points is much more difficult](https://github.com/cwida/ALP).
Nonetheless, if there is a pattern, the data will compress quite well:

```sql
CREATE TABLE range AS SELECT range / 1e9 FROM range(1e9::BIGINT);
COPY range TO 'v1.parquet' (PARQUET_VERSION V1); -- 6.3 GB, ~3.83s
COPY range TO 'v2.parquet' (PARQUET_VERSION V2); -- 610 MB, ~2.63s
```

This sequence compresses really well with `BYTE_STREAM_SPLIT`.
It is ~90% smaller and writes ~31% faster.
Real-world data often does not have such extremely compressible patterns.
Still, there are patterns, nonetheless, which will be exploited by these encodings.

If the query engines you're using support reading them, you can start using these encodings once DuckDB 1.2.0 is released!

## Wasted Bits

Although it's difficult to get exact numbers, it's safe to assume that many TBs of data are written in Parquet each day.
A large chunk of the bits written are wasted because query engines haven't implemented these newer encodings.
The solution to this is surprisingly easy.
There's no need to invent anything new to stop wasting all that space.
Just [read the specification on Parquet encodings](https://parquet.apache.org/docs/file-format/data-pages/encodings/), and implement them.
Some of these "newer" encodings are almost 10 years old by now!

By reducing the size of Parquet files, we can reduce the amount of data we store in data centers.
Reducing the amount of data we store even a little bit can have a big impact, as it can eventually reduce the need to build new data centers.
This is not to say that data centers are evil; we will certainly need more of them in the future.
However, making the most out of the data centers that we already have wouldn't hurt anyone.

## Conclusion

Parquet is currently the industry standard tabular data format.
Because it is also used as a data interchange format, the effectiveness of Parquet's features depends on the query engines that use it.
If _some_ of the mainstream query engines (you know who you are) refuse to implement these features, we _all_ lose.
This is not to say that all query engines must be on Parquet's bleeding edge, and DuckDB certainly isn't.
However, query engine developers have a shared responsibility to make Parquet more useful.

We hope that more query engines will implement these newer encodings.
Then, more query engines can write them by default and stop wasting so many bits.

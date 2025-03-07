---
layout: post
title: "Parquet Bloom Filters in DuckDB"
author: "Hannes Mühleisen"
thumb: "/images/blog/thumbs/bloom-filters.svg"
image: "/images/blog/thumbs/bloom-filters.png"
excerpt: "DuckDB now supports reading and writing Parquet Bloom filters."
tags: ["deep dive"]
---

One of the key features of the Parquet file format is the ability for readers to *selectively* read only the data that is relevant to a particular query. To support this, Parquet files contain column *statistics*, most notably the minimum and maximum value for each column in each row group. If a query is filtering with a particular value, and the data is – as it is often – somewhat sorted, a reader can “prove” that a particular row group cannot contain values relevant to the query. DuckDB heavily leverages this, and is able to – even when querying remote endpoints – selectively only read the parts of a Parquet file relevant to a query. For details on how this works, see our by now ancient blog post [“Querying Parquet with precision using DuckDB”]({% post_url 2021-06-25-querying-parquet %}).

However, there are some limitation to this approach. What if a column's data is randomly shuffled? In that case, all values occur in all row groups and the minimum and maximum statistics are less useful because we can only exclude values that are outside the minimum and maximum *of the entire column*. Parquet will use [dictionary encoding](https://parquet.apache.org/docs/file-format/data-pages/encodings/) if there are not too many distinct values in the column. In theory, that dictionary could be used to eliminate row groups but there are two problems with this approach: Parquet (inexplicably) allows *switching* from dictionary to plain encoding *halfway through a row group*. If the dictionary alone were used to eliminate the row group, but the plain part contained the queried value, this would lead to incorrect results. Furthermore, the dictionary is part of the actual column data. If we're reading the column data just to look at the dictionary we have already incurred most of the cost of reading the column in the first place.

Obscure sidenote: Again, in theory the column metadata contains the list of encodings that occur in that column. *If* that list is correct and does *not* include the plain encoding the dictionary *could* – again, in theory – be used for slightly earlier row group elimination. But the usefulness of this approach is more than dubious.

## Parquet Bloom Filters

The good people over at the [Parquet PMC](https://projects.apache.org/committee.html?parquet) have recognized that there is room for improvement here and added [Bloom filters](https://github.com/apache/parquet-format/blob/master/BloomFilter.md) for Parquet back in 2018. In a nutshell, [Bloom filters](https://en.wikipedia.org/wiki/Bloom_filter) are compact but approximate index structures for a set of values. For a given value, they can either say with certainty that a value is *not* in the set or that it *may be* in the set, with a false positive ratio depending on the size of the Bloom filter and the amount of distinct values added to it. For now, we can just treat a Bloom filter like an opaque series of bytes with magic properties.

When used, Parquet files can contain a Bloom filter for each column in each row group. Each Bloom filter can be at an arbitrary location in the file (`bloom_filter_offset`). At the offset in the file, we find another Thrift-encoded structure, the `BloomFilterHeader`. This structure has a field for the length of the filter, and some algorithmic settings which are currently redundant because there is only one valid setting for all of them. But decode the header you must to find out where the header ends and where the filter bytes begin. Finally, we have arrived at the precious magic bytes of the Bloom filter. We can now test the filter against any query predicates and see if we can skip the row group entirely.

More obscure sidenotes: while the column metadata *does* contain a field to store the size of the filter (`bloom_filter_length`) it is also optional and some writers (looking at you, Spark) annoyingly only set the offset, not the length. Also, the specification describes two possible filter locations. By also not requiring a length in the metadata, this makes it difficult slash impossible to read all Bloom filters for a Parquet file in a single range request. It is also not clear why the Bloom filters needed to *each* be prefixed with a Thrift metadata blob, when this information could also be contained in the ColumnMetaData. Or perhaps, god forbid, the filters could have become part of the main Parquet metadata itself. In the end we end up with a lot of additional reads to find and read the Bloom filter bytes, in principle requiring a careful trade-off between reading the filters and “just” reading the column brute-force.

## DuckDB Bloom Filters

As of the last feature release (1.2.0), DuckDB supports *both reading and writing* of Parquet Bloom filters. This happens completely transparently to users, no additional action or configuration is required.

### Writing

Currently, Bloom filters are supported for the following types:

* Integer types (`TINYINT`, `UTINYINT`, `SMALLINT`, `USMALLINT`, `INTEGER`, `UINTEGER`, `BIGINT`, `UBIGINT`)
* Floating point types (`FLOAT`, `DOUBLE`)
* String types (`VARCHAR` and `BLOB`)

Nested types (lists, structs, arrays) are currently *not* supported, but they might be added in a future release. In general, Bloom filters will be written if DuckDB decides to use dictionary encoding for a particular column (chunk) within the row group. There is a `COPY` parameter that controls the maximum dictionary size (`DICTIONARY_SIZE_LIMIT`), but this parameter is by default set to 10% of the row group size (`ROW_GROUP_SIZE`), which is 122,880 rows by default. Those values have been found to be reasonable first approximations for most use cases but users are of course encouraged to experiment with both parameters if they encounter performance issues. As the number of distinct values in a Bloom filter grows, its size needs to be improved to maintain a certain false positive ratio. By default, filters size is chosen using an 
“acceptable” false positive ratio of 1% or 0.01. The new `BLOOM_FILTER_FALSE_POSITIVE_RATIO` `COPY` parameter controls the acceptable ratio. In general, false positive hurt more the slower the read path is.

### Reading

During reading, DuckDB will automatically use constant-comparison filter predicates in the query (e.g., `WHERE a = 42`) to probe the Bloom filter (if present) and skip row groups where the Bloom filter can guarantee there are no matching rows in the group. Again, this happens transparently to users and there is no configuration that needs to be set. 

Users can find out if a given Parquet file contains Bloom filters: the `parquet_metadata` function was extended with two new columns, `bloom_filter_offset` and `bloom_filter_length`. Furthermore, to actually find out which row groups would be eliminated by Bloom filters for a given file and column, we have added the `parquet_bloom_probe` function. For example, `parquet_bloom_probe('file.parquet', 'col1', 42)` returns a table for each row group in `file.parquet` that indicates whether the value `42` can guaranteed not to be in each row group or not for column `col1`. Most users will not need to use these functions however, they just help with debugging (and testing).

## Example Use Case

Let's showcase the Parquet Bloom filters in DuckDB with an example. First, we create a example file `filter.parquet` that *will* contain Bloom filters:

```sql
COPY (
    FROM range(10) r1, range(10_000_000) r2
    SELECT r1.range * 100 AS r
    ORDER BY random()
)
TO 'filter.parquet'
(FORMAT parquet, ROW_GROUP_SIZE 10_000_000);
```

```sql
SELECT r, count(*)
FROM 'filter.parquet'
GROUP BY r
ORDER BY r;
```

The file contains 10 distinct values `(0, 100, 200 ... 900)`, each repeated ten million times. So in total, 100 million rows. The resulting Parquet file weighs in at 88 MB. 

We will also create an equivalent file but *without* Bloom filters. We achieve this by setting the `DICTIONARY_SIZE_LIMIT` to 1:

```sql
COPY 'filter.parquet' to 'nofilter.parquet'
(FORMAT parquet, DICTIONARY_SIZE_LIMIT 1, ROW_GROUP_SIZE 10_000_000);
```

The contents of both files will be equivalent, but `nofilter.parquet` will not use dictionary encoding and thus not use Bloom filters. As a result, the file is also larger, weighing in at 181 MB. However, there is a much larger difference when querying for non-existing values, in our example `501`:

```sql
.timer on
SELECT sum(r) FROM 'filter.parquet'   WHERE r = 501;
SELECT sum(r) FROM 'nofilter.parquet' WHERE r = 501;
```

The first query completes in ca. than 0.002 s, where the second query takes 0.1 s. This large difference can be explained by Bloom filters! Since `501` does not actually occur in the query, DuckDB can automatically exclude all row groups and not actually read any data besides the Bloom filters. We can explore this further using the `parquet_metadata` function:
 
```sql
FROM parquet_metadata('filter.parquet')
SELECT row_group_id, stats_min, stats_max,
    bloom_filter_offset, bloom_filter_length
ORDER BY row_group_id;
```

| row_group_id | stats_min | stats_max | bloom_filter_offset | bloom_filter_length |
|-------------:|----------:|----------:|--------------------:|--------------------:|
| 0            | 0         | 900       | 92543967            | 47                  |
| ...          |           |           |                     |                     |
| 9            | 0         | 900       | 92544390            | 47                  |

We can see that there are ten row groups, and that there is a quite compact Bloom filter for reach row group with a length of 47 bytes each. That's ca. 500 bytes added to fairly large file, so rather irrelevant for file size.

If we run the query on the other file, we can see the lack of Bloom filters:

```sql
FROM parquet_metadata('nofilter.parquet')
SELECT row_group_id, stats_min, stats_max,
       bloom_filter_offset, bloom_filter_length
ORDER BY row_group_id;
```

| row_group_id | stats_min | stats_max | bloom_filter_offset | bloom_filter_length |
|-------------:|----------:|----------:|---------------------|---------------------|
| 0            | 0         | 900       | NULL                | NULL                |
| ...          |           |           |                     |                     |

We can further explore the Bloom filters in the file using the `parquet_bloom_probe` function. For example, for the value of 500 (which exists in the data), the function shows the following:

```sql
FROM parquet_bloom_probe('filter.parquet', 'r', 500);
```

|   file_name    | row_group_id | bloom_filter_excludes |
|----------------|-------------:|----------------------:|
| filter.parquet | 0            | false                 |
| ...            | ...          | ...                   |
| filter.parquet | 9            | false                 |

So the Bloom filter cannot exclude any row group because the value `500` is contained in all row groups. But if we try a *non-existent* value, the Bloom filter strikes:

```sql
FROM parquet_bloom_probe('filter.parquet', 'r', 501);
```

|   file_name    | row_group_id | bloom_filter_excludes |
|----------------|-------------:|----------------------:|
| filter.parquet | 0            | true                  |
| ...            | ...          | ...                   |
| filter.parquet | 9            | true                  |

Here, we can confidently skip all row groups because the Bloom filter guarantees that there can be no matching values in those row groups. All that with 47 bytes per row group.

## Conclusion

DuckDB's new Bloom filter support for Parquet files can greatly reduce the amount of data to be read in certain scenarios, greatly improving query performance. This is particularly useful if files are read over a slow network connection or if row groups are particularly large with few distinct yet non-clustered values.

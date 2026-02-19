---
layout: docu
title: Querying Parquet Metadata
---

## Parquet Metadata

The `parquet_metadata` function can be used to query the metadata contained within a Parquet file, which reveals various internal details of the Parquet file such as the statistics of the different columns. This can be useful for figuring out what kind of skipping is possible in Parquet files, or even to obtain a quick overview of what the different columns contain:

```sql
SELECT *
FROM parquet_metadata('test.parquet');
```

Below is a table of the columns returned by `parquet_metadata`.

<div class="monospace_table"></div>

| Field                      | Type            |
| -------------------------- | --------------- |
| file_name                  | VARCHAR         |
| row_group_id               | BIGINT          |
| row_group_num_rows         | BIGINT          |
| row_group_num_columns      | BIGINT          |
| row_group_bytes            | BIGINT          |
| column_id                  | BIGINT          |
| file_offset                | BIGINT          |
| num_values                 | BIGINT          |
| path_in_schema             | VARCHAR         |
| type                       | VARCHAR         |
| stats_min                  | VARCHAR         |
| stats_max                  | VARCHAR         |
| stats_null_count           | BIGINT          |
| stats_distinct_count       | BIGINT          |
| stats_min_value            | VARCHAR         |
| stats_max_value            | VARCHAR         |
| compression                | VARCHAR         |
| encodings                  | VARCHAR         |
| index_page_offset          | BIGINT          |
| dictionary_page_offset     | BIGINT          |
| data_page_offset           | BIGINT          |
| total_compressed_size      | BIGINT          |
| total_uncompressed_size    | BIGINT          |
| key_value_metadata         | MAP(BLOB, BLOB) |
| bloom_filter_offset        | BIGINT          |
| bloom_filter_length        | BIGINT          |
| min_is_exact               | BOOLEAN         |
| max_is_exact               | BOOLEAN         |
| row_group_compressed_bytes | BIGINT          |

## Parquet Schema

The `parquet_schema` function can be used to query the internal schema contained within a Parquet file. Note that this is the schema as it is contained within the metadata of the Parquet file. If you want to figure out the column names and types contained within a Parquet file it is easier to use `DESCRIBE`.

Fetch the column names and column types:

```sql
DESCRIBE SELECT * FROM 'test.parquet';
```

Fetch the internal schema of a Parquet file:

```sql
SELECT *
FROM parquet_schema('test.parquet');
```

Below is a table of the columns returned by `parquet_schema`.

<div class="monospace_table"></div>

| Field           | Type    |
| --------------- | ------- |
| file_name       | VARCHAR |
| name            | VARCHAR |
| type            | VARCHAR |
| type_length     | VARCHAR |
| repetition_type | VARCHAR |
| num_children    | BIGINT  |
| converted_type  | VARCHAR |
| scale           | BIGINT  |
| precision       | BIGINT  |
| field_id        | BIGINT  |
| logical_type    | VARCHAR |

## Parquet File Metadata

The `parquet_file_metadata` function can be used to query file-level metadata such as the format version and the encryption algorithm used:

```sql
SELECT *
FROM parquet_file_metadata('test.parquet');
```

Below is a table of the columns returned by `parquet_file_metadata`.

<div class="monospace_table"></div>

| Field                       | Type    |
| --------------------------- | ------- |
| file_name                   | VARCHAR |
| created_by                  | VARCHAR |
| num_rows                    | BIGINT  |
| num_row_groups              | BIGINT  |
| format_version              | BIGINT  |
| encryption_algorithm        | VARCHAR |
| footer_signing_key_metadata | VARCHAR |

## Parquet Key-Value Metadata

The `parquet_kv_metadata` function can be used to query custom metadata defined as key-value pairs:

```sql
SELECT *
FROM parquet_kv_metadata('test.parquet');
```

Below is a table of the columns returned by `parquet_kv_metadata`.

<div class="monospace_table"></div>

| Field     | Type    |
| --------- | ------- |
| file_name | VARCHAR |
| key       | BLOB    |
| value     | BLOB    |

## Bloom Filters

DuckDB [supports Bloom filters]({% post_url 2025-03-07-parquet-bloom-filters-in-duckdb %}) for pruning the row groups that need to be read to answer highly selective queries.
Currently, Bloom filters are supported for the following types:

* Integer types: `TINYINT`, `UTINYINT`, `SMALLINT`, `USMALLINT`, `INTEGER`, `UINTEGER`, `BIGINT`, `UBIGINT`
* Floating point types: `FLOAT`, `DOUBLE`
* `VARCHAR`
* `BLOB`

The `parquet_bloom_probe(filename, column_name, value)` function shows which row groups can be excluded when filtering for a given value of a given column using the Bloom filter.
For example:

```sql
FROM parquet_bloom_probe('my_file.parquet', 'my_col', 500);
```

| file_name       | row_group_id | bloom_filter_excludes |
| --------------- | -----------: | --------------------: |
| my_file.parquet |            0 |                  true |
| ...             |          ... |                   ... |
| my_file.parquet |            9 |                 false |

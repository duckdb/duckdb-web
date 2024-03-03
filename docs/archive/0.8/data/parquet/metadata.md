---
layout: docu
title: Querying Parquet Metadata
---

### Parquet Metadata
The `parquet_metadata` function can be used to query the metadata contained within a Parquet file, which reveals various internal details of the Parquet file such as the statistics of the different columns. This can be useful for figuring out what kind of skipping is possible in Parquet files, or even to obtain a quick overview of what the different columns contain.

```sql
SELECT * FROM parquet_metadata('test.parquet');
```

Below is a table of the columns returned by `parquet_metadata`.

|          Field          |  Type   |
|-------------------------|---------|
| file_name               | VARCHAR |
| row_group_id            | BIGINT  |
| row_group_num_rows      | BIGINT  |
| row_group_num_columns   | BIGINT  |
| row_group_bytes         | BIGINT  |
| column_id               | BIGINT  |
| file_offset             | BIGINT  |
| num_values              | BIGINT  |
| path_in_schema          | VARCHAR |
| type                    | VARCHAR |
| stats_min               | VARCHAR |
| stats_max               | VARCHAR |
| stats_null_count        | BIGINT  |
| stats_distinct_count    | BIGINT  |
| stats_min_value         | VARCHAR |
| stats_max_value         | VARCHAR |
| compression             | VARCHAR |
| encodings               | VARCHAR |
| index_page_offset       | BIGINT  |
| dictionary_page_offset  | BIGINT  |
| data_page_offset        | BIGINT  |
| total_compressed_size   | BIGINT  |
| total_uncompressed_size | BIGINT  |


### Parquet Schema
The `parquet_schema` function can be used to query the internal schema contained within a Parquet file. Note that this is the schema as it is contained within the metadata of the Parquet file. If you want to figure out the column names and types contained within a Parquet file it is easier to use `DESCRIBE`.

```sql
-- fetch the column names and column types
DESCRIBE SELECT * FROM 'test.parquet';
-- fetch the internal schema of a parquet file
SELECT * FROM parquet_schema('test.parquet');
```

Below is a table of the columns returned by `parquet_schema`.

|      Field      |  Type   |
|-----------------|---------|
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

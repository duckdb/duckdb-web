---
github_repository: https://github.com/duckdb/duckdb-avro
layout: docu
title: Avro Extension
---

The `avro` extension enables DuckDB to read [Apache Avro](https://avro.apache.org) files.

> The `avro` extension was [released as a community extension in late 2024]({% post_url 2024-12-09-duckdb-avro-extension %}) and became a core extension in early 2025.

## The `read_avro` Function

The extension adds a single DuckDB function, `read_avro`. This function can be used like so:

```sql
FROM read_avro('⟨some_file⟩.avro');
```

This function will expose the contents of the Avro file as a DuckDB table. You can then use any arbitrary SQL constructs to further transform this table.

## File IO

The `read_avro` function is integrated into DuckDB's file system abstraction, meaning you can read Avro files directly from, e.g., HTTP or S3 sources. For example:

```sql
FROM read_avro('https://blobs.duckdb.org/data/userdata1.avro');
FROM read_avro('s3://⟨your-bucket⟩/⟨some_file⟩.avro');
```

should "just" work.

You can also *glob* multiple files in a single read call or pass a list of files to the functions:

```sql
FROM read_avro('some_file_*.avro');
FROM read_avro(['some_file_1.avro', 'some_file_2.avro']);
```

If the filenames somehow contain valuable information (as is unfortunately all-too-common), you can pass the `filename` argument to `read_avro`:

```sql
FROM read_avro('some_file_*.avro', filename=true);
```

This will result in an additional column in the result set that contains the actual filename of the Avro file. 

## Schema Conversion

This extension automatically translates the Avro Schema to the DuckDB schema. *All* Avro types can be translated, except for *recursive type definitions*, which DuckDB does not support.

The type mapping is very straightforward except for Avro's "unique" way of handling `NULL`. Unlike other systems, Avro does not treat `NULL` as a possible value in a range of e.g. `INTEGER` but instead represents `NULL` as a union of the actual type with a special `NULL` type. This is different to DuckDB, where any value can be `NULL`. Of course DuckDB also supports `UNION` types, but this would be quite cumbersome to work with.

This extension *simplifies* the Avro schema where possible: An Avro union of any type and the special null type is simplified to just the non-null type. For example, an Avro record of the union type `["int","null"]` becomes a DuckDB `INTEGER`, which just happens to be `NULL` sometimes. Similarly, an Avro union that contains only a single type is converted to the type it contains. For example, an Avro record of the union type `["int"]` also becomes a DuckDB `INTEGER`.

The extension also "flattens" the Avro schema. Avro defines tables as root-level "record" fields, which are the same as DuckDB `STRUCT` fields. For more convenient handling, this extension turns the entries of a single top-level record into top-level columns.

## Implementation

Internally, this extension uses the "official" [Apache Avro C API](https://avro.apache.org/docs/++version++/api/c/), albeit with some minor patching to allow reading of Avro files from memory.

## Limitations and Future Plans

* This extension currently does not make use of **parallelism** when reading either a single (large) Avro file or when reading a list of files. Adding support for parallelism in the latter case is on the roadmap. 
* There is currently no support for either projection or filter **pushdown**, but this is also planned at a later stage.
* There is currently no support for the Wasm or the Windows-MinGW builds of DuckDB due to issues with the Avro library dependency (sigh again). We plan to fix this eventually.
* As mentioned above, DuckDB cannot express recursive type definitions that Avro has, this is unlikely to ever change.
* There is no support to allow users to provide a separate Avro schema file. This is unlikely to change, all Avro files we have seen so far had their schema embedded.
* There is currently no support for the `union_by_name` flag that other readers in DuckDB support. This is planned for the future.

---
layout: post
title: "The DuckDB Avro Extension"
author: "Hannes Mühleisen"
thumb: "/images/blog/thumbs/avro.svg"
image: "/images/blog/thumbs/avro.png"
excerpt: "DuckDB now supports reading Avro files through the `avro` community extension."
tags: ["extensions"]
---

## The Apache™ Avro™ Format

[Avro](https://avro.apache.org) is a binary format for record data. Like many innovations in the data space, Avro was [developed](https://vimeo.com/7362534) by [Doug Cutting](https://en.wikipedia.org/wiki/Doug_Cutting) as part of the Apache Hadoop project [in around 2009](https://github.com/apache/hadoop/commit/8296413d4988c08343014c6808a30e9d5e441bfc). Avro gets its name – somewhat obscurely – from a defunct [British aircraft manufacturer](https://en.wikipedia.org/wiki/Avro). The company famously built over 7,000 [Avro Lancaster heavy bombers](https://en.wikipedia.org/wiki/Avro_Lancaster) under the challenging conditions of World War 2. But we digress.

The Avro format is yet another attempt to solve the dimensionality reduction problem that occurs when transforming a complex *multi-dimensional data structure* like tables (possibly with nested types) to a *single-dimensional storage layout* like a flat file, which is just a sequence of bytes. The most fundamental question that arises here is whether to use a columnar or a row-major layout. Avro uses a row-major layout, which differentiates it from its famous cousin, the [Apache™ Parquet™](https://parquet.apache.org) format. There are valid use cases for a row-major format: for example, appending a few rows to a Parquet file is difficult and inefficient because of Parquet's columnar layout and due to the fact the Parquet metadata is stored *at the back* of the file. In a row-major format like Avro with the metadata *up top*, we can “just” add those rows to the end of the files and we're done. This enables Avro to handle appends of a few rows somewhat efficiently.

Avro-encoded data can appear in several ways, e.g., in [RPC messages](https://en.wikipedia.org/wiki/Remote_procedure_call) but also in files. In the following, we focus on files since those survive long-term.

### Header Block

Avro “object container” files are encoded using a comparatively simple binary [format](https://avro.apache.org/docs/++version++/specification/#object-container-files): each file starts with a **header block** that first has the [magic bytes](https://en.wikipedia.org/wiki/List_of_file_signatures) `Obj1`. Then, a metadata “map” (a list of string-bytearray key-value pairs) follows. The map is only strictly required to contain a single entry for the `avro.schema` key. This key contains the Avro file schema encoded as JSON. Here is an example for such a schema:

```json
{
  "namespace": "example.avro",
  "type": "record",
  "name": "User",
  "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number", "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
  ]
}
```

The Avro schema defines a record structure. Records can contain scalar data fields (like `int`, `double`, `string`, etc.) but also more complex types like records (similar to [DuckDB `STRUCT`s]({% link docs/stable/sql/data_types/struct.md %})), unions and lists. As a sidenote, it is quite strange that a data format for the definition of record structures would fall back to another format like JSON to describe itself, but such are the oddities of Avro.

### Data Blocks

The header concludes with 16 randomly chosen bytes as a “sync marker”. The header is followed by an arbitrary amount of **data blocks**: each data block starts with a record count, followed by a size and a byte array containing the actual records. Optionally, the bytes can be compressed with deflate (gzip), which will be known from the header metadata.

The data bytes can only be decoded using the schema. The [object file specification](https://avro.apache.org/docs/++version++/specification/#object-container-files) contains the details on how each type is encoded. For example, in the example schema we know each value is a record of three fields. The root-level record will encode its entries in the order they are declared. There are no actual bytes required for this. First we will be reading the `name` field. Strings consist of a length followed by the string bytes. Like other formats (e.g., Thrift), Avro uses [variable-length integers with zigzag encoding](https://en.wikipedia.org/wiki/Variable-length_quantity#Zigzag_encoding) to store lengths and counts and the like. After reading the string, we can proceed to `favorite_number`. This field is a union type (encoded with the `[]` syntax). This union can have values of two types, `int` and `null`. The `null` type is a bit odd, it can only be used to encode the fact that a value is missing. To decode the `favorite_number` fields, we first read an `int` that encodes which choice of the union was used. Afterward, we use the “normal” decoders to read the values (e.g., `int` or `null`). The same can be done for `favorite_color`. Each data block again ends with the sync marker. The sync marker can be used to verify that the block was fully written and that there is no garbage in the file.

## The DuckDB `avro` Community Extension

We have developed a DuckDB community extension that enables DuckDB to *read* [Apache Avro™](https://avro.apache.org) files.

The extension does not contain Avro *write* functionality. This is on purpose, by not providing a writer we hope to decrease the amount of Avro files in the world over time.

### Installation & Loading

Installation is simple through the DuckDB community extension repository, just type

```sql
INSTALL avro FROM community;
LOAD avro;
```

in a DuckDB instance near you. There is currently no build for Wasm because of dependencies (sigh).

### The `read_avro` Function

The extension adds a single DuckDB function, `read_avro`. This function can be used like so:

```sql
FROM read_avro('some_example_file.avro');
```

This function will expose the contents of the Avro file as a DuckDB table. You can then use any arbitrary SQL constructs to further transform this table.

### File IO

The `read_avro` function is integrated into DuckDB's file system abstraction, meaning you can read Avro files directly from e.g., HTTP or S3 sources. For example:

```sql
FROM read_avro('http://blobs.duckdb.org/data/userdata1.avro');
FROM read_avro('s3://my-example-bucket/some_example_file.avro');
```

should “just” work.

You can also [*glob* multiple files]({% link docs/stable/sql/functions/pattern_matching.md %}#globbing) in a single read call or pass a list of files to the functions:

```sql
FROM read_avro('some_example_file_*.avro');
FROM read_avro(['some_example_file_1.avro', 'some_example_file_2.avro']);
```

If the filenames somehow contain valuable information (as is unfortunately all-too-common), you can pass the `filename` argument to `read_avro`:

```sql
FROM read_avro('some_example_file_*.avro', filename = true);
```

This will result in an additional column in the result set that contains the actual filename of the Avro file.

### Schema Conversion

This extension automatically translates the Avro Schema to the DuckDB schema. *All* Avro types can be translated, except for *recursive type definitions*, which DuckDB does not support.

The type mapping is very straightforward except for Avro's “unique” way of handling `NULL`. Unlike other systems, Avro does not treat `NULL` as a possible value in a range of e.g., `INTEGER` but instead represents `NULL` as a union of the actual type with a special `NULL` type. This is different to DuckDB, where any value can be `NULL`. Of course DuckDB also supports `UNION` types, but this would be quite cumbersome to work with.

This extension *simplifies* the Avro schema where possible: an Avro union of any type and the special null type is simplified to just the non-null type. For example, an Avro record of the union type `["int", "null"]` (like `favorite_number` in the [example](#header-block)) becomes a DuckDB `INTEGER`, which just happens to be `NULL` sometimes. Similarly, an Avro union that contains only a single type is converted to the type it contains. For example, an Avro record of the union type `["int"]` also becomes a DuckDB `INTEGER`.

The extension also “flattens” the Avro schema. Avro defines tables as root-level “record” fields, which are the same as DuckDB `STRUCT` fields. For more convenient handling, this extension turns the entries of a single top-level record into top-level columns.

### Implementation

Internally, this extension uses the “official” [Apache Avro C API](https://avro.apache.org/docs/++version++/api/c/), albeit with some minor patching to allow reading Avro files from memory.

### Limitations & Next Steps

In the following, we disclose the limitations of the `avro` DuckDB extension along with our plans to mitigate them in the future:

* The extension currently does not make use of **parallelism** when reading either a single (large) Avro file or when reading a list of files. Adding support for parallelism in the latter case is on the roadmap.

* There is currently no support for projection or filter **pushdown**, but this is also planned at a later stage.

* There is currently no support for the Wasm or the Windows-MinGW builds of DuckDB due to issues with the Avro library dependency (sigh again). We plan to fix this eventually.

* As mentioned above, DuckDB cannot express recursive type definitions that Avro has. This is unlikely to ever change.

* There is no support to allow users to provide a separate Avro schema file. This is unlikely to change, all Avro files we have seen so far had their schema embedded.

* There is currently no support for the `union_by_name` flag that other readers in DuckDB support. This is planned for the future.

## Conclusion

The new `avro` community extension for DuckDB enables DuckDB to read Avro files directly as if they were tables. If you have a bunch of Avro files, go ahead and try it out! We'd love to [hear from you](https://github.com/hannes/duckdb_avro/issues) if you run into any issues.

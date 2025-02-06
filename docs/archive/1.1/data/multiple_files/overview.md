---
layout: docu
redirect_from:
- /docs/archive/1.1/data/csv/multiple_files
title: Reading Multiple Files
---

DuckDB can read multiple files of different types (CSV, Parquet, JSON files) at the same time using either the glob syntax, or by providing a list of files to read.
See the [combining schemas]({% link docs/archive/1.1/data/multiple_files/combining_schemas.md %}) page for tips on reading files with different schemas.

## CSV

Read all files with a name ending in `.csv` in the folder `dir`:

```sql
SELECT *
FROM 'dir/*.csv';
```

Read all files with a name ending in `.csv`, two directories deep:

```sql
SELECT *
FROM '*/*/*.csv';
```

Read all files with a name ending in `.csv`, at any depth in the folder `dir`:

```sql
SELECT *
FROM 'dir/**/*.csv';
```

Read the CSV files `flights1.csv` and `flights2.csv`:

```sql
SELECT *
FROM read_csv(['flights1.csv', 'flights2.csv']);
```

Read the CSV files `flights1.csv` and `flights2.csv`, unifying schemas by name and outputting a `filename` column:

```sql
SELECT *
FROM read_csv(['flights1.csv', 'flights2.csv'], union_by_name = true, filename = true);
```

## Parquet

Read all files that match the glob pattern:

```sql
SELECT *
FROM 'test/*.parquet';
```

Read three Parquet files and treat them as a single table:

```sql
SELECT *
FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

Read all Parquet files from two specific folders:

```sql
SELECT *
FROM read_parquet(['folder1/*.parquet', 'folder2/*.parquet']);
```

Read all Parquet files that match the glob pattern at any depth:

```sql
SELECT *
FROM read_parquet('dir/**/*.parquet');
```

## Multi-File Reads and Globs

DuckDB can also read a series of Parquet files and treat them as if they were a single table. Note that this only works if the Parquet files have the same schema. You can specify which Parquet files you want to read using a list parameter, glob pattern matching syntax, or a combination of both.

### List Parameter

The `read_parquet` function can accept a list of filenames as the input parameter.

Read three Parquet files and treat them as a single table:

```sql
SELECT *
FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

### Glob Syntax

Any file name input to the `read_parquet` function can either be an exact filename, or use a glob syntax to read multiple files that match a pattern.

|  Wildcard  |                        Description                        |
|------------|-----------------------------------------------------------|
| `*`        | Matches any number of any characters (including none)     |
| `**`       | Matches any number of subdirectories (including none)     |
| `?`        | Matches any single character                              |
| `[abc]`    | Matches one character given in the bracket                |
| `[a-z]`    | Matches one character from the range given in the bracket |

Note that the `?` wildcard in globs is not supported for reads over S3 due to HTTP encoding issues.

Here is an example that reads all the files that end with `.parquet` located in the `test` folder:

Read all files that match the glob pattern:

```sql
SELECT *
FROM read_parquet('test/*.parquet');
```

### List of Globs

The glob syntax and the list input parameter can be combined to scan files that meet one of multiple patterns.

Read all Parquet files from 2 specific folders.

```sql
SELECT *
FROM read_parquet(['folder1/*.parquet', 'folder2/*.parquet']);
```

DuckDB can read multiple CSV files at the same time using either the glob syntax, or by providing a list of files to read.

## Filename

The `filename` argument can be used to add an extra `filename` column to the result that indicates which row came from which file. For example:

```sql
SELECT *
FROM read_csv(['flights1.csv', 'flights2.csv'], union_by_name = true, filename = true);
```

| FlightDate | OriginCityName |  DestCityName   | UniqueCarrier |   filename   |
|------------|----------------|-----------------|---------------|--------------|
| 1988-01-01 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-02 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-03 | New York, NY   | Los Angeles, CA | AA            | flights2.csv |

## Glob Function to Find Filenames

The glob pattern matching syntax can also be used to search for filenames using the `glob` table function.
It accepts one parameter: the path to search (which may include glob patterns).

Search the current directory for all files.

```sql
SELECT *
FROM glob('*');
```

|     file      |
|---------------|
| test.csv      |
| test.json     |
| test.parquet  |
| test2.csv     |
| test2.parquet |
| todos.json    |
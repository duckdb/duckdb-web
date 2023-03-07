---
layout: docu
title: Reading Multiple Files
redirect_from:
  - /docs/data/csv/multiple_files
---

DuckDB can read multiple files of different types (CSV, Parquet, JSON files) at the same time using either the glob syntax, or by providing a list of files to read. See the [combining schemas][combining_schemas] page for tips on reading files with different schemas.

### CSV

```sql
-- read all files with a name ending in ".csv" in the folder "dir"
SELECT * FROM 'dir/*.csv';
-- read all files with a name ending in ".csv", two directories deep
SELECT * FROM '*/*/*.csv';
-- read the CSV files 'flights1.csv' and 'flights2.csv'
SELECT * FROM read_csv_auto(['flights1.csv', 'flights2.csv'])
-- read the CSV files 'flights1.csv' and 'flights2.csv', unifying schemas by name and outputting a `filename` column
SELECT * FROM read_csv_auto(['flights1.csv', 'flights2.csv'], union_by_name=True, filename=True)
```

### Parquet

```sql
-- read all files that match the glob pattern
SELECT * FROM 'test/*.parquet';
-- read 3 parquet files and treat them as a single table
SELECT * FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
-- Read all parquet files from 2 specific folders
SELECT * FROM read_parquet(['folder1/*.parquet','folder2/*.parquet']);
```


### Multi-File Reads and Globs
DuckDB can also read a series of Parquet files and treat them as if they were a single table. Note that this only works if the Parquet files have the same schema. You can specify which Parquet files you want to read using a list parameter, glob pattern matching syntax, or a combination of both.

#### List Parameter
The read_parquet function can accept a list of filenames as the input parameter.

```sql
-- read 3 parquet files and treat them as a single table
SELECT * FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

#### Glob Syntax
Any file name input to the read_parquet function can either be an exact filename, or use a glob syntax to read multple files that match a pattern.

|  Wildcard  |                        Description                        |
|------------|-----------------------------------------------------------|
| `*`        | matches any number of any characters (including none)     |
| `?`        | matches any single character                              |
| `[abc]`    | matches one character given in the bracket                |
| `[a-z]`    | matches one character from the range given in the bracket |

Note that the `?` wildcard in globs is not supported for reads over S3 due to HTTP encoding issues. 

Here is an example that reads all the files that end with `.parquet` located in the `test` folder:

```sql
-- read all files that match the glob pattern
SELECT * FROM read_parquet('test/*.parquet');
```

#### List of Globs
The glob syntax and the list input parameter can be combined to scan files that meet one of multiple patterns.

```sql
-- Read all parquet files from 2 specific folders
SELECT * FROM read_parquet(['folder1/*.parquet','folder2/*.parquet']);
```

DuckDB can read multiple CSV files at the same time using either the glob syntax, or by providing a list of files to read.

### Filename

The `filename` argument can be used to add an extra `filename` column to the result that indicates which row came from which file. For example:

```sql
SELECT * FROM read_csv_auto(['flights1.csv', 'flights2.csv'], union_by_name=True, filename=True)
```

| FlightDate | OriginCityName |  DestCityName   | UniqueCarrier |   filename   |
|------------|----------------|-----------------|---------------|--------------|
| 1988-01-01 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-02 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-03 | New York, NY   | Los Angeles, CA | AA            | flights2.csv |

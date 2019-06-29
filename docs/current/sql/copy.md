---
layout: default
title: CSV Import/Export
selected: Documentation/CSV Import
---
# CSV Import
```sql
COPY table_name [ ( column_name [, ...] ) ]
FROM 'filename'
[ [ WITH ] (option [, ...]) ]

where option can be one of:

   DELIMITER 'delimiter_character'
   HEADER [ boolean ]
   QUOTE 'quote_character'
```

`COPY ... FROM` imports data into DuckDB from an external CSV file into an existing table. The amount of columns inside the file must match the amount of columns in the table `table_name`, and the contents of the columns must be convertable to the column types of the table. In case this is not possible, an error will be thrown.

If a list of columns is specified, COPY will only copy the data in the specified columns from the file. If there are any columns in the table that are not in the column list, COPY FROM will insert the default values for those columns.

## Parameters

* `table_name`

The name (optionally schema-qualified) of an existing table.

* `column_name`

An optional list of columns to be copied. If no column list is specified, all columns of the table will be copied.

* `filename`

The name of the file from which to copy its contents

* `DELIMITER`

Specifies the character that separates columns within each row (line) of the file. The default is a comma (`,`). This must be a single one-byte character.

* `HEADER`

Specifies that the file contains a header line with the names of each column in the file. When this option is specified the first line is ignored. This option is allowed only when using CSV format.

* `QUOTE`

Specifies the quoting character to be used when a data value is quoted. The default is double-quote (`"`). This must be a single one-byte character.

## Examples

```sql
-- Copy the contents of a comma-separated file 'test.csv' without a header into the table 'test'
COPY test FROM 'test.csv';
-- Copy the contents of a comma-separated file with a header into the 'category' table
COPY category FROM 'categories.csv' HEADER;
-- Copy the contents of 'lineitem.tbl' into the 'lineitem' table, where the contents are delimited by a pipe character ('|')
COPY lineitem FROM 'lineitem.tbl' DELIMITER '|';
-- Read the contents of a comma-separated file 'names.csv' into the 'name' column of the 'category' table. Any other columns of this table are filled with their default value.
COPY category(name) FROM 'names.csv';
```

# CSV Export
```sql
COPY table_name [ ( column_name [, ...] ) ]
TO 'filename'
[ [ WITH ] (option [, ...]) ]

COPY (query)
TO 'filename'
[ [ WITH ] (option [, ...]) ]
```

`COPY ... TO` exports data from DuckDB to an external CSV file. The `COPY ... TO` has the same set of options as the `COPY ... FROM`, however, in the case of `COPY ... TO` the options specify how the CSV file should be written to disk. Any CSV file created by `COPY ... TO` can be copied back into the database by using `COPY ... FROM` with the same set of options.

The `COPY ... TO` function can be called specifying either a table name, or a query. When a table name is specified, the contents of the entire table will be written into the resulting CSV file. When a query is specified, the query is executed and the result of the query is written to the resulting file.

## Examples
```sql
-- Copy the contents of the 'lineitem' table to the file 'lineitem.tbl', where the columns are delimited by a pipe character ('|'), including a header line.
COPY lineitem TO 'lineitem.tbl' DELIMITER '|' HEADER;
-- Copy the l_orderkey column of the 'lineitem' table to the file 'orderkey.tbl'
COPY lineitem(l_orderkey) TO 'orderkey.tbl' DELIMITER '|';
-- Copy the result of the query SELECT 42 to the file 'query.csv', including a header with column names
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.csv' WITH (HEADER 1, DELIMITER ',');
```


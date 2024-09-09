---
layout: docu
title: Excel Import
redirect_from:
  - /docs/guides/import/excel_import
---

## Installing the Extension

To read data from an Excel file, install and load the [spatial extension]({% link docs/extensions/spatial.md %}).
This is only needed once per DuckDB connection.

```sql
INSTALL spatial;
LOAD spatial;
```

## Importing Excel Sheets

Use the `st_read` function in the `FROM` clause of a query:

```sql
SELECT * FROM st_read('test_excel.xlsx');
```

The `layer` parameter allows specifying the name of the Excel worksheet:

```sql
SELECT * FROM st_read('test_excel.xlsx', layer = 'Sheet1');
```

### Creating a New Table

To create a new table using the result from a query, use `CREATE TABLE ... AS` from a `SELECT` statement:

```sql
CREATE TABLE new_tbl AS
    SELECT * FROM st_read('test_excel.xlsx', layer = 'Sheet1');
```

### Loading to an Existing Table

To load data into an existing table from a query, use `INSERT INTO` from a `SELECT` statement:

```sql
INSERT INTO tbl
    SELECT * FROM st_read('test_excel.xlsx', layer = 'Sheet1');
```

### Options

Several configuration options are also available for the underlying GDAL library that is doing the XLSX parsing.
You can pass them via the `open_options` parameter of the `st_read` function as a list of `'KEY=VALUE'` strings.

#### Importing a Sheet with/without a Header

The option `HEADERS` has three possible values:

* `FORCE`: treat the first row as a header
* `DISABLE` treat the first row as a row of data
* `AUTO` attempt auto-detection (default)

For example, to treat the first row as a header, run:

```sql
SELECT *
FROM st_read(
    'test_excel.xlsx',
    layer = 'Sheet1',
    open_options = ['HEADERS=FORCE']
);
```

#### Detecting Types

The option `FIELD_TYPE` defines how field types should be treated:

* `STRING`: all fields should be loaded as strings (`VARCHAR` type)
* `AUTO`: field types should be auto-detected (default)

For example, to treat the first row as a header and use auto-detection for types, run:

```sql
SELECT *
FROM st_read(
    'test_excel.xlsx',
    layer = 'Sheet1',
    open_options = ['HEADERS=FORCE', 'FIELD_TYPES=AUTO']
);
```

To treat the fields as strings:

```sql
SELECT *
FROM st_read(
    'test_excel.xlsx',
    layer = 'Sheet1',
    open_options = ['FIELD_TYPES=STRING']
);
```

## See Also

DuckDB can also [export Excel files]({% link docs/guides/file_formats/excel_export.md %}).
For additional details on Excel support, see the [spatial extension page]({% link docs/extensions/spatial.md %}), the [GDAL XLSX driver page](https://gdal.org/drivers/vector/xlsx.html), and the [GDAL configuration options page](https://gdal.org/user/configoptions.html#configoptions).

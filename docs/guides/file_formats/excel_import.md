---
layout: docu
title: Excel Import
redirect_from:
  - /docs/guides/import/excel_import
  - /docs/guides/import/excel_import/
---

DuckDB supports reading Excel `.xlsx` files, however, `.xls` files are not supported.

## Importing Excel Sheets

Use the `read_xlsx` function in the `FROM` clause of a query:

```sql
SELECT * FROM read_xlsx('test_excel.xlsx');
```

Alternatively, you can omit the `read_xlsx` function and let DuckDB infer it from the extension:

```sql
SELECT * FROM 'test_excel.xlsx';
```

However, if you want to be able to pass options to control the import behavior, you should use the `read_xlsx` function.

One such option is the `sheet` parameter, which allows specifying the name of the Excel worksheet:

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', sheet = 'Sheet1');
```

By default, the first sheet is loaded if no sheet is specified.

## Importing a specific range

To select a specific range of cells, use the `range` parameter with a string in the format `A1:B2`, where `A1` is the top-left cell and `B2` is the bottom-right cell:

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', range = 'A1:B2');
```

This can also be used to e.g. skip the first 5 of rows:

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', range = 'A5:Z');
```

Or skip the first 5 columns

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', range = 'E:Z');
```

If no range parameter is provided, the range is automatically inferred as the rectangular region of cells between the first row of consecutive non-empty cells and the first empty row spanning the same columns.

By default, if no range is provided DuckDB will stop reading the excel file at when encountering an empty row. But when a range is provided, the default is to read until the end of the range. This behavior can be controlled with the `stop_at_empty` parameter:

```sql
-- Read the first 100 rows, or until the first empty row, whichever comes first
SELECT * FROM read_xlsx('test_excel.xlsx', range = '1:100', stop_at_empty = true);

-- Always read the whole sheet, even if it contains empty rows
SELECT * FROM read_xlsx('test_excel.xlsx', stop_at_empty = false);
```

## Creating a New Table

To create a new table using the result from a query, use `CREATE TABLE ... AS` from a `SELECT` statement:

```sql
CREATE TABLE new_tbl AS
    SELECT * FROM read_xlsx('test_excel.xlsx', sheet = 'Sheet1');
```

## Loading to an Existing Table

To load data into an existing table from a query, use `INSERT INTO` from a `SELECT` statement:

```sql
INSERT INTO tbl
    SELECT * FROM read_xlsx('test_excel.xlsx', sheet = 'Sheet1');
```

Alternatively, you can use the `COPY` statement with the `XLSX` format option to import an Excel file into an existing table:

```sql
COPY tbl FROM 'test_excel.xlsx' (FORMAT XLSX, sheet 'Sheet1');
```

When using the `COPY` statement to load an excel file into a existing table, the types of the columns in the target table will be used to coerce the types of the cells in the Excel sheet.

## Importing a Sheet with/without a Header

To treat the first row as containing the names of the resulting columns, use the `header` parameter:

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', header = true);
```

By default, the first row is treated as a header if all the cells in the first row (within the inferred or supplied range) are non-empty strings. To disable this behavior, set `header` to `false`.

## Detecting Types

When not importing into an existing table, DuckDB will attempt to infer the types of the columns in the Excel sheet based on their contents and/or "number format".

- `TIMESTAMP`, `TIME`, `DATE` and `BOOLEAN` types are inferred when possible based on the "number format" applied to the cell.
- Text cells containing `TRUE` and `FALSE` are inferred as `BOOLEAN`.
- Empty cells are considered to be of type `DOUBLE` by default.
- Otherwise cells are inferred as `VARCHAR` or `DOUBLE` based on their contents.

This behavior can be adjusted in the following ways.

To treat all empty cells as `VARCHAR` instead of `DOUBLE`, set `empty_as_varchar` to `true`:

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', empty_as_varchar = true);
```

To disable type inference completely and treat all cells as `VARCHAR`, set `all_varchar` to `true`:

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', all_varchar = true);
```

Additionally, if the `ignore_errors` parameter is set to `true`, DuckDB will silently replace cells that can't be cast to the corresponding inferred column type with `NULL`'s.

```sql
SELECT * FROM read_xlsx('test_excel.xlsx', ignore_errors = true);
```

## See Also

DuckDB can also [export Excel files]({% link docs/guides/file_formats/excel_export.md %}).
For additional details on Excel support, see the [excel extension page]({% link docs/extensions/excel.md %}).
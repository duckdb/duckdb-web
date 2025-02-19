---
layout: docu
title: Excel Export
redirect_from:
  - /docs/guides/import/excel_export
  - /docs/guides/import/excel_export/
---

DuckDB supports exporting data to Excel `.xlsx` files. However, `.xls` files are not supported.

## Exporting Excel Sheets

To export a table to an Excel file, use the `COPY` statement with the `FORMAT XLSX` option:

```sql
COPY tbl TO 'output.xlsx' WITH (FORMAT XLSX);
```

The result of a query can also be directly exported to an Excel file:

```sql
COPY (SELECT * FROM tbl) TO 'output.xlsx' WITH (FORMAT XLSX);
```

To write the column names as the first row in the Excel file, use the `HEADER` option:

```sql
COPY tbl TO 'output.xlsx' WITH (FORMAT XLSX, HEADER TRUE);
```

To name the worksheet in the resulting Excel file, use the `SHEET` option:

```sql
COPY tbl TO 'output.xlsx' WITH (FORMAT XLSX, SHEET 'Sheet1');
```

## Type Conversions

Because Excel only really supports storing numbers or strings – the equivalent of `VARCHAR` and `DOUBLE`, the following type conversions are automatically applied when writing XLSX files:

* Numeric types are cast to `DOUBLE`.
* Temporal types (`TIMESTAMP`, `DATE`, `TIME`, etc.) are converted to excel "serial" numbers, that is the number of days since 1900-01-01 for dates and the fraction of a day for times. These are then styled with a "number format" so that they appear as dates or times when opened in Excel.
* `TIMESTAMP_TZ` and `TIME_TZ` are cast to UTC `TIMESTAMP` and `TIME` respectively, with the timezone information being lost.
* `BOOLEAN`s are converted to `1` and `0`, with a "number format" applied to make them appear as `TRUE` and `FALSE` in Excel.
* All other types are cast to `VARCHAR` and then written as text cells.

But you can of course also explicitly cast columns to a different type before exporting them to Excel:

```sql
COPY (SELECT CAST(a AS VARCHAR), b FROM tbl) TO 'output.xlsx' WITH (FORMAT XLSX);
```

## See Also

DuckDB can also [import Excel files]({% link docs/guides/file_formats/excel_import.md %}).
For additional details on Excel support, see the [excel extension page]({% link docs/extensions/excel.md %}).

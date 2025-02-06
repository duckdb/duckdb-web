---
layout: docu
redirect_from:
- /docs/archive/1.1/guides/import/excel_export
title: Excel Export
---

## Installing the Extension

To export the data from a table to an Excel file, install and load the [spatial extension]({% link docs/archive/1.1/extensions/spatial/overview.md %}).
This is only needed once per DuckDB connection.

```sql
INSTALL spatial;
LOAD spatial;
```

## Exporting Excel Sheets

Then use the `COPY` statement. The file will contain one worksheet with the same name as the file, but without the `.xlsx` extension:

```sql
COPY tbl TO 'output.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');
```

The result of a query can also be directly exported to an Excel file:

```sql
COPY (SELECT * FROM tbl) TO 'output.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');
```

> Dates and timestamps are currently not supported by the `xlsx` writer.
> Cast columns of those types to `VARCHAR` prior to creating the `xlsx` file.

## See Also

DuckDB can also [import Excel files]({% link docs/archive/1.1/guides/file_formats/excel_import.md %}).
For additional details, see the [spatial extension page]({% link docs/archive/1.1/extensions/spatial/overview.md %}) and the [GDAL XLSX driver page](https://gdal.org/drivers/vector/xlsx.html).
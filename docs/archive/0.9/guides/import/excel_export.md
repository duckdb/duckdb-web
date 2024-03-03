---
layout: docu
redirect_from:
- docs/archive/0.9.2/guides/import/excel_export
title: Excel Export
---

To export the data from a table to an Excel file, install and load the spatial extension, then use the `COPY` statement.
The file will contain one worksheet with the same name as the file, but without the .xlsx extension.

```sql
INSTALL spatial; -- Only needed once per DuckDB connection
LOAD spatial; -- Only needed once per DuckDB connection

COPY tbl TO 'output.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');
```

The result of queries can also be directly exported to an Excel file.

```sql
INSTALL spatial; -- Only needed once per DuckDB connection
LOAD spatial; -- Only needed once per DuckDB connection

COPY (SELECT * FROM tbl) TO 'output.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');
```

**Note**: Dates and timestamps are not supported by the xlsx writer driver. 
Cast columns of those types to `VARCHAR` prior to creating the xlsx file.

**Note**: The output file must not already exist. 

For additional details, see the [spatial extension page](../../extensions/spatial) and the [GDAL XLSX driver page](https://gdal.org/drivers/vector/xlsx.html).
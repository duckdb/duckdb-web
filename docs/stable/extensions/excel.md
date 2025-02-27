---
github_repository: https://github.com/duckdb/duckdb-excel
layout: docu
redirect_from:
- /docs/extensions/excel
title: Excel Extension
---

The `excel` extension provides functions to format numbers per Excel's formatting rules by wrapping the [i18npool library](https://www.openoffice.org/l10n/i18n_framework/index.html), but as of DuckDB 1.2 also provides functionality to read and write Excel (`.xlsx`) files. However, `.xls` files are not supported.

Previously, reading and writing Excel files was handled through the [`spatial` extension]({% link docs/stable/extensions/spatial/overview.md %}), which coincidentally included support for XLSX files through one of its dependencies, but this capability may be removed from the spatial extension in the future. Additionally, the `excel` extension is more efficient and provides more control over the import/export process. See the [Excel Import]({% link docs/stable/guides/file_formats/excel_import.md %}) and [Excel Export]({% link docs/stable/guides/file_formats/excel_export.md %}) pages for instructions.

## Installing and Loading

The `excel` extension will be transparently [autoloaded]({% link docs/stable/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL excel;
LOAD excel;
```

## Excel Scalar Functions

| Function                            | Description                                                          |
| :---------------------------------- | :------------------------------------------------------------------- |
| `excel_text(number, format_string)` | Format the given `number` per the rules given in the `format_string` |
| `text(number, format_string)`       | Alias for `excel_text`                                               |

## Examples

```sql
SELECT excel_text(1_234_567.897, 'h:mm AM/PM') AS timestamp;
```

| timestamp |
| --------- |
| 9:31 PM   |

```sql
SELECT excel_text(1_234_567.897, 'h AM/PM') AS timestamp;
```

| timestamp |
| --------- |
| 9 PM      |

## Reading XLSX Files

Reading a `.xlsx` file is as simple as just `SELECT`ing from it immediately, e.g.:

```sql
SELECT *
FROM 'test.xlsx';
```

|   a |   b |
| --: | --: |
| 1.0 | 2.0 |
| 3.0 | 4.0 |

However, if you want to set additional options to control the import process, you can use the `read_xlsx` function instead. The following named parameters are supported.

| Option             | Type      | Default                  | Description                                                                                                                                                                                                                                                                                           |
| ------------------ | --------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `header`           | `BOOLEAN` | _automatically inferred_ | Whether to treat the first row as containing the names of the resulting columns.                                                                                                                                                                                                                      |
| `sheet`            | `VARCHAR` | _automatically inferred_ | The name of the sheet in the xlsx file to read. Default is the first sheet.                                                                                                                                                                                                                           |
| `all_varchar`      | `BOOLEAN` | `false`                  | Whether to read all cells as containing `VARCHAR`s.                                                                                                                                                                                                                                                   |
| `ignore_errors`    | `BOOLEAN` | `false`                  | Whether to ignore errors and silently replace cells that cant be cast to the corresponding inferred column type with `NULL`'s.                                                                                                                                                                        |
| `range`            | `VARCHAR` | _automatically inferred_ | The range of cells to read, in spreadsheet notation. For example, `A1:B2` reads the cells from A1 to B2. If not specified the resulting range will be inferred as rectangular region of cells between the first row of consecutive non-empty cells and the first empty row spanning the same columns. |
| `stop_at_empty`    | `BOOLEAN` | _automatically inferred_ | Whether to stop reading the file when an empty row is encountered. If an explicit `range` option is provided, this is `false` by default, otherwise `true`.                                                                                                                                           |
| `empty_as_varchar` | `BOOLEAN` | `false`                  | Whether to treat empty cells as `VARCHAR` instead of `DOUBLE` when trying to automatically infer column types.                                                                                                                                                                                        |

```sql
SELECT *
FROM read_xlsx('test.xlsx', header = true);
```

|   a |   b |
| --: | --: |
| 1.0 | 2.0 |
| 3.0 | 4.0 |

Alternatively, the `COPY` statement with the `XLSX` format option can be used to import an Excel file into an existing table, in which case the types of the columns in the target table will be used to coerce the types of the cells in the Excel file.

```sql
CREATE TABLE test (a DOUBLE, b DOUBLE);
COPY test FROM 'test.xlsx' WITH (FORMAT 'xlsx', HEADER);
SELECT * FROM test;
```

### Type and Range Inference

Because Excel itself only really stores numbers or strings in cells, and dont enforce that all cells in a column is of the same type, the `excel` extension has to do some guesswork to "infer" and decide the types of the columns when importing an Excel sheet. While almost all columns are inferred as either `DOUBLE` or `VARCHAR`, there are some caveats:

* `TIMESTAMP`, `TIME`, `DATE` and `BOOLEAN` types are inferred when possible based on the _format_ applied to the cell.
* Text cells containing `TRUE` and `FALSE` are inferred as `BOOLEAN`.
* Empty cells are considered to be `DOUBLE` by default, unless the `empty_as_varchar` option is set to `true`, in which case they are typed as `VARCHAR`.

If the `all_varchar` option is set to `true`, none of the above applies and all cells are read as `VARCHAR`.

When no types are specified explicitly, (e.g., when using the `read_xlsx` function instead of `COPY TO ... FROM '⟨file⟩.xlsx'`)
the types of the resulting columns are inferred based on the first "data" row in the sheet, that is:

* If no explicit range is given
  * The first row after the header if a header is found or forced by the `header` option
  * The first non-empty row in the sheet if no header is found or forced
* If an explicit range is given
  * The second row of the range if a header is found in the first row or forced by the `header` option
  * The first row of the range if no header is found or forced

This can sometimes lead to issues if the first "data row" is not representative of the rest of the sheet (e.g., it contains empty cells) in which case the `ignore_errors` or `empty_as_varchar` options can be used to work around this.

However, when the `COPY TO ... FROM '⟨file⟩.xlsx'` syntax is used, no type inference is done and the types of the resulting columns are determined by the types of the columns in the table being copied to. All cells will simply be converted by casting from `DOUBLE` or `VARCHAR` to the target column type.

## Writing XLSX Files

Writing `.xlsx` files is supported using the `COPY` statement with `XLSX` given as the format. The following additional parameters are supported.

| Option            | Type      | Default   | Description                                                                          |
| ----------------- | --------- | --------- | ------------------------------------------------------------------------------------ |
| `header`          | `BOOLEAN` | `false`   | Whether to write the column names as the first row in the sheet                      |
| `sheet`           | `VARCHAR` | `Sheet1`  | The name of the sheet in the xlsx file to write.                                     |
| `sheet_row_limit` | `INTEGER` | `1048576` | The maximum number of rows in a sheet. An error is thrown if this limit is exceeded. |

> Warning Many tools only support a maximum of 1,048,576 rows in a sheet, so increasing the `sheet_row_limit` may render the resulting file unreadable by other software.

These are passed as options to the `COPY` statement after the `FORMAT`, e.g.:

```sql
CREATE TABLE test AS
    SELECT *
    FROM (VALUES (1, 2), (3, 4)) AS t(a, b);
COPY test TO 'test.xlsx' WITH (FORMAT 'xlsx', HEADER true);
```

### Type conversions

Because XLSX files only really support storing numbers or strings – the equivalent of `VARCHAR` and `DOUBLE`, the following type conversions are applied when writing XLSX files.

* Numeric types are cast to `DOUBLE` when writing to an XLSX file.
* Temporal types (`TIMESTAMP`, `DATE`, `TIME`, etc.) are converted to excel "serial" numbers, that is the number of days since 1900-01-01 for dates and the fraction of a day for times. These are then styled with a "number format" so that they appear as dates or times when opened in Excel.
* `TIMESTAMP_TZ` and `TIME_TZ` are cast to UTC `TIMESTAMP` and `TIME` respectively, with the timezone information being lost.
* `BOOLEAN`s are converted to `1` and `0`, with a "number format" applied to make them appear as `TRUE` and `FALSE` in Excel.
* All other types are cast to `VARCHAR` and then written as text cells.

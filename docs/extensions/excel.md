---
layout: docu
title: Excel Extension
github_repository: https://github.com/duckdb/duckdb_excel
---

The `excel` extension, unlike what its name may suggest, does not provide support for reading Excel files.
Instead, provides a function that wraps the number formatting functionality of the [i18npool library](https://www.openoffice.org/l10n/i18n_framework/index.html), which formats numbers per Excel's formatting rules.

Excel files can be currently handled through the [`spatial` extension](spatial): see the [Excel Import](../guides/import/excel_import) and [Excel Export](../guides/import/excel_export) pages for instructions.

## Installing and Loading

The `excel` extension will be transparently autoloaded on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL excel;
LOAD excel;
```

## Functions

| Function | Description |
|:--|:---|
| `excel_text(number, format_string)`| Format the given `number` per the rules given in the `format_string`. |
| `text(number, format_string)` | Alias for `excel_text`. |

## Examples

```sql
SELECT excel_text(1_234_567.897, 'h:mm AM/PM') AS timestamp;
```

| timestamp |
|-----------|
| 9:31 PM   |

```sql
SELECT excel_text(1_234_567.897, 'h AM/PM') AS timestamp;
```

| timestamp |
|-----------|
| 9 PM      |

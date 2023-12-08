---
layout: docu
redirect_from:
- /docs/extensions/excel
title: Excel Extension
---

This extension, contrary to its name, does not provide support for reading Excel files. It instead provides a function that wraps the number formatting functionality of the [i18npool library](https://www.openoffice.org/l10n/i18n_framework/index.html), which formats numbers per Excel's formatting rules.

Excel files can be handled through the [`spatial` extension](spatial): see the [Excel Import](../guides/import/excel_import) and [Excel Export](../guides/import/excel_export) pages for instructions.

## Installing and Loading

The `excel` extension will be transparently autoloaded on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL excel;
LOAD excel;
```

## Usage

```sql
SELECT excel_text(1234567.897, 'h:mm AM/PM') AS timestamp;
```
```text
┌───────────┐
│ timestamp │
│  varchar  │
├───────────┤
│ 9:31 PM   │
└───────────┘
```

## Functions

| Function | Description | Example | Result |
|:--|:---|:--|:-|
| `text(`*`number`*`, `*`format_string`*`)`       | Format the given `number` per the rules given in the `format_string` | `text(1234567.897, 'h AM/PM')`          | `9 PM`    |
| `excel_text(`*`number`*`, `*`format_string`*`)` | Alias for `text`.                                                    | `excel_text(1234567.897, 'h:mm AM/PM')` | `9:31 PM` |

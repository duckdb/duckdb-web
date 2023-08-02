---
layout: docu
title: Excel
selected: Extensions
---

This extension, contrary to its name, does not provide support for reading Excel files.
Instead, see our guides for Excel [Import](../guides/import/excel_import) and [Export](../guides/import/excel_export).

It instead provides a function that wraps the number formatting functionality of the i18npool library, which formats numbers per excels formatting rules

| Function                                        | Description                                                          | Example                           | Result    |
|:------------------------------------------------|:---------------------------------------------------------------------|:----------------------------------|:----------|
| `text(`*`number`*`, `*`format_string`*`)`       | Format the given `number` per the rules given in the `format_string` | `text(1234567.897, 'h AM/PM')`    | `9 PM`    |
| `excel_text(`*`number`*`, `*`format_string`*`)` | Alias for `text`.                                                    | `text(1234567.897, 'h:mm AM/PM')` | `9:31 PM` |

---
layout: docu
redirect_from:
- /docs/archive/0.10/api/cli/output-formats
title: Output Formats
---

The `.mode` [dot command](dot_commands) may be used to change the appearance of the tables returned in the terminal output. In addition to customizing the appearance, these modes have additional benefits. This can be useful for presenting DuckDB output elsewhere by redirecting the terminal [output to a file](dot_commands#output-writing-results-to-a-file). Using the `insert` mode will build a series of SQL statements that can be used to insert the data at a later point.
The `markdown` mode is particularly useful for building documentation and the `latex` mode is useful for writing academic papers.

<div class="narrow_table"></div>

|     Mode     |                 Description                  |
|--------------|----------------------------------------------|
| `ascii`      | Columns/rows delimited by 0x1F and 0x1E      |
| `box`        | Tables using unicode box-drawing characters  |
| `csv`        | Comma-separated values                       |
| `column`     | Output in columns.  (See .width)             |
| `duckbox`    | Tables with extensive features               |
| `html`       | HTML `<table>` code                          |
| `insert`     | SQL insert statements for TABLE              |
| `json`       | Results in a JSON array                      |
| `jsonlines`  | Results in a NDJSON                          |
| `latex`      | LaTeX tabular environment code               |
| `line`       | One value per line                           |
| `list`       | Values delimited by "\|"                     |
| `markdown`   | Markdown table format                        |
| `quote`      | Escape answers as for SQL                    |
| `table`      | ASCII-art table                              |
| `tabs`       | Tab-separated values                         |
| `tcl`        | TCL list elements                            |
| `trash`      | No output                                    |

```sql
.mode markdown
SELECT 'quacking intensifies' AS incoming_ducks;
```

```text
|    incoming_ducks    |
|----------------------|
| quacking intensifies |
```

The output appearance can also be adjusted with the `.separator` command. If using an export mode that relies on a separator (`csv` or `tabs` for example), the separator will be reset when the mode is changed. For example, `.mode csv` will set the separator to a comma (`,`). Using `.separator "|"` will then convert the output to be pipe-separated.

```sql
.mode csv
SELECT 1 AS col_1, 2 AS col_2
UNION ALL
SELECT 10 AS col1, 20 AS col_2;
```

```csv
col_1,col_2
1,2
10,20
```

```sql
.separator "|"
SELECT 1 AS col_1, 2 AS col_2
UNION ALL
SELECT 10 AS col1, 20 AS col_2;
```

```csv
col_1|col_2
1|2
10|20
```
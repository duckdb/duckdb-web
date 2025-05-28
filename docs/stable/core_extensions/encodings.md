---
github_directory: https://github.com/duckdb/duckdb-encodings
layout: docu
title: Encodings Extension
redirect_from:
- /docs/stable/extensions/encodings
- /docs/stable/extensions/encodings/
- /docs/extensions/encodings
- /docs/extensions/encodings/
---

The `encodings` extension adds supports for reading CSVs using [more than 1,000 character encodings available in the ICU data repository](https://github.com/unicode-org/icu-data/tree/main/charset/data/ucm).

### Installing and Loading

```sql
INSTALL encodings;
LOAD encodings;
```

## Usage

Refer to the encoding while reading from files:

```sql
FROM read_csv('my_shift_jis.csv', encoding = 'shift_jis');
```

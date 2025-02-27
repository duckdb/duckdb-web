---
layout: docu
redirect_from:
- /docs/archive/0.10/sql/case_sensitivity
- /docs/archive/0.10/sql/case_sensitivity/
- /docs/archive/0.10/sql/keywords-and-identifiers
title: Keywords and Identifiers
---

## Identifiers

Similarly to other SQL dialects and programming languages, identifiers in DuckDB's SQL are subject to several rules.

* Unquoted identifiers need to conform to a number of rules:
    * They must not be a reserved keyword (see [`duckdb_keywords()`](duckdb_table_functions#duckdb_keywords)), e.g., `SELECT 123 AS SELECT` will fail.
    * They must not start with a number or special character, e.g., `SELECT 123 AS 1col` is invalid.
    * They cannot contain whitespaces (including tabs and newline characters).
* Identifiers can be quoted using double-quote characters (`"`). Quoted identifiers can use any keyword, whitespace or special character, e.g., `"SELECT"` and `" § 🦆 ¶ "` are valid identifiers.
* Double quotes can be escaped by repeating the quote character, e.g., to create an identifier named `IDENTIFIER "X"`, use `"IDENTIFIER ""X"""`.

### Deduplicating Identifiers

In some cases, duplicate identifiers can occur, e.g., column names may conflict when unnesting a nested data structure.
In these cases, DuckDB automatically deduplicates column names by renaming them according to the following rules:

* For a column named `⟨name⟩`, the first instance is not renamed.
* Subsequent instances are renamed to `⟨name⟩_⟨count⟩`, where `⟨count⟩` starts at 1.

For example:

```sql
SELECT *
FROM (SELECT UNNEST({'a': 42, 'b': {'a': 88, 'b': 99}}, recursive := true));
```

| a  | a_1 | b  |
|---:|----:|---:|
| 42 | 88  | 99 |

## Database Names

Database names are subject to the rules for [identifiers](#identifiers).

Additionally, it is best practice to avoid DuckDB's two internal [database schema names](duckdb_table_functions#duckdb_databases), `system` and `temp`.
By default, persistent databases are named after their filename without the extension.
Therefore, the filenames `system.db` and `temp.db` (as well as `system.duckdb` and `temp.duckdb`) result in the database names `system` and `temp`, respectively.
If you need to attach to a database that has one of these names, use an alias, e.g.:

```sql
ATTACH 'temp.db' AS temp2;
USE temp2;
```

## Rules for Case-Sensitivity

### Keywords and Function Names

SQL keywords and function names are case-insensitive in DuckDB.

For example, the following two queries are equivalent:

```matlab
select COS(Pi()) as CosineOfPi;
SELECT cos(pi()) AS CosineOfPi;
```

| CosineOfPi |
|-----------:|
| -1.0       |

### Case-Sensitivity of Identifiers

Identifiers in DuckDB are always case-insensitive, similarly to PostgreSQL.
However, unlike PostgreSQL (and some other major SQL implementation), DuckDB also treats quoted identifiers as case-sensitive.

Despite treating identifiers in a case-insensitive manner, each character's case (uppercase/lowercase) is maintained as originally specified by the user even if a query uses different cases when referring to the identifier.
For example:

```sql
CREATE TABLE tbl AS SELECT cos(pi()) AS CosineOfPi;
SELECT cosineofpi FROM tbl;
```

| CosineOfPi |
|-----------:|
| -1.0       |

To change this behavior, set the `preserve_identifier_case` [configuration option](../configuration/overview#configuration-reference) to `false`.

#### Handling Conflicts

In case of a conflict, when the same identifier is spelt with different cases, one will be selected randomly. For example:

```sql
CREATE TABLE t1 (idfield INTEGER, x INTEGER);
CREATE TABLE t2 (IdField INTEGER, y INTEGER);
INSERT INTO t1 VALUES (1, 123);
INSERT INTO t2 VALUES (1, 456);
SELECT * FROM t1 NATURAL JOIN t2;
```

| idfield |  x  |  y  |
|--------:|----:|----:|
| 1       | 123 | 456 |

#### Disabling Preserving Cases

With the `preserve_identifier_case` [configuration option](../configuration/overview#configuration-reference) set to `false`, all identifiers are turned into lowercase:

```sql
SET preserve_identifier_case = false;
CREATE TABLE tbl AS SELECT cos(pi()) AS CosineOfPi;
SELECT CosineOfPi FROM tbl;
```

| cosineofpi |
|-----------:|
| -1.0       |
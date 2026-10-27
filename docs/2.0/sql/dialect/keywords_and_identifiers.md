---
layout: docu
redirect_from:
- /docs/sql/case_sensitivity
- /docs/sql/dialect/keywords-and-identifiers
- /docs/sql/dialect/keywords_and_identifiers
- /docs/sql/keywords-and-identifiers
- /docs/stable/sql/dialect/keywords_and_identifiers
- /docs/current/sql/dialect/keywords_and_identifiers
- /docs/lts/sql/dialect/keywords_and_identifiers
- /docs/preview/sql/dialect/keywords_and_identifiers
title: Keywords and Identifiers
---

## Identifiers

Similarly to other SQL dialects and programming languages, identifiers in DuckDB's SQL are subject to several rules.

* Unquoted identifiers need to conform to a number of rules:
    * They must not be a reserved keyword (see [`duckdb_keywords()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_keywords)), e.g., `CREATE TABLE select (i INTEGER)` will fail.
    * They must not start with a number or special character, e.g., `SELECT 123 AS 1col` is invalid.
    * They cannot contain whitespaces (including tabs and newline characters).
* Identifiers can be quoted using double-quote characters (`"`). Quoted identifiers can use any keyword, whitespace or special character, e.g., `"SELECT"` and `" § 🦆 ¶ "` are valid identifiers.
* Double quotes can be escaped by repeating the quote character, e.g., to create an identifier named `IDENTIFIER "X"`, use `"IDENTIFIER ""X"""`.

> New As of DuckDB 2.0, identifiers can also be quoted using backtick characters (`` ` ``), following exactly the same rules as double-quoted identifiers. A backtick is escaped by doubling it, e.g., `` `a``b` `` denotes the identifier `` a`b ``. Backtick-quoted identifiers are never case-folded and work everywhere double-quoted identifiers do. Note that stored and round-tripped DDL (for example in [`duckdb_views()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_views)) still uses double quotes.

### Deduplicating Identifiers

In some cases, duplicate identifiers can occur, e.g., column names may conflict when unnesting a nested data structure.
In these cases, DuckDB automatically deduplicates column names by renaming them according to the following rules:

* For a column named `⟨name⟩`{:.language-sql .highlight}, the first instance is not renamed.
* Subsequent instances are renamed to `⟨name⟩_⟨count⟩`{:.language-sql .highlight}, where `⟨count⟩`{:.language-sql .highlight} starts at 1.

For example:

```sql
SELECT *
FROM (SELECT unnest({'a': 42, 'b': {'a': 88, 'b': 99}}, recursive := true));
```

| a  | a_1 | b  |
|---:|----:|---:|
| 42 | 88  | 99 |

## Identifier Resolution

Identifiers can be *qualified* to remove ambiguity. A fully qualified column reference has the form `⟨database⟩.⟨schema⟩.⟨table⟩.⟨column⟩`, and any leading part can be omitted when the remaining name is unambiguous. Table names can likewise be qualified as `⟨database⟩.⟨schema⟩.⟨table⟩`.

When a name is not fully qualified, DuckDB resolves it using the catalog search path. The search path is controlled by the `schema` and `search_path` [configuration options]({% link docs/2.0/configuration/overview.md %}#local-configuration-options): `schema` sets a single default `⟨catalog⟩.⟨schema⟩` entry, while `search_path` sets a comma-separated list of such entries that are searched in order. Both options write to the same catalog search path, and each entry may be a bare schema or a `⟨catalog⟩.⟨schema⟩` pair.

For a detailed description of how database and schema names are resolved, including the default database and schema and how to change the search path, see [Name Qualification]({% link docs/2.0/sql/statements/attach.md %}#name-qualification) on the `ATTACH` page.

## Database Names

Database names are subject to the rules for [identifiers](#identifiers).

Additionally, it is best practice to avoid DuckDB's two internal [database schema names]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_databases), `system` and `temp`.
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
However, unlike PostgreSQL (and some other major SQL implementations), DuckDB also treats quoted identifiers as case-insensitive.

**Comparison of identifiers:**
Case-insensitivity is implemented using an ASCII-based comparison:
`col_A` and `col_a` are equal but `col_á` is not equal to them.

```sql
SELECT col_A FROM (SELECT 'x' AS col_a); -- succeeds
SELECT col_á FROM (SELECT 'x' AS col_a); -- fails
```

**Preserving cases:**
While DuckDB treats identifiers in a case-insensitive manner, it preserves the cases of these identifiers.
That is, each character's case (uppercase/lowercase) is maintained as originally specified by the user even if a query uses different cases when referring to the identifier.
For example:

```sql
CREATE TABLE tbl AS SELECT cos(pi()) AS CosineOfPi;
SELECT cosineofpi FROM tbl;
```

| CosineOfPi |
|-----------:|
| -1.0       |

To change this behavior, use the `preserve_identifier_case` [configuration option]({% link docs/2.0/configuration/overview.md %}#configuration-reference), see [below](#disabling-preserving-cases).

### Case-Sensitivity of Keys in Nested Data Structures

The keys of `MAP`s are case-sensitive:

```sql
SELECT MAP(['key1'], [1]) = MAP(['KEY1'], [1]) AS equal;
```

```text
false
```

The keys of `UNION`s and `STRUCT`s are case-insensitive:

```sql
SELECT {'key1': 1} = {'KEY1': 1} AS equal;
```

```text
true
```

```sql
SELECT union_value(key1 := 1) = union_value(KEY1 := 1) as equal;
```

```text
true
```

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

> New In DuckDB 2.0, `preserve_identifier_case` is a `VARCHAR` option. Previously, it was a `BOOLEAN` option.

The `preserve_identifier_case` [configuration option]({% link docs/2.0/configuration/overview.md %}#configuration-reference) controls how non-quoted identifiers are folded. It accepts the following values:

* `'preserve_case'` (default): keep the case as written.
* `'lowercase'`: turn non-quoted identifiers into lowercase.
* `'uppercase'`: turn non-quoted identifiers into uppercase.

For backward compatibility, the Boolean values `true` and `false` are also accepted and map to `'preserve_case'` and `'lowercase'`, respectively.

For example, with `preserve_identifier_case` set to `'lowercase'`, all non-quoted identifiers are turned into lowercase:

```sql
SET preserve_identifier_case = 'lowercase';
CREATE TABLE tbl AS SELECT cos(pi()) AS CosineOfPi;
SELECT CosineOfPi FROM tbl;
```

| cosineofpi |
|-----------:|
| -1.0       |

With `preserve_identifier_case` set to `'uppercase'`, they are turned into uppercase, so the table above would be named `TBL` and its column `COSINEOFPI`.

> The setting is applied when a statement is parsed. Therefore, it only takes effect for statements parsed after the `SET` statement has been executed, e.g., in a subsequent query string.

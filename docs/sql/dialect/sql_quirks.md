---
layout: docu
title: SQL Quirks
---

Like all programming languages and libraries, DuckDB has its share of idiosyncrasies and inconsistencies.  
Some are vestiges of our feathered friend's evolution; others are inevitable because we strive to adhere to the [SQL Standard](https://blog.ansi.org/sql-standard-iso-iec-9075-2023-ansi-x3-135/) and specifically to PostgreSQL's dialect (see the [PostgreSQL compatibility]({% link docs/sql/dialect/postgresql_compatibility.md %}) page for exceptions).
The rest may simply come down to different preferences, or we may even agree on what _should_ be done but just haven’t gotten around to it yet.

Acknowledging these quirks is the best we can do, which is why we have compiled below a list of examples that may catch some users off guard: 

- On empty groups, the aggregate functions `sum`, `list`, and `string_agg` all return `NULL` instead of `0`, `[]` and `''`, respectively. This is dictated by the SQL Standard and obeyed by all SQL implementations we know.
- One-based indexing everywhere (e.g., array and string indexing and slicing, and window functions (`row_number`, `rank`, `dense_rank`)) is another SQL Standard requirement. Good for our R users and those with an SQL background, bad for everybody else.
- DuckDB's `1 = true` is common but violates PostgreSQL compatibility, whereas DuckDB's `'t' = true` is more quirky and was inherited from PostgreSQL. DuckDB's `1 = '1.1'` is perhaps most difficult to justify.
- `-1^2 = 1`. PostgreSQL compatibility means the unary minus has higher precedence than the exponentiation operator. Use the `pow` function to avoid mistakes. 
- `'NaN'::FLOAT = 'NaN'::FLOAT` and `'NaN'::FLOAT > 3` violate IEEE-754 but mean floating point data types have a total order, like all other datatypes (beware the consequences for `greatest`/`least`)
- Automatic column deduplication. You thought `SELECT a FROM (SELECT *, 1 AS a FROM tbl)` will give you a bunch of `1`s? Not if `tbl` already contains a column named `a` (or even `A`, see point below).
- Case insensitivity and the resulting inability to `SELECT a FROM 'file.parquet'` when a column called `A` appears before the desired column `a` in `file.parquet`. That's a DuckDB original and can actually be useful when not working with external data: who wants to get the wrong numbers when they get the capitalization wrong?
- `list_extract` / `map_extract` return `NULL` on non-existing keys, `struct_extract` throws. The former follows has PostgreSQL precedence. The latter makes sense because keys of structs are like columns. 
- `USING SAMPLE` is syntactically placed after the `WHERE` and `GROUP BY` clauses (same as the `LIMIT` clause) but is semantically applied before both (unlike the `LIMIT` clause).
- `SELECT CASE WHEN 0 > 1 THEN (SELECT sum(range) FROM range(0, 100000000000000000)) END` never completes to return the obvious `NULL` answer. DuckDB is ducklarative, not imperative; as such, it tries hard to produce fast code for you (e.g., constant folding) but sometimes gets it wrong (e.g., short-circuiting case expressions).
- `1 IN (0, NULL)` is `NULL`. That one makes some sense if you interpret the `NULL`s in the input and output as `UNKNOWN`. Alas, that's not really how `NULL`s work elsewhere: `1 in [0, NULL]` is `false`, `if(NULL > 1, 2, 3)` returns `3`, and most aggregate functions ignore  `NULL`s too even though, for example, the sum of `UNKNOWN` and `1` would be `UNKNOWN`.
- `concat(x, NULL) = x` (same for `list_concat`). If you prefer `NULL`s in, `NULL`s out, use `x || NULL`.
- `age(x)` is `current_date - x` instead of `current_timestamp - x`. Another quirk inherited from PostgreSQL.

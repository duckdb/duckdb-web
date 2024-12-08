Like any language, framework, or interface out there, DuckDB is not without quirks, idiosyncrasies, and inconsistencies.  

Some are unavoidable because we strive to adhere to the SQL Standard and specifically to PostgreSQL's dialect (see the [PostgreSQL compatibility]() page for exceptions).

Some are vestiges of our feathered friend's evolution, and the benefit of righting them has not been deemed worth the pain of migration (yet).

Some are of the type that have divided programmers since the dawn of computers.

Some, we may just not have come around to fixing yet and may never do because there are always bigger fires to put out or more useful features to add.  

Acknowledging and being open about these things is the best we can do. In this sense, we provide below a list of examples that may be surprising to some, in the hope that they won't run into them unprepared while investigating a misbehaving multi-page query on tens of terrabytes of parquet files scattered across S3: 

- The aggregate functions `sum`, `list`, and `string_agg` return `NULL` instead of `0`, `[]` and `''`, respectively, for empty groups. The SQL Standard commands, we obey.
- One-based indexing everywhere (e.g., array and string indexing and slicing, and window functions (`row_number`, `rank`, `dense_rank`)). The SQL Standard dictates, we comply. Good for our R users and those with an SQL background, bad for everybody else.
- DuckDB's `1 = true` is common but violates PostgreSQL compatibility, whereas DuckDB's `'t' = true` is more quirky and was inherited from PostgreSQL. DuckDB's `1 = '1.1'` is probably most difficult to justify.
- `'NaN'::FLOAT = 'NaN'::FLOAT` and `'NaN'::FLOAT > 3` violate IEEE-754 but mean floating point data types are totally ordered, like all other datatypes (beware the consequences for `greatest`/`least`/`ORDER BY`)
- Case insensitivity and the resulting inability to `SELECT A FROM 'file.parquet'` when both `a` and `A` are in the file. That's actually a DuckDB thing. Great when not working with external data, who wants to need to remember the correct capitalization and otherwise get the wrong numbers?
- Automatic column deduplication. You thought `SELECT A FROM (SELECT *, 1 AS A FROM tbl)` will give you a bunch of `1`s? Not if `tbl` already contains a column named `A` (or even `a`, see previous point).
- `list_extract` / `map_extract` return `NULL` on non-existing keys, `struct_extract` throws. The former follows has PostgreSQL precedence. The latter makes sense because keys of structs are like columns. 
- `USING SAMPLE` precedence rules. TODO.
- `SELECT CASE WHEN 0 > 1 THEN (SELECT sum(range) FROM range(0, 100000000000000000)) END` never completes to return the obvious `NULL` answer. DuckDB is ducklarative. As such, it tries hard to produce fast code for you (e.g., constant folding) but sometimes gets it wrong (e.g., short-circuiting case expressions).
- `1 IN (0, NULL)` is `NULL`. That one makes some sense when you interpret the `NULL`s in the input and output as `UNKNOWN`. Alas, that's not really how `NULL`s work elsewhere: `1 in [0, NULL]` is `false`, `if(NULL > 1, 2, 3)` returns `3`, and most aggregate functions ignore  `NULL`s too even though, for example, the sum of `UNKNOWN` and `1` would be `UNKNOWN`, not `1`.
- `concat(x, NULL) = x` (same for `string_concat` and `list_concat`). More gratuitous `NULL` ignoring behavior; you can blame this one on PostgreSQL. If you prefer `NULL`s in, `NULL`s out, use `x || NULL`.
- `age(x)` is `current_date - x` instead of `current_timestamp - x`. PostgreSQL did it first. We have no explanation.

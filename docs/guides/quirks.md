Like any language, framework, or interface out there, DuckDB is not without quirks, idiosyncrasies, and inconsistencies.  

Some of these are unavoidable because we strive to adhere to the SQL Standard and, as a general but not absolute rule, to PostgreSQL's dialect specifically (see the [PostgreSQL compatibility]() page for exceptions).

Some are vestiges of our feathered friend's evolution, and the benefit of righting them has not been deemed worth the pain of migration (yet).

Finally, some are simply of the type that programmers like to start holy wars about, and while we may have our reasons for choices made, we acknowledge they can sometimes be contentious, or at the least, non-obvious.

In this sense, we provide below a list of examples that may be surprising to some, in the hope that you don't run into them unprepared while investigating a misbehaving multi-page query on a terrabyte of data: 

- The aggregate functions `sum()` and `list()` return `NULL` instead of `0` and `[]`, respectively, for empty groups. The SQL Standard commands, we obey.
- One-based indexing (e.g., arrays, strings, window functions (`row_number()`, `rank()`, `dense_rank`). The SQL Standard dictates, we comply. 
- `age(x) = current_date - x` instead of `current_timestamp - x`. PostgreSQL did it first. We have no explanation.
- `1 = true` is common, but `'t' = true` was inherited from PostgreSQL. 
- `'NaN'::FLOAT = 'NaN'::FLOAT` and `'NaN'::FLOAT > 3` violate IEEE-754 but are necessary for a total order, which is crucial in SQL (also, beware the consequences for `greatest`/`least`/`ORDER BY`)
- `concat(x, NULL) = x` (same for `string_concat` and `list_concat`). You can blame this one on PostgreSQL. If you prefer `NULL`s in, `NULL`s out, use `x || NULL`.
- Case insensitivity and the resulting inability to `SELECT A FROM 'file.parquet'` when both cases are in the file. That's actually a DuckDB thing. Great when not working with external data, you shoudln't want to need to remember the correct capitalization to avoid gettign the wrong data. 
- Automatic column deduplication. You thought `SELECT A FROM (SELECT *, 1 AS A FROM tbl)` will give you a bunch of `1`s? Think again, and remember the previous point. 
- `list_extract` / `map_extract` return `NULL` on non-existing keys, `struct_extract` throws. The former follows has PostgreSQL precedence. The latter makes sense because keys of structs are like columns. 
- USING SAMPLE precedence rules
- `SELECT CASE WHEN 0 > 1 THEN (SELECT sum(range) FROM range(0, 100000000000000000)) END` never completes to return the obvious `NULL` answer. DuckDB is ducklarative, not imperative. As such, it tries hard to do optimizations for you (e.g., constant folding) but sometimes gets it wrong (e.g., short-circuiting case expressions).
- `1 IN (0, NULL)` is `NULL`. That one makes some sense. All operations including `NULL` return `NULL`, no? (Except `0 IN (0, NULL)`.). Surprising that `1 in [0, NULL]` is `false` though.

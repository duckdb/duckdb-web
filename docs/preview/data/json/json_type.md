---
layout: docu
title: JSON Type
---

DuckDB supports `json` via the `JSON` logical type.
The `JSON` logical type is interpreted as JSON, i.e., parsed, in JSON functions rather than interpreted as `VARCHAR`, i.e., a regular string (modulo the equality-comparison caveat at the bottom of this page).
All JSON creation functions return values of this type.

We also allow any of DuckDB's types to be cast to JSON, and JSON to be cast back to any of DuckDB's types, for example, to cast `JSON` to DuckDB's `STRUCT` type, run:

```sql
SELECT '{"duck": 42}'::JSON::STRUCT(duck INTEGER);
```

```text
{'duck': 42}
```

And back:

```sql
SELECT {duck: 42}::JSON;
```

```text
{"duck":42}
```

This works for our nested types as shown in the example, but also for non-nested types:

```sql
SELECT '2023-05-12'::DATE::JSON;
```

```text
"2023-05-12"
```

The only exception to this behavior is the cast from `VARCHAR` to `JSON`, which does not alter the data, but instead parses and validates the contents of the `VARCHAR` as JSON.
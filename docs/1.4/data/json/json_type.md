---
layout: docu
title: JSON Type
---

DuckDB supports `json` via the `JSON` logical type. For example:

```sql
SELECT '[1, null, {"key": "value"}]'::JSON;
```

```text
[1, null, {"key": "value"}]
```

Logically, the `JSON` type is similar to a `VARCHAR`, but with the restriction that it must be valid JSON.
Physically, the data is stored as a `VARCHAR`.

For example, you can't parse invalid JSON:

```sql
SELECT 'unquoted'::JSON;
```

```console
Conversion Error: Malformed JSON at byte 0 of input: unexpected character.  Input: "unquoted"
```

Instead, what you probably want here is `SELECT '"quoted"'::JSON`.

Since the data is stored physically as a `VARCHAR`, whitespace is significant:

```sql
SELECT '{ "a": 5 }'::JSON = '{"a":5}'::JSON;
```

```text
false
```

Please note that whitespaces are kept in roundtrips:

```sql
SELECT '{  "a":5 }'::JSON::VARCHAR
```

```text
{  "a":5 }
```

The order of keys in objects is significant:

```sql
 SELECT '{"a":1,"b":2}'::JSON = '{"b":2,"a":1}'::JSON;
```

```text
false
```

Duplicate keys are allowed in JSON objects:

```sql
SELECT '{"a":1,"a":2}'::JSON;
```

```text
{"a":1,"a":2}
```

We allow any of DuckDB's types to be cast to JSON, and JSON to be cast back to any of DuckDB's types, for example, to cast `JSON` to DuckDB's `STRUCT` type, run:

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

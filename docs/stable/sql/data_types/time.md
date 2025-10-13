---
blurb: A time instance represents the time of a day (hour, minute, second, microsecond).
layout: docu
redirect_from:
- /docs/sql/data_types/time
title: Time Types
---

The `TIME` and `TIMETZ` types specify the hour, minute, second, microsecond of a day.

| Name      | Aliases                  | Description                        |
| :-------- | :----------------------- | :--------------------------------- |
| `TIME`    | `TIME WITHOUT TIME ZONE` | Time of day                        |
| `TIMETZ`  | `TIME WITH TIME ZONE`    | Time of day, with time zone offset |
| `TIME_NS` |                          | Time of day, nanosecond precision  |

Instances can be created using the type names as a keyword, where the data must be formatted according to the ISO 8601 format (`hh:mm:ss[.zzzzzz[zzz]][+-TT[:tt]]`).

```sql
SELECT TIME '1992-09-20 11:30:00.123456';
```

```text
11:30:00.123456
```

```sql
SELECT TIMETZ '1992-09-20 11:30:00.123456';
```

```text
11:30:00.123456+00
```

```sql
SELECT TIMETZ '1992-09-20 11:30:00.123456-02:00';
```

```text
13:30:00.123456+00
```

```sql
SELECT TIMETZ '1992-09-20 11:30:00.123456+05:30';
```

```text
06:00:00.123456+00
```

```sql
SELECT '15:30:00.123456789'::TIME_NS;
```

```text
15:30:00.123456789
```

`TIME_NS` values can also be read from Parquet when the type is [`TIME` with unit `NANOS`](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#time).

> Warning The `TIME` type should only be used in rare cases, where the date part of the timestamp can be disregarded.
> Most applications should use the [`TIMESTAMP` types]({% link docs/stable/sql/data_types/timestamp.md %}) to represent their timestamps.

---
layout: docu
title: Timestamp Types
blurb: Timestamps represent points in time.
---

Timestamps represent points in time and are internally stored as the `INT64` number of seconds / milliseconds / microseconds / nanoseconds since `1970-01-01 00:00:00+00`, depending on the chosen variant. Informally speaking, they contain both [`DATE`]({% link docs/sql/data_types/date.md %}) (year, month, day) and [`TIME`]({% link docs/sql/data_types/time.md %}) (hour, minute, second, microsecond or nanosecond) information. 

## Timestamp Types

| Name | Aliases | Description |
|:---|:---|:---|
| `TIMESTAMP_NS` |                                           | timestamp with nanosecond precision (local semantics)    |
| `TIMESTAMP`    | `DATETIME`, `TIMESTAMP WITHOUT TIME ZONE` | timestamp with microsecond precision (local semantics)   |
| `TIMESTAMP_MS` |                                           | timestamp with millisecond precision (local semantics)   |
| `TIMESTAMP_S`  |                                           | timestamp with second precision (local semantics)        |
| `TIMESTAMPTZ`  | `TIMESTAMP WITH TIME ZONE`                | timestamp with microsecond precision (instant semantics) |

> Warning Since there is not currently a `TIMESTAMP_NS WITH TIME ZONE` data type, external columns with nano-second precision and instant semantics, e.g., [parquet timestamp columns with `isAdjustedToUTC=true`](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#instant-semantics-timestamps-normalized-to-utc), lose precision when read using DuckDB.

Timestamps can be created using the `TIMESTAMP` keyword (or its variants), where the data must be formatted according to the ISO 8601 format (`YYYY-MM-DD hh:mm:ss[.zzzzzz][+-TT[:tt]]` (three extra decimal places supported by `TIMESTAMP_NS`). Decimal places beyond the targeted sub-second precision are ignored.

The `WITH TIME ZONE` data types exhibit *instant* semantics, which means that they represent points in absolute time, called *instants*, and are *displayed* in the system or a configured time zone. They require the [ICU extension]({% link docs/extensions/icu.md %}) to be installed. The `WITHOUT TIME ZONE` data types exhibit *local* semantics, which means they represent a local value of time for an unspecified observer. As such, a `WITHOUT TIME ZONE` data type together *with* a time zone defines an *instant* that can be stored in a `WITH TIME ZONE` data type:

```sql
SELECT timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40')
```

```text
2001-02-17 04:38:40+01  
```

Note that `WITH TIMEZONE` is a slight misnomer, however, since no time zone is actually stored in this data type: The computation above determines the *instant* at which an observer in the `'America/Denver'` time zone would observe the local time `2001-02-16 20:38:40`. The result is stored as microseconds since `1970-01-01 00:00:00+00` and *displayed* in the system time zone or the time zone configured via `SET TimeZone`, which is `'Europe/Berlin'` in the example above. Note that the offsets of `'America/Denver'` and `'Europe/Berlin'` with respect to Coordinated Universal Time (UTC) at the given instant are `-07:00` and `+01:00`, respectively.

In the opposite direction, we can extract the *local* time for an observer in a given time zone at a given *instant*:

```sql
SELECT timezone('America/Denver', TIMESTAMPTZ '2001-02-16 04:38:40+01')
```

```text
2001-02-16 20:38:40
```

Note that the displayed value is now independent of the system or configured time zone, since it specifically represents a local value of time without time zone information. 
Even though no physical information is lost in the above conversion, the logical information that the timestamp was one observed in `'America/Denver'` is lost. Converting `2001-02-16 20:38:40` back to the original *instant* requires the time zone information.

The difference between *local* and *instant* semantics also affects timestamp arithmetic, most notably when timestamps cross daylight saving time boundaries.

> Warning It is possible to convert between `WITH TIME ZONE` and `WITHOUT TIME ZONE` types using regular explicit and even implicit casts. These conversions perform the same computation as the `timezone` function above, but using the system or configured time zone.

> Bestpractice If in doubt, use `WITH TIME ZONE` data types to process and store timestamp data. If you prefer that your data be *displayed* in a specific timezone that is not your system time zone, you may configure that time zone using `SET TimeZone`. If you interact with external tooling that doesn't handle time zone offsets properly, consider using the `timezone` function above to convert your data to local `WITHOUT TIME ZONE` timestamps in a fixed time zone as the last step before leaving DuckDB.

> Tip To avoid surprises from implicit conversions and avoid having to think about *local* and *instant* semantics altogether, you may set `SET TimeZone='UTC'`. All computations will then be performed in UTC. For example, there will be no special casing of Daylight Saving Times and all displayed timestamps, whether stored in `WITH TIME ZONE` or `WITHOUT TIME ZONE` columns will be interpretable as time in UTC. You should still prefer `WITH TIME ZONE` data types to ensure your data is interpreted correctly when exported to external formats or when shared with users that don't set their time zone to `'UTC'`. 

### Examples

```sql
SELECT TIMESTAMP_NS '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456789
```

```sql
SELECT TIMESTAMP '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456
```

```sql
SELECT DATETIME '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456
```

```sql
SELECT TIMESTAMP_MS '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123
```

```sql
SELECT TIMESTAMP_S '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00
```

```sql
SELECT TIMESTAMPTZ '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456+00
```

```sql
SELECT TIMESTAMP WITH TIME ZONE '1992-09-20 11:30:00.123456789';
```

```text
1992-09-20 11:30:00.123456+00
```

## Special Values

There are also three special date values that can be used on input:


| Input string | Valid types                | Description                                    |
|:-------------|:---------------------------|:-----------------------------------------------|
| `epoch`      | `TIMESTAMP`, `TIMESTAMPTZ` | 1970-01-01 00:00:00+00 (Unix system time zero) |
| `infinity`   | `TIMESTAMP`, `TIMESTAMPTZ` | later than all other time stamps               |
| `-infinity`  | `TIMESTAMP`, `TIMESTAMPTZ` | earlier than all other time stamps             |

The values `infinity` and `-infinity` are specially represented inside the system and will be displayed unchanged;
but `epoch` is simply a notational shorthand that will be converted to the time stamp value when read.

```sql
SELECT '-infinity'::TIMESTAMP, 'epoch'::TIMESTAMP, 'infinity'::TIMESTAMP;
```


| Negative  | Epoch               | Positive |
|:----------|:--------------------|:---------|
| -infinity | 1970-01-01 00:00:00 | infinity |

## Functions

See [Timestamp Functions]({% link docs/sql/functions/timestamp.md %}).

## Time Zones

The `TIMESTAMPTZ` type can be binned into calendar and clock bins using a suitable extension.
The built-in [ICU extension]({% link docs/extensions/icu.md %}) implements all the binning and arithmetic functions using the
[International Components for Unicode](https://icu.unicode.org) time zone and calendar functions.

To set the time zone to use, first load the ICU extension. The ICU extension comes pre-bundled with several DuckDB clients (including Python, R, JDBC, and ODBC), so this step can be skipped in those cases. In other cases you might first need to install and load the ICU extension.

```sql
INSTALL icu;
LOAD icu;
```

Next, use the `SET TimeZone` command:

```sql
SET TimeZone = 'America/Los_Angeles';
```

Time binning operations for `TIMESTAMPTZ` will then be implemented using the given time zone.

A list of available time zones can be pulled from the `pg_timezone_names()` table function:

```sql
SELECT
    name,
    abbrev,
    utc_offset
FROM pg_timezone_names()
ORDER BY
    name;
```

You can also find a reference table of [available time zones]({% link docs/sql/data_types/timezones.md %}).

## Calendars

The [ICU extension]({% link docs/extensions/icu.md %}) also supports non-Gregorian calendars using the `SET Calendar` command.
Note that the `INSTALL` and `LOAD` steps are only required if the DuckDB client does not bundle the ICU extension.

```sql
INSTALL icu;
LOAD icu;
SET Calendar = 'japanese';
```

Time binning operations for `TIMESTAMPTZ` will then be implemented using the given calendar.
In this example, the `era` part will now report the Japanese imperial era number.

A list of available calendars can be pulled from the `icu_calendar_names()` table function:

```sql
SELECT name
FROM icu_calendar_names()
ORDER BY 1;
```

## Settings

The current value of the `TimeZone` and `Calendar` settings are determined by ICU when it starts up.
They can be queried from in the `duckdb_settings()` table function:

```sql
SELECT *
FROM duckdb_settings()
WHERE name = 'TimeZone';
```

|   name   |      value       |      description      | input_type |
|----------|------------------|-----------------------|------------|
| TimeZone | Europe/Amsterdam | The current time zone | VARCHAR    |

```sql
SELECT *
FROM duckdb_settings()
WHERE name = 'Calendar';
```

|   name   |   value   |     description      | input_type |
|----------|-----------|----------------------|------------|
| Calendar | gregorian | The current calendar | VARCHAR    |

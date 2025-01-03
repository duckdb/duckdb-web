---
layout: docu
title: Timestamp Types
blurb: Timestamps represent points in time. 
---

Timestamps represent points in time and thus combine [`DATE`]({% link docs/sql/data_types/date.md %}) and [`TIME`]({% link docs/sql/data_types/time.md %}) information.
They can be created using the `TIMESTAMP` keyword followed by a string formatted according to the ISO 8601 format, `YYYY-MM-DD hh:mm:ss[.zzzzzzzzz][+-TT[:tt]]`, which is also the format we use in this documentation. Decimal places beyond the targeted sub-second precision are ignored.

## Timestamp Types

| Name | Aliases | Description |
|:---|:---|:---|
| `TIMESTAMP_NS` |                                           | naive timestamp with nanosecond precision              |
| `TIMESTAMP`    | `DATETIME`, `TIMESTAMP WITHOUT TIME ZONE` | naive timestamp with microsecond precision             |
| `TIMESTAMP_MS` |                                           | naive timestamp with millisecond precision             |
| `TIMESTAMP_S`  |                                           | naive timestamp with second precision                  |
| `TIMESTAMPTZ`  | `TIMESTAMP WITH TIME ZONE`                | time zone aware timestamp with microsecond precision   |

> Warning Since there is not currently a `TIMESTAMP_NS WITH TIME ZONE` data type, external columns with nano-second precision and `WITH TIME ZONE` semantics, e.g., [parquet timestamp columns with `isAdjustedToUTC=true`](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#instant-semantics-timestamps-normalized-to-utc), are converted to `TIMESTAMP WITH TIME ZONE` and thus lose precision when read using DuckDB.

DuckDB distinguishes *naive* / `WITHOUT TIME ZONE` and *time zone aware* / `WITH TIME ZONE` (of which there currently only exists `TIMESTAMP WITH TIME ZONE`) timestamps. 

Despite the name, the `TIMESTAMP WITH TIME ZONE` data type does not store time zone information or UTC offsets. Instead, it stores the `INT64` number of non-leap seconds since the Unix epoch `1970-01-01 00:00:00+00`, and thus unambiguously identifies a point, or *instant*, in absolute time. What makes `TIMESTAMP WITH TIME ZONE` *time zone aware* is that timestamp arithmetic, binning (see below), and string formatting for this type are performed in a configured time zone. The time zone used for this purpose can be configured by `SET TimeZone` (see https://duckdb.org/docs/sql/data_types/timezones.html for valid string values) and defaults to the system time zone.  

The corresponding *naive* `TIMESTAMP WITHOUT TIME ZONE` stores the same raw `INT64` data, but arithmetic, binning, and string formatting follow the straightforward rules of UTC, whose implementation is significantly easier and faster. Accordingly, timestamps could be interpreted as timestamps in UTC, but more commonly they are used to represent *local* values of time as recorded by an observer in an unspecified time zone.  It is a common data cleaning step to disambiguate such observations, which often originate from strings formatted using a _local_ binning system, which can have "holes" or "collisions" around daylight savings time transitions. To perform this data cleaning step,
the UTC offset to non-UTC strings: `2021-07-31 07:20:15 -07:00`.
The DuckDB `VARCHAR` cast operation parses these offsets correctly and will generate the corresponding instant.

Such strings can be converted to `TIMESTAMP WITHOUT TIMEZONE` values using an explicit cast. As such, it is a common data cleaning step to combine a `TIMESTAMP WITHOUT TIME ZONE` *with* a time zone specification to compute a `TIMESTAMP WITH TIME ZONE`. For this purpose, implicit or explicit casts use the configured time zone; if an alternative time zone is required, the `timezone` function can be used to convert between the two types using an arbitrary time zone specification:

```sql
SELECT
    timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40')
    timezone('America/Denver', TIMESTAMPTZ '2001-02-16 04:38:40+01:00')
```

<div class="monospace_table"></div>
| aware                     | naive               |
|--------------------------:|--------------------:|
| 2001-02-17 03:38:40+00:00 | 2001-02-15 20:38:40 |

Note that the second value, a naive `TIMESTAMP`, is displayed without time zone offset, following ISO 8601 rules for local times, while the first value, a `TIMESTAMP WITH TIME ZONE`, is displayed with the UTC offset of the configured time zone, which is `'Europe/Berlin'`. The UTC offsets of `'America/Denver'` and `'Europe/Berlin'` at the given point in absolute time are `-07:00` and `+01:00`, respectively.

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

To understand time zones and the `WITH TIME ZONE` types, it helps to start with two concepts: _instants_ and _temporal binning_.

### Instants

An instant is a point in absolute time, usually given as a count of some time increment from a fixed point in time (called the _epoch_). This is similar to how positions on the earth's surface are given using latitude and longitude relative to the equator and the Greenwich Meridian. In DuckDB, the fixed point is the Unix epoch `1970-01-01 00:00:00+00:00`, and the increment is in seconds, milliseconds, microseconds, or nanoseconds, depending on the specific data type. 

### Temporal Binning

Binning is a common practice with continuous data: A set of values is broken up into ranges and the binning maps each value to the range (or _bin_) that it falls into. _Temporal binning_ is simply applying this practice to instants, e.g., by binning instants into years, months, and days:

<img src="/images/blog/timezones/tz-instants.svg"
     alt="Time Zone Instants at the Epoch"
     width=600
     />

Temporal binning rules are complex, and generally come in two sets: _time zones_ and _calendars_.
For most tasks, the calendar will just be the widely used Gregorian calendar,
but time zones apply locale-specific rules and can vary widely.
For example, here is what the binning in the IANA `'America/Los_Angeles'` time zone looks like at the epoch:

<img src="/images/blog/timezones/tz-timezone.svg"
     alt="Two Time Zones at the Epoch"
     width=600
     />

The most common temporal binning problem occurs when daylight savings time changes.
The example below contains a daylight savings time change where the "hour" bin is two hours long.
To distinguish the two hours, another range of bins, containing the offset from UTC, is needed:

<img src="/images/blog/timezones/tz-daylight.svg"
     alt="Two Time Zones at a Daylight Savings Time transition"
     width=600
     />

### Time Zone Support

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

## Calendar Support

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

> If you find that your binning operations are not behaving as you expect, check these values and adjust them if needed.

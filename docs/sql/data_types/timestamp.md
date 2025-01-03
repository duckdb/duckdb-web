---
layout: docu
title: Timestamp Types
blurb: A timestamp specifies a combination of a date (year, month, day) and a time (hour, minute, second, microsecond or nanosecond).
---

Timestamps represent points in absolute time, usually called *instants*.
DuckDB represents instants as the number of microseconds (µs) (or nanoseconds, for `TIMESTAMP_NS`) since `1970-01-01 00:00:00+00`.

A timestamp specifies a combination of [`DATE`]({% link docs/sql/data_types/date.md %}) (year, month, day) and a [`TIME`]({% link docs/sql/data_types/time.md %}) (hour, minute, second, microsecond or nanosecond). Timestamps can be created using the `TIMESTAMP` keyword, where the data must be formatted according to the ISO 8601 format (`YYYY-MM-DD hh:mm:ss[.zzzzzz][+-TT[:tt]]` (three extra decimal places supported by `TIMESTAMP_NS`). Decimal places beyond the targeted sub-second precision are ignored.

(Note: To avoid confusion from different time notation conventions, we will be using ISO-8601 y-m-d notation in this documentation.)

## Timestamp Types

| Name | Aliases | Description |
|:---|:---|:---|
| `TIMESTAMP_NS` |                                           | timestamp with nanosecond precision (UTC)              |
| `TIMESTAMP`    | `DATETIME`, `TIMESTAMP WITHOUT TIME ZONE` | timestamp with microsecond precision (UTC)             |
| `TIMESTAMP_MS` |                                           | timestamp with millisecond precision (UTC)             |
| `TIMESTAMP_S`  |                                           | timestamp with second precision (UTC)                  |
| `TIMESTAMPTZ`  | `TIMESTAMP WITH TIME ZONE`                | timestamp with microsecond precision (time-zone aware) |

> Since there is not currently a `TIMESTAMP_NS WITH TIME ZONE` data type, external columns with nano-second precision and "instant semantics", e.g., [parquet timestamp columns with `isAdjustedToUTC=true`](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#instant-semantics-timestamps-normalized-to-utc), lose precision when read using DuckDB.

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

A common claim is that database time is "stored in UTC", but in reality, databases store instants. An instant is a point in universal time, usually given as a count of some time increment from a fixed point in time (called the _epoch_). This is similar to how positions on the earth's surface are given using latitude and longitude relative to the equator and the Greenwich Meridian. In DuckDB, the fixed point is the Unix epoch `1970-01-01 00:00:00 +00:00`, and the increment is microseconds (µs). 

### Temporal Binning

Binning is a common practice with continuous data: A set of values is broken up into ranges and the binning maps each value to the range (or _bin_) that it falls into. _Temporal binning_ is simply applying this practice to instants:

<img src="/images/blog/timezones/tz-instants.svg"
     alt="Time Zone Instants at the Epoch"
     width=600
     />

Temporal binning rules are complex, and generally come in two sets: _time zones_ and _calendars_.
For most tasks, the calendar will just be the widely used Gregorian calendar,
but time zones apply locale-specific rules and can vary widely.
For example, here is what the binning from the UTC time zone looks like at the epoch:

<img src="/images/blog/timezones/tz-timezone.svg"
     alt="Two Time Zones at the Epoch"
     width=600
     />

The most common temporal binning problem occurs when daylight savings time changes.
This example contains a daylight savings time change where the "hour" bin is two hours long.
To distinguish the two hours, another bin containing the offset from UTC is needed:

<img src="/images/blog/timezones/tz-daylight.svg"
     alt="Two Time Zones at a Daylight Savings Time transition"
     width=600
     />

This illustrates why temporal data should always be stored as instants. 
For more on this subject, see the section on "naïve timestamps" below. 

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

## Naïve Timestamps

Timestamp values are sometimes created from a string formatted using a _local_ binning system instead of one that can represent instants.
This results in the column values being offset from UTC, which can cause problems with daylight savings time.
More generally, such string representations can have "holes" or "collisions" around DST transitions.
These values are called *naïve* timestamps, and often constitute a data cleaning problem.

A simple way to avoid this situation going forward is to add the UTC offset to non-UTC strings: `2021-07-31 07:20:15 -07:00`.
The DuckDB `VARCHAR` cast operation parses these offsets correctly and will generate the corresponding instant.


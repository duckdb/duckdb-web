---
blurb: Timestamps represent points in time.
layout: docu
title: Timestamp Types
---

Timestamps represent points in time. As such, they combine [`DATE`]({% link docs/preview/sql/data_types/date.md %}) and [`TIME`]({% link docs/preview/sql/data_types/time.md %}) information.
They can be created using the type name followed by a string formatted according to the ISO 8601 format, `YYYY-MM-DD hh:mm:ss[.zzzzzzzzz][+-TT[:tt]]`, which is also the format we use in this documentation. Decimal places beyond the supported precision are ignored.

## Timestamp Types

| Name | Aliases | Description |
|:---|:---|:---|
| `TIMESTAMP_NS` |                                           | Naive timestamp with nanosecond precision              |
| `TIMESTAMP`    | `DATETIME`, `TIMESTAMP WITHOUT TIME ZONE` | Naive timestamp with microsecond precision             |
| `TIMESTAMP_MS` |                                           | Naive timestamp with millisecond precision             |
| `TIMESTAMP_S`  |                                           | Naive timestamp with second precision                  |
| `TIMESTAMPTZ`  | `TIMESTAMP WITH TIME ZONE`                | Time zone aware timestamp with microsecond precision   |

> Warning Since there is not currently a `TIMESTAMP_NS WITH TIME ZONE` data type, external columns with nanosecond precision and `WITH TIME ZONE` semantics, e.g., [Parquet timestamp columns with `isAdjustedToUTC=true`](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#instant-semantics-timestamps-normalized-to-utc), are converted to `TIMESTAMP WITH TIME ZONE` and thus lose precision when read using DuckDB.

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
SELECT TIMESTAMPTZ '1992-09-20 12:30:00.123456789+01:00';
```

```text
1992-09-20 11:30:00.123456+00
```

DuckDB distinguishes timestamps `WITHOUT TIME ZONE` and `WITH TIME ZONE` (of which the only current representative is `TIMESTAMP WITH TIME ZONE`).

Despite the name, a `TIMESTAMP WITH TIME ZONE` does not store time zone information. Instead, it only stores the `INT64` number of non-leap microseconds since the Unix epoch `1970-01-01 00:00:00+00`, and thus unambiguously identifies a point in absolute time, or [*instant*]({% link docs/preview/sql/data_types/timestamp.md %}#instants). The reason for the labels *time zone aware* and `WITH TIME ZONE` is that timestamp arithmetic, [*binning*]({% link docs/preview/sql/data_types/timestamp.md %}#temporal-binning), and string formatting for this type are performed in a [configured time zone]({% link docs/preview/sql/data_types/timestamp.md %}#time-zone-support), which defaults to the system time zone and is just `UTC+00:00` in the examples above.

The corresponding `TIMESTAMP WITHOUT TIME ZONE` stores the same `INT64`, but arithmetic, binning and string formatting follow the straightforward rules of Coordinated Universal Time (UTC) without offsets or time zones. Accordingly, `TIMESTAMP`s could be interpreted as UTC timestamps, but more commonly they are used to represent *local* observations of time recorded in an unspecified time zone, and operations on these types can be interpreted as simply manipulating tuple fields following nominal temporal logic.
It is a common data cleaning problem to disambiguate such observations, which may also be stored in raw strings without time zone specification or UTC offsets, into unambiguous `TIMESTAMP WITH TIME ZONE` instants. One possible solution to this is to append UTC offsets to strings, followed by an explicit cast to `TIMESTAMP WITH TIME ZONE`. Alternatively, a `TIMESTAMP WITHOUT TIME ZONE` may be created first and then be combined with a time zone specification to obtain a time zone aware `TIMESTAMP WITH TIME ZONE`.

## Conversion between Strings and Naïve / Time Zone-Aware Timestamps

The conversion between strings *without* UTC offsets or IANA time zone names and `WITHOUT TIME ZONE` types is unambiguous and straightforward.
The conversion between strings *with* UTC offsets or time zone names and `WITH TIME ZONE` types is also unambiguous, but requires the `ICU` extension to handle time zone names.

When strings *without* UTC offsets or time zone names are converted to a `WITH TIME ZONE` type, the string is interpreted in the configured time zone. 
When strings with UTC offsets are passed to a `WITHOUT TIME ZONE` type, the offsets or time zone specifications are ignored.
When strings with time zone names other than `UTC` are passed to a `WITHOUT TIME ZONE` type, an error is thrown. 

Finally, when `WITH TIME ZONE` and `WITHOUT TIME ZONE` types are converted to each other via explicit or implicit casts, the translation uses the configured time zone. To use an alternative time zone, the `timezone` function provided by the `ICU` extension may be used:

```sql
SELECT
    timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40') AS aware1,
    timezone('America/Denver', TIMESTAMPTZ '2001-02-16 04:38:40') AS naive1,
    timezone('UTC', TIMESTAMP '2001-02-16 20:38:40+00:00') AS aware2,
    timezone('UTC', TIMESTAMPTZ '2001-02-16 04:38:40 Europe/Berlin') AS naive2;
```

<div class="monospace_table"></div>

|         aware1         |       naive1        |         aware2         |       naive2        |
|------------------------|---------------------|------------------------|---------------------|
| 2001-02-17 04:38:40+01 | 2001-02-15 20:38:40 | 2001-02-16 21:38:40+01 | 2001-02-16 03:38:40 |

Note that `TIMESTAMP`s are displayed without time zone specification in the results, following ISO 8601 rules for local times, while time-zone aware `TIMESTAMPTZ`s are displayed with the UTC offset of the configured time zone, which is `'Europe/Berlin'` in the example. The UTC offsets of `'America/Denver'` and `'Europe/Berlin'` at all involved instants are `-07:00` and `+01:00`, respectively.

## Special Values

Three special strings can be used to create timestamps:

| Input string | Description                                      |
|:-------------|:-------------------------------------------------|
| `epoch`      | 1970-01-01 00:00:00[+00] (Unix system time zero) |
| `infinity`   | Later than all other timestamps                  |
| `-infinity`  | Earlier than all other timestamps                |

The values `infinity` and `-infinity` are special cased and are displayed unchanged, whereas the value `epoch` is simply a notational shorthand that is converted to the corresponding timestamp value when read.

```sql
SELECT '-infinity'::TIMESTAMP, 'epoch'::TIMESTAMP, 'infinity'::TIMESTAMP;
```

| Negative  | Epoch               | Positive |
|:----------|:--------------------|:---------|
| -infinity | 1970-01-01 00:00:00 | infinity |

## Functions

See [Timestamp Functions]({% link docs/preview/sql/functions/timestamp.md %}).

## Time Zones

To understand time zones and the `WITH TIME ZONE` types, it helps to start with two concepts: *instants* and *temporal binning*.

### Instants

An instant is a point in absolute time, usually given as a count of some time increment from a fixed point in time (called the *epoch*). This is similar to how positions on the earth's surface are given using latitude and longitude relative to the equator and the Greenwich Meridian. In DuckDB, the fixed point is the Unix epoch `1970-01-01 00:00:00+00:00`, and the increment is in seconds, milliseconds, microseconds, or nanoseconds, depending on the specific data type.

### Temporal Binning

Binning is a common practice with continuous data: A range of possible values is broken up into contiguous subsets and the binning operation maps actual values to the *bin* they fall into. *Temporal binning* is simply applying this practice to instants; for example, by binning instants into years, months and days.

<img src="/images/blog/timezones/tz-instants-light.svg"
     alt="Time Zone Instants at the Epoch"
     width="600"
     class="lightmode-img"
     />
<img src="/images/blog/timezones/tz-instants-dark.svg"
     alt="Time Zone Instants at the Epoch"
     width="600"
     class="darkmode-img"
     />

Temporal binning rules are complex, and generally come in two sets: *time zones* and *calendars*.
For most tasks, the calendar will just be the widely used Gregorian calendar,
but time zones apply locale-specific rules and can vary widely.
For example, here is what binning for the `'America/Los_Angeles'` time zone looks like near the epoch:

<img src="/images/blog/timezones/tz-timezone-light.svg"
     alt="Two Time Zones at the Epoch"
     width="600"
     class="lightmode-img"
     />
<img src="/images/blog/timezones/tz-timezone-dark.svg"
     alt="Two Time Zones at the Epoch"
     width="600"
     class="darkmode-img"
     />

The most common temporal binning problem occurs when daylight saving time changes.
The example below contains a daylight saving time change where the "hour" bin is two hours long.
To distinguish the two hours, another range of bins containing the offset from UTC is needed:

<img src="/images/blog/timezones/tz-daylight-light.svg"
     alt="Two Time Zones at a Daylight Savings Time transition"
     width="600"
     class="lightmode-img"
     />
<img src="/images/blog/timezones/tz-daylight-dark.svg"
     alt="Two Time Zones at a Daylight Savings Time transition"
     width="600"
     class="darkmode-img"
     />

### Time Zone Support

The `TIMESTAMPTZ` type can be binned into calendar and clock bins using a suitable extension.
The built-in [ICU extension]({% link docs/preview/core_extensions/icu.md %}) implements all the binning and arithmetic functions using the
[International Components for Unicode](https://icu.unicode.org) time zone and calendar functions.

To set the time zone to use, first load the ICU extension. The ICU extension comes pre-bundled with several DuckDB clients (including Python, R, JDBC and ODBC), so this step can be skipped in those cases. In other cases you might first need to install and load the ICU extension.

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

You can also find a reference table of [available time zones]({% link docs/preview/sql/data_types/timezones.md %}).

## Calendar Support

The [ICU extension]({% link docs/preview/core_extensions/icu.md %}) also supports non-Gregorian calendars using the `SET Calendar` command.
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

> If you find that your binning operations are not behaving as you expect, check the `TimeZone` and `Calendar` values and adjust them if needed.

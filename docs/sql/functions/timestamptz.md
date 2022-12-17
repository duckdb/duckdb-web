---
layout: docu
title: Timestamp With Time Zone Functions
selected: Documentation/Functions/Timestamp With Time Zone Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating `TIMESTAMP WITH TIME ZONE` values.

Despite the name, these values do not store a time zone - just an instant like `TIMESTAMP`.
Instead, they request that the instant be binned and formatted using the current time zone.

Time zone support is not built in but can be provided by an extension,
such as the ICU extension that ships with DuckDB.

In the examples below, the current time zone is presumed to be America/Los_Angeles
using the Gregorian calendar.

## Built-in Timestamp With Time Zone Functions

The table below shows the available scalar functions for `TIMESTAMP WITH TIME ZONE` values.
Since these functions do not involve binning or display,
they are always available.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `current_timestamp` | Current date and time (start of current transaction) | `current_timestamp` | `2022-10-08 12:44:46.122-07` |
| `get_current_timestamp()` | Current date and time (start of current transaction) | `get_current_timestamp()` | `2022-10-08 12:44:46.122-07` |
| `greatest(`*`timestamptz`*`, `*`timestamptz`*`)` | The later of two timestamps | `greatest(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` | `1992-09-20 20:38:48-07` |
| `isfinite(`*`timestamptz`*`)` | Returns true if the timestamp with time zone is finite, false otherwise | `isfinite(TIMESTAMPTZ '1992-03-07')` | true |
| `isinf(`*`timestamptz`*`)` | Returns true if the timestamp with time zone is infinite, false otherwise | `isinf(TIMESTAMPTZ '-infinity')` | true |
| `least(`*`timestamptz`*`, `*`timestamptz`*`)` | The earlier of two timestamps | `least(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` | `1992-03-22 01:02:03.1234-08` |
| `now()` | Current date and time (start of current transaction) | `now()` | `2022-10-08 12:44:46.122-07`|
| `transaction_timestamp()` | Current date and time (start of current transaction) | `transaction_timestamp()` | `2022-10-08 12:44:46.122-07`|

## Timestamp With Time Zone Strings
With no time zone extension loaded, `TIMESTAMPTZ` values will be cast to and from strings
using offset notation.
This will let you specify an instant correctly without access to time zone information.
Without a time zone extension, `TIMESTAMPTZ` values will be displayed using GMT offsets:

```sql
select '2022-10-08 13:13:34-07'::TIMESTAMPTZ'
-- 2022-10-08 20:13:34+00
```

If a time zone extension such as ICU is loaded, then a time zone can be parsed from a string
and cast to a representation in the local time zone:

```sql
select '2022-10-08 13:13:34 Europe/Amsterdam'::TIMESTAMPTZ::VARCHAR;
-- 2022-10-08 04:13:34-07
```

## ICU Timestamp With Time Zone Operators
The table below shows the available mathematical operators for `TIMESTAMP WITH TIME ZONE` values
provided by the ICU extension.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `+` | addition of an `INTERVAL` | `TIMESTAMPTZ '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `-` | subtraction of `TIMESTAMPTZ`s | `TIMESTAMPTZ '1992-03-27' - TIMESTAMPTZ '1992-03-22'` | `5 days` |
| `-` | subtraction of an `INTERVAL` | `TIMESTAMPTZ '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |

Adding to or subtracting from [infinite values](../../sql/data_types/timestamp#special-values) produces the same infinite value.

## ICU Timestamp With Time Zone Functions
The table below shows the ICU provided scalar functions for `TIMESTAMP WITH TIME ZONE` values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `age(`*`timestamptz`*`, `*`timestamptz`*`)` | Subtract arguments, resulting in the time difference between the two timestamps | `age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20')` | `8 years 6 months 20 days` |
| `age(`*`timestamptz`*`)` | Subtract from current_date | `age(TIMESTAMP '1992-09-20')` | `29 years 1 month 27 days 12:39:00.844` |
| `date_diff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of [partition](../../sql/functions/datepart) boundaries between the timestamps | `date_diff('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` | `2` |
| `datediff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_diff. The number of [partition](../../sql/functions/datepart) boundaries between the timestamps | `datediff('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` | `2` |
| `date_part(`*`part`*`, `*`timestamptz`*`)` | Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `date_part('minute', TIMESTAMPTZ '1992-09-20 20:38:40')` | `38` |
| `datepart(`*`part`*`, `*`timestamptz`*`)` | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `datepart('minute', TIMESTAMPTZ '1992-09-20 20:38:40')` | `38` |
| `date_part([`*`part`*`, ...], `*`timestamptz`*`)` | Get the listed [subfields](../../sql/functions/datepart) as a `struct`. The list must be constant. | `date_part(['year', 'month', 'day'], TIMESTAMPTZ '1992-09-20 20:38:40-07')` | `{year: 1992, month: 9, day: 20}` |
| `datepart([`*`part`*`, ...], `*`timestamptz`*`)` | Alias of date_part. Get the listed [subfields](../../sql/functions/datepart) as a `struct`. The list must be constant. | `datepart(['year', 'month', 'day'], TIMESTAMPTZ '1992-09-20 20:38:40-07')` | `{year: 1992, month: 9, day: 20}` |
| `date_sub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of complete [partitions](../../sql/functions/datepart) between the timestamps | `date_sub('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` | `1` |
| `datesub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_sub. The number of complete [partitions](../../sql/functions/datepart) between the timestamps | `datesub('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` | `1` |
| `date_trunc(`*`part`*`, `*`timestamptz`*`)` | Truncate to specified [precision](../../sql/functions/datepart) | `date_trunc('hour', TIMESTAMPTZ '1992-09-20 20:38:40')` | `1992-09-20 20:00:00` |
| `datetrunc(`*`part`*`, `*`timestamptz`*`)` | Alias of date_trunc. Truncate to specified [precision](../../sql/functions/datepart) | `datetrunc('hour', TIMESTAMPTZ '1992-09-20 20:38:40')` | `1992-09-20 20:00:00` |
| `extract(`*`field`* `from` *`timestamptz`*`)` | Get [subfield](../../sql/functions/datepart) from a timestamp with time zone | `extract('hour' FROM TIMESTAMPTZ '1992-09-20 20:38:48')` | `20` |
| `last_day(`*`timestamptz`*`)` | The last day of the month. | `last_day(TIMESTAMPTZ '1992-03-22 01:02:03.1234')` | `1992-03-31` |
| `make_timestamptz(`*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`double`*`)` | The timestamp with time zone for the given parts in the current time zone | `make_timestamptz(1992, 9, 20, 13, 34, 27.123456)` | `1992-09-20 13:34:27.123456-07` |
| `make_timestamptz(`*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`double`*`, `*`string`*`)` | The timestamp with time zone for the given parts and time zone | `make_timestamptz(1992, 9, 20, 15, 34, 27.123456, 'CET')` | `1992-09-20 05:34:27.123456-07` |
| `strftime(`*`timestamptz`*`, `*`format`*`)` | Converts timestamp with time zone to string according to the [format string](../../sql/functions/dateformat) | `strftime(timestamptz '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` | `Wed, 1 January 1992 - 08:38:40 PM` |
| `strptime(`*`text`*`, `*`format`*`)` | Converts string to timestamp with time zone according to the [format string](../../sql/functions/dateformat) if `%Z` is specified. | `strptime('Wed, 1 January 1992 - 08:38:40 PST', '%a, %-d %B %Y - %H:%M:%S %Z')` | `1992-01-01 08:38:40-08` |
| `timezone(`*`text`*`, `*`timestamp`*`)` | Use the [date parts](../../sql/functions/datepart) of the timestamp to construct a timestamp in the given time zone. Effectively, the argument is a "local" time. | `timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40')` | `2001-02-16 19:38:40-08` |
| `timezone(`*`text`*`, `*`timestamptz`*`)` | Use the [date parts](../../sql/functions/datepart) of the timestamp in the given time zone to construct a timestamp. Effectively, the result is a "local" time. | `timezone('America/Denver', TIMESTAMPTZ '2001-02-16 20:38:40-05')` | `2001-02-16 18:38:40` |

There are also dedicated extraction functions to get the [subfields](../../sql/functions/datepart).

### Infinities

Functions applied to infinite dates will either return the same infinite dates
(e.g, `greatest`) or `NULL` (e.g., `date_part`) depending on what "makes sense".
In general, if the function needs to examine the parts of the infinite temporal value,
the result will be `NULL`.

### At Time Zone

The `AT TIME ZONE` syntax is syntactic sugar for the (two argument) `timezone` function listed above:

```sql
timestamp '2001-02-16 20:38:40' AT TIME ZONE 'America/Denver'
-- 2001-02-16 19:38:40-08
timestamp with time zone '2001-02-16 20:38:40-05' AT TIME ZONE 'America/Denver'
-- 2001-02-16 18:38:40
```

These operations are intended to allow queries to work with "local" timestamps.
A local timestamp is effectively a way of encoding the part values from a time zone into a single value.
They should be used with caution because the produced values can contain gaps and ambiguities thanks to daylight savings time.
Often the same functionality can be implemented more reliably using the `struct` variant of the `date_part` function.

## Calendars

The ICU extension also supports [non-Gregorian calendars](../../sql/data_types/timestamp#calendars).
If such a calendar is current, then the display and binning operations will use that calendar.

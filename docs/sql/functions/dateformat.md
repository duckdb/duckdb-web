---
layout: docu
title: Date Format Functions
---

The `strftime` and `strptime` functions can be used to convert between dates/timestamps and strings. This is often required when parsing CSV files, displaying output to the user or transferring information between programs. Because there are many possible date representations, these functions accept a format string that describes how the date or timestamp should be structured.

## strftime Examples

`strftime(timestamp, format)` converts timestamps or dates to strings according to the specified pattern.

```sql
SELECT strftime(DATE '1992-03-02', '%d/%m/%Y');
-- 02/03/1992
```
```sql
SELECT strftime(TIMESTAMP '1992-03-02 20:32:45', '%A, %-d %B %Y - %I:%M:%S %p');
-- Monday, 2 March 1992 - 08:32:45 PM
```

## strptime Examples

`strptime(string, format)` converts strings to timestamps according to the specified pattern.

```sql
SELECT strptime('02/03/1992', '%d/%m/%Y');
-- 1992-03-02 00:00:00
```
```sql
SELECT strptime('Monday, 2 March 1992 - 08:32:45 PM', '%A, %-d %B %Y - %I:%M:%S %p');
-- 1992-03-02 20:32:45
```

## CSV Parsing

The date formats can also be specified during CSV parsing, either in the [`COPY` statement](../statements/copy) or in the `read_csv` function. This can be done by either specifying a `DATEFORMAT` or a `TIMESTAMPFORMAT` (or both). `DATEFORMAT` will be used for converting dates, and `TIMESTAMPFORMAT` will be used for converting timestamps. Below are some examples for how to use this:

```sql
-- in COPY statement
COPY dates FROM 'test.csv' (DATEFORMAT '%d/%m/%Y', TIMESTAMPFORMAT '%A, %-d %B %Y - %I:%M:%S %p');
```
```sql
-- in read_csv function
SELECT * FROM read_csv('test.csv', dateformat = '%m/%d/%Y');
```

## Format Specifiers

Below is a full list of all available format specifiers.

<div class="narrow_table"></div>

| Specifier | Description | Example |
|:-|:------|:---|
| `%a` | Abbreviated weekday name. | Sun, Mon, ... |
| `%A` | Full weekday name. | Sunday, Monday, ... |
| `%b` | Abbreviated month name. | Jan, Feb, ..., Dec |
| `%B` | Full month name. | January, February, ... |
| `%c` | ISO date and time representation | 1992-03-02 10:30:20 |
| `%d` | Day of the month as a zero-padded decimal. | 01, 02, ..., 31 |
| `%-d` | Day of the month as a decimal number. | 1, 2, ..., 30 |
| `%f` | Microsecond as a decimal number, zero-padded on the left. | 000000 - 999999 |
| `%g` | Millisecond as a decimal number, zero-padded on the left. | 000 - 999 |
| `%G` | ISO 8601 year with century representing the year that contains the greater part of the ISO week (see `%V`). | 0001, 0002, ..., 2013, 2014, ..., 9998, 9999 |
| `%H` | Hour (24-hour clock) as a zero-padded decimal number. | 00, 01, ..., 23 |
| `%-H` | Hour (24-hour clock) as a decimal number. | 0, 1, ..., 23 |
| `%I` | Hour (12-hour clock) as a zero-padded decimal number. | 01, 02, ..., 12 |
| `%-I` | Hour (12-hour clock) as a decimal number. | 1, 2, ... 12 |
| `%j` | Day of the year as a zero-padded decimal number. | 001, 002, ..., 366 |
| `%-j` | Day of the year as a decimal number. | 1, 2, ..., 366 |
| `%m` | Month as a zero-padded decimal number. | 01, 02, ..., 12 |
| `%-m` | Month as a decimal number. | 1, 2, ..., 12 |
| `%M` | Minute as a zero-padded decimal number. | 00, 01, ..., 59 |
| `%-M` | Minute as a decimal number. | 0, 1, ..., 59 |
| `%n` | Nanosecond as a decimal number, zero-padded on the left. | 000000000 - 999999999 |
| `%p` | Locale's AM or PM. | AM, PM |
| `%S` | Second as a zero-padded decimal number. | 00, 01, ..., 59 |
| `%-S` | Second as a decimal number. | 0, 1, ..., 59 |
| `%u` | ISO 8601 weekday as a decimal number where 1 is Monday. | 1, 2, ..., 7 |
| `%U` | Week number of the year. Week 01 starts on the first Sunday of the year, so there can be week 00. Note that this is not compliant with the week date standard in ISO-8601. | 00, 01, ..., 53 |
| `%V` | ISO 8601 week as a decimal number with Monday as the first day of the week. Week 01 is the week containing Jan 4. | 01, ..., 53 |
| `%w` | Weekday as a decimal number. | 0, 1, ..., 6 |
| `%W` | Week number of the year. Week 01 starts on the first Monday of the year, so there can be week 00. Note that this is not compliant with the week date standard in ISO-8601. | 00, 01, ..., 53 |
| `%x` | ISO date representation | 1992-03-02 |
| `%X` | ISO time representation | 10:30:20 |
| `%y` | Year without century as a zero-padded decimal number. | 00, 01, ..., 99 |
| `%-y` | Year without century as a decimal number. | 0, 1, ..., 99 |
| `%Y` | Year with century as a decimal number. | 2013, 2019 etc. |
| `%z` | [Time offset from UTC](https://en.wikipedia.org/wiki/ISO_8601#Time_offsets_from_UTC) in the form ±HH:MM, ±HHMM, or ±HH. | -0700 |
| `%Z` | Time zone name. | Europe/Amsterdam  |
| `%%` | A literal `%` character. | % |

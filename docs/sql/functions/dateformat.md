---
layout: docu
title: Date Format
selected: Documentation/Functions/Date Format
expanded: Functions
---

The `strftime` and `strptime` functions can be used to convert between dates/timestamps and strings. This is often required when parsing CSV files, displaying output to the user or transferring information between programs. Because there are many possible date representations, these functions accept a format string that describes how the date or timestamp should be structured.

##### strftime examples
`strftime(timestamp, format)` converts timestamps or dates to strings according to the specified pattern.

```sql
SELECT strftime(DATE '1992-03-02', '%d/%m/%Y');
-- 02/03/1992
SELECT strftime(TIMESTAMP '1992-03-02 20:32:45', '%A, %-d %B %Y - %I:%M:%S %p');
-- Monday, 2 March 1992 - 08:32:45 PM
```

##### strptime examples
`strptime(string, format)` converts strings to timestamps according to the specified pattern.

```sql
SELECT strptime('02/03/1992', '%d/%m/%Y');
-- 1992-03-02 00:00:00
SELECT strptime('Monday, 2 March 1992 - 08:32:45 PM', '%A, %-d %B %Y - %I:%M:%S %p');
-- 1992-03-02 20:32:45
```

##### CSV Parsing
The date formats can also be specified during CSV parsing, either in the `COPY` statement or in the `read_csv` function. This can be done by either specifying a `DATEFORMAT` or a `TIMESTAMPFORMAT` (or both). `DATEFORMAT` will be used for converting dates, and `TIMESTAMPFORMAT` will be used for converting timestamps. Below are some examples for how to use this:

```sql
-- in COPY statement
COPY dates FROM 'test.csv' (DATEFORMAT '%d/%m/%Y', TIMESTAMPFORMAT '%A, %-d %B %Y - %I:%M:%S %p')

-- in read_csv function
SELECT * FROM read_csv('test.csv', dateformat='%m/%d/%Y');
```

##### Format Specifiers
Below is a full list of all available format specifiers.

| Specifier | Description | Example |
|:---|:---|:---|:---|
| `%a` | Abbreviated weekday name. | Sun, Mon, ... |
| `%A` | Full weekday name. | Sunday, Monday, ... |
| `%w` | Weekday as a decimal number. | 0, 1, ..., 6 |
| `%d` | Day of the month as a zero-padded decimal. | 01, 02, ..., 31 |
| `%-d` | Day of the month as a decimal number. | 1, 2, ..., 30 |
| `%b` | Abbreviated month name. | Jan, Feb, ..., Dec |
| `%B` | Full month name. | January, February, ... |
| `%m` | Month as a zero-padded decimal number. | 01, 02, ..., 12 |
| `%-m` | Month as a decimal number. | 1, 2, ..., 12 |
| `%y` | Year without century as a zero-padded decimal number. | 00, 01, ..., 99 |
| `%-y` | Year without century as a decimal number. | 0, 1, ..., 99 |
| `%Y` | Year with century as a decimal number. | 2013, 2019 etc. |
| `%H` | Hour (24-hour clock) as a zero-padded decimal number. | 00, 01, ..., 23 |
| `%-H` | Hour (24-hour clock) as a decimal number. | 0, 1, ..., 23 |
| `%I` | Hour (12-hour clock) as a zero-padded decimal number. | 01, 02, ..., 12 |
| `%-I` | Hour (12-hour clock) as a decimal number. | 1, 2, ... 12 |
| `%p` | Locale's AM or PM. | AM, PM |
| `%M` | Minute as a zero-padded decimal number. | 00, 01, ..., 59 |
| `%-M` | Minute as a decimal number. | 0, 1, ..., 59 |
| `%S` | Second as a zero-padded decimal number. | 00, 01, ..., 59 |
| `%-S` | Second as a decimal number. | 0, 1, ..., 59 |
| `%g` | Millisecond as a decimal number, zero-padded on the left. | 000 - 999 |
| `%f` | Microsecond as a decimal number, zero-padded on the left. | 000000 - 999999 |
| `%z` | UTC offset in the form +HHMM or -HHMM. |  |
| `%Z` | Time zone name. |   |
| `%j` | Day of the year as a zero-padded decimal number. | 001, 002, ..., 366 |
| `%-j` | Day of the year as a decimal number. | 1, 2, ..., 366 |
| `%U` | Week number of the year (Sunday as the first day of the week). | 00, 01, ..., 53 |
| `%W` | Week number of the year (Monday as the first day of the week). | 00, 01, ..., 53 |
| `%c` | ISO date and time representation | 1992-03-02 10:30:20 |
| `%x` | ISO date representation | 1992-03-02 |
| `%X` | ISO time representation | 10:30:20 |
| `%%` | A literal '%' character. | % |

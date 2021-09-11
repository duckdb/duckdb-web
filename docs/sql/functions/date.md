---
layout: docu
title: Date Functions
selected: Documentation/Functions/Date Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating date values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `current_date` | Current date (start of current transaction) | | |
| `date_part(`*`part`*`, `*`date`*`)` | Get subfield (equivalent to *extract*) | `date_part('year', DATE '1992-09-20')` | 1992 |
| `date_trunc(`*`part`*`, `*`date`*`)` | Truncate to specified precision | `date_trunc('month', DATE '1992-03-07')` | 1992-03-01 |
| `extract(`*`part`* `from` *`date`*`)` | Get subfield from a date | `extract('year' FROM DATE '1992-09-20')` | 1992 |
| `strftime(date, format)` | Converts date to string according to format (see [Date Format](/docs/sql/functions/dateformat)) | `strftime(date '1992-01-01', '%a, %-d %B %Y')` | Wed, 1 January 1992 |
| `day(`*`date`*`)` | extract day from a date | `day(date '1992-02-15')` | `15` |
| `month(`*`date`*`)` | extract month from a date | `month(date '1992-02-15')` | `2` |
| `dayofyear(`*`date`*`)` | extract day of year from a date | `dayofyear(date '1992-02-15')` | `46` |
| `week(`*`date`*`)` | extract week from a date | `week(date '1992-02-15')` | `7` |
| `quarter(`*`date`*`)` | extract quarter from a date | `quarter(date '1992-02-15')` | `1` |
| `year(`*`date`*`)` | extract year from a date | `year(date '1992-02-15')` | `1992` |
| `dayofmonth(`*`date`*`)` | extract day of month from a date | `dayofmonth(date '1992-02-15')` | `15` |
| `dayname(`*`date`*`)` | extract day name from a date | `dayname(date '1992-02-15')` | `Saturday` |
| `last_day(`*`date`*`)` | extract last day of the corresponding month in the date | `last_day(date '1992-02-15')` | `1992-02-29` |
| `monthname(`*`date`*`)` | extract month name from a date | `monthname(date '1992-02-15')` | `February` |
| `weekday(`*`date`*`)` | extract week day from a date | `weekday(date '1992-02-15')` | `6` |
| `weekofyear(`*`date`*`)` | extract week of year from a date | `weekofyear(date '1992-02-15')` | `7` |
| `yearweek(`*`date`*`)` | extract year and week of year from a date | `yearweek(date '1992-02-15')` | `199207` |

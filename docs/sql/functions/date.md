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
| `strftime(date, format)` | Converts date to string according to format (see [Date Format](/docs/sql/functions/dateformat)) | strftime(date '1992-01-01', '%a, %-d %B %Y') | Wed, 1 January 1992 |

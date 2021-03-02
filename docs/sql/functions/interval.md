---
layout: docu
title: Interval Functions
selected: Documentation/Functions/Interval Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating interval values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `date_part(`*`part`*`, `*`interval`*`)` | Get subfield (equivalent to *extract*) | `date_part('year', INTERVAL '14 months')` | 1 |
| `extract(`*`part`* `from` *`interval`*`)` | Get subfield from a date | `extract('month' FROM INTERVAL '14 months')` | 2 |

All date parts are defined for intervals except `dow`, `isodow`, `doy`and `week`.

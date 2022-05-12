---
layout: docu
title: Date Types
selected: Documentation/Data Types/Date
expanded: Data Types
blurb: A date specifies a combination of year, month and day.
---
| Name   | Aliases | Description                     |
|:-------|:--------|:--------------------------------|
| `DATE` |         | calendar date (year, month day) |

A date specifies a combination of year, month and day. DuckDB follows the SQL standard's lead by counting dates exclusively in the Gregorian calendar, even for years before that calendar was in use. Dates can be created using the `DATE` keyword, where the data must be formatted according to the ISO 8601 format (`YYYY-MM-DD`).

```sql
-- 20 September, 1992
SELECT DATE '1992-09-20';
```

## Special Values

There are also three special date values that can be used on input:

| Input String | Description                       |
|:-------------|:----------------------------------|
| epoch	       | 1970-01-01 (Unix system day zero) |
| infinity	   | later than all other dates        |
| -infinity	   | earlier than all other dates      |

The values `infinity` and `-infinity` are specially represented inside the system and will be displayed unchanged; 
but `epoch` is simply a notational shorthand that will be converted to the date value when read.

```sql
SELECT '-infinity'::DATE, 'epoch'::DATE, 'infinity'::DATE;
```

| Negative  | Epoch      | Positive |
|:----------|:-----------|:---------|
| -infinity | 1970-01-01 | infinity |

## Functions
See [Date Functions](/docs/sql/functions/date).

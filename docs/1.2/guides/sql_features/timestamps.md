---
layout: docu
title: Timestamp Issues
---

## Timestamp With Time Zone Promotion Casts

Working with time zones in SQL can be quite confusing at times. 
For example, when filtering to a date range, one might try the following query:

```sql
set timezone='America/Los_Angeles';

create table times as 
    from range('2025-08-30'::TIMESTAMPTZ, '2025-08-31'::TIMESTAMPTZ, INTERVAL 1 HOUR) tbl(t);

from times where t <= '2025-08-30';
```
| t |
| timestamp with time zone |
| :--- |
| 2025-08-30 00:00:00-07 |

But if you change to another time zone, the results of the query change:

```sql
set timezone = 'HST';
from fnord where t <= '2025-08-30';
```
| t |
| timestamp with time zone |
| :--- |
| 2025-08-29 21:00:00-10 |
| 2025-08-29 22:00:00-10 |
| 2025-08-29 23:00:00-10 |
| 2025-08-30 00:00:00-10 |

or worse:

```sql
set timezone = 'America/New_York';
from times where t <= '2025-08-30';
```
| t |
| timestamp with time zone |
| ---: |
| 0 rows |

These confusing results are due to the SQL casting rules from `DATE` to `TIMESTAMP WITH TIME ZONE`.
This cast is required to promote the date to midnight _in the current time zone_. 

In general, unless you need to use the current time zone for display (or 
[other temporal binning](https://duckdb.org/2022/01/06/time-zones.html) operations) 
you should use plain `TIMESTAMP`s for temporal data.
This will avoid confusing issues such as this, and the arithmetic operations are generally faster. 

## Time Zone Performance

DuckDB uses the International Components for Unicode time library for 
[time zone support](https://duckdb.org/2022/01/06/time-zones.html).
This library has a number of advantages, including support for daylight savings time past 2037.
(Note: Pandas gives incorrect results past that year).

The downside of using ICU is that it is not highly performant.
One workaround for this is to create a calendar table for the timestamps being modeled.
For example, if the application is modeling electrical supply and demand out to 2100 at hourly resolution,
one can create the calendar table like so:

```sql
set timezone = 'Europe/Netherlands';

create or replace table hourly as
    select 
        ts, 
        year::SMALLINT as year,
        month::TINYINT as month,
        day::TINYINT as day,
        hour::TINYINT as hour,
    from (
        select ts, unnest(date_part(['year', 'month', 'day', 'hour',], ts))
        from generate_series(
            '2020-01-01'::DATE::TIMESTAMPTZ, 
            '2100-01-01'::DATE::TIMESTAMPTZ, 
            INTERVAL 1 HOUR) tbl(ts)
    ) parts;
```

You can then join this ~700K row table against any timestamp column 
to quickly obtain the temporal bin values for the time zone in question.
The inner casts are not required, but result in a smaller table 
because `date_part` returns 64 bit integers for all parts.

Notice that we can extract _all_ of the parts with a single call to `date_part`.
This part list version of the function is faster than extracting the parts one by one
because the underlying binning computation computes all parts,
so picking out the ones in the list is avoids duplicate calls to the slow ICU function.

Also notice that we are leveraging the `DATE` cast rules from the previous section 
to bound the calendar to the model domain.

## Half Open Intervals

Another subtle problem in using SQL for temporal analytics is the `BETWEEN` operator.
Temporal analytics almost always uses 
[half-open binning intervals](https://www.cs.arizona.edu/~rts/tdbbook.pdf) 
to avoid overlaps at the ends.
Unfortunately, the `BETWEEN` operator is a closed-closed interval:

```sql
x BETWEEN begin AND end
-- expands to
begin <= x AND x <= end
-- not
begin <= x AND x < end

```

To avoid this problem, make sure you are explicit about comparison boundaries instead of using `BETWEEN`.

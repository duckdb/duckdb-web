---
layout: docu
title: DuckDB ASOF Join
selected: DuckDB ASOF Join
---

Problem: we have a time-based price table; Traditional joins against this table get NULL
results if there is a time which does not exactly match.

Solution: "ASOF JOIN" picks a good value for "in the gap" values.

First, we create a price table and sales table.

```sql
CREATE TABLE prices AS (
    SELECT '2001-01-01 00:16:00'::TIMESTAMP + INTERVAL (v) MINUTE AS ticker_time,
        v AS unit_price
    FROM range(0,5) vals(v)
);

create table sales(item text, sale_time timestamp, quantity int);
insert into sales values('a', '2001-01-01 00:18:00', 10);
insert into sales values('b', '2001-01-01 00:18:30', 20);
insert into sales values('c', '2001-01-01 00:19:00', 30);
```

We can see that we have a unit_price defined for each hour, but not for half hours.

```sql
SELECT * FROM prices;
```
```
┌─────────────────────┬────────────┐
│     ticker_time     │ unit_price │
│      timestamp      │   int64    │
├─────────────────────┼────────────┤
│ 2001-01-01 00:16:00 │          0 │
│ 2001-01-01 00:17:00 │          1 │
│ 2001-01-01 00:18:00 │          2 │ No unit_price for 18:30!
│ 2001-01-01 00:19:00 │          3 │
│ 2001-01-01 00:20:00 │          4 │
└─────────────────────┴────────────┘
```
```sql
SELECT * FROM sales;
```
```
┌─────────┬─────────────────────┬──────────┐
│  item   │      sale_time      │ quantity │
│ varchar │      timestamp      │  int32   │
├─────────┼─────────────────────┼──────────┤
│ a       │ 2001-01-01 00:18:00 │       10 │
│ b       │ 2001-01-01 00:18:30 │       20 │ A sale time of 18:30!
│ c       │ 2001-01-01 00:19:00 │       30 │
└─────────┴─────────────────────┴──────────┘
```

With a normal LEFT JOIN, there is a problem for the 18:30 sale.
Since there is not a sale_time of 18:30, a join against that time
will be NULL.

```sql
-- no price value for 18:30, so item b's unit_price and total are NULL!

SELECT s.*, p.unit_price, s.quantity * p.unit_price AS total
 FROM sales s LEFT JOIN prices p
   ON s.sale_time = p.ticker_time;
```
```
┌─────────┬─────────────────────┬──────────┬────────────┬───────┐
│  item   │      sale_time      │ quantity │ unit_price │ total │
│ varchar │      timestamp      │  int32   │   int64    │ int64 │
├─────────┼─────────────────────┼──────────┼────────────┼───────┤
│ a       │ 2001-01-01 00:18:00 │       10 │          2 │    20 │
│ c       │ 2001-01-01 00:19:00 │       30 │          3 │    90 │
│ b       │ 2001-01-01 00:18:30 │       20 │       NULL │  NULL │  NULL result!
└─────────┴─────────────────────┴──────────┴────────────┴───────┘
```

The `ASOF JOIN` picks a good price for the 18:30 sale.  the `ON s.sale_item >= pp.ticker_time`
will cause the nearest lower value (in this case, for 18:00) to be used.

```sql
-- using ASOF, 18:30 "rounds down" to use the 18:00 unit_price

SELECT s.*, p.unit_price, s.quantity * p.unit_price AS total_cost
  FROM sales s ASOF LEFT JOIN prices p
    ON s.sale_time >= p.ticker_time;
```
```
┌─────────┬─────────────────────┬──────────┬────────────┬────────────┐
│  item   │      sale_time      │ quantity │ unit_price │ total_cost │
│ varchar │      timestamp      │  int32   │   int64    │   int64    │
├─────────┼─────────────────────┼──────────┼────────────┼────────────┤
│ a       │ 2001-01-01 00:18:00 │       10 │          2 │         20 │
│ b       │ 2001-01-01 00:18:30 │       20 │          2 │         40 │ Good result!
│ c       │ 2001-01-01 00:19:00 │       30 │          3 │         90 │
└─────────┴─────────────────────┴──────────┴────────────┴────────────┘
```

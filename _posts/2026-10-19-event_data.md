---
layout: post
title: "When Did the Session End? Did They Buy?"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/window-functions-2.svg"
image: "/images/blog/thumbs/window-functions-2.png"
excerpt: "Splitting clicks into sessions, finding the longest run of consecutive days, and checking whether a cart was followed by a purchase are all questions about ordered rows. DuckDB now answers them with `MATCH_RECOGNIZE`, the SQL standard's row pattern matching clause. This post shows how it works, with window-function equivalents for comparison."
tag: using-duckdb
---

A lot of analytical questions are about the order of rows, not just their values.

* When did a user's session end?
* What is the longest run of days on which someone logged in?
* Did a visitor buy something within ten minutes of adding it to the cart?

The SQL standard answers questions like these with [`MATCH_RECOGNIZE`](https://en.wikipedia.org/wiki/SQL:2016#Row_pattern_recognition), a clause for *row pattern recognition*: you write a regular expression over rows, label the rows it matches, and compute values from each match. It has been a [long-standing request](https://github.com/duckdb/duckdb/discussions/3994) for DuckDB, and it is now implemented.

> New The `MATCH_RECOGNIZE` clause is introduced in DuckDB 2.1. It is not part of the 2.0 release. To run the examples in this post today, install a [nightly build]({% link install/preview.md %}).

In this blog post, we use `MATCH_RECOGNIZE` to answer all three questions, and we show the [window function]({% link docs/current/sql/functions/window_functions.md %}) equivalents that work in DuckDB 2.0 and earlier.

## The Data

We use a small clickstream with two users:

```sql
CREATE TABLE clicks (user_id INTEGER, ts TIMESTAMP, event VARCHAR);
INSERT INTO clicks VALUES
    (1, '2026-10-01 09:00:00', 'view'),
    (1, '2026-10-01 09:02:10', 'view'),
    (1, '2026-10-01 09:04:30', 'cart'),
    (1, '2026-10-01 09:51:00', 'view'),
    (1, '2026-10-01 09:53:15', 'cart'),
    (1, '2026-10-01 09:55:40', 'buy'),
    (2, '2026-10-01 10:10:00', 'view'),
    (2, '2026-10-01 10:12:00', 'cart'),
    (2, '2026-10-01 10:13:30', 'view'),
    (2, '2026-10-01 10:20:00', 'buy');
```

## Anatomy of a Match

Start with the funnel question: did a user who added something to the cart go on to buy? `MATCH_RECOGNIZE` is a table clause, written after a table in the `FROM` list. For each user, it looks for a `cart` event, any number of non-purchase events, and then a `buy`:

```sql
FROM clicks MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES
        first(cart.ts) AS cart_ts,
        last(buy.ts)   AS buy_ts
    ONE ROW PER MATCH
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (cart nonbuy* buy)
    DEFINE
        cart   AS event = 'cart',
        nonbuy AS event <> 'buy',
        buy    AS event = 'buy'
)
ORDER BY user_id;
```

```text
┌─────────┬─────────────────────┬─────────────────────┐
│ user_id │       cart_ts       │       buy_ts        │
│  int32  │      timestamp      │      timestamp      │
├─────────┼─────────────────────┼─────────────────────┤
│       1 │ 2026-10-01 09:04:30 │ 2026-10-01 09:55:40 │
│       2 │ 2026-10-01 10:12:00 │ 2026-10-01 10:20:00 │
└─────────┴─────────────────────┴─────────────────────┘
```

Each clause plays a distinct role:

* `PARTITION BY` and `ORDER BY` work as they do in [window functions]({% link docs/current/sql/functions/window_functions.md %}): matching happens inside each user independently, with rows examined in timestamp order.
* `PATTERN` is a regular expression over rows. The names `cart`, `nonbuy`, and `buy` are *pattern variables*, and the quantifier `*` means zero or more, just as in a text regular expression.
* `DEFINE` gives the condition each variable must satisfy. A row is labeled `cart` only when `event = 'cart'`, and so on. A pattern variable with no `DEFINE` matches any row.
* `MEASURES` computes output columns from the matched rows. Here `first(cart.ts)` is the timestamp of the first `cart` row in the match, and `last(buy.ts)` is the timestamp of its `buy` row.
* `ONE ROW PER MATCH` returns a single summary row per match.
* `AFTER MATCH SKIP PAST LAST ROW` tells the engine to resume scanning after the last row of the match, so matches do not overlap.

## Seeing Every Matched Row

`ONE ROW PER MATCH` hides which rows made up each match. Switching to `ALL ROWS PER MATCH` returns every matched row, and the `classifier()` function reports the pattern variable each row was assigned to:

```sql
FROM clicks MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES
        match_number() AS match_no,
        classifier()   AS which
    ALL ROWS PER MATCH
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (cart nonbuy* buy)
    DEFINE
        cart   AS event = 'cart',
        nonbuy AS event <> 'buy',
        buy    AS event = 'buy'
)
ORDER BY user_id, ts;
```

```text
┌─────────┬─────────────────────┬──────────┬─────────┬─────────┐
│ user_id │         ts          │ match_no │  which  │  event  │
│  int32  │      timestamp      │  uint64  │ varchar │ varchar │
├─────────┼─────────────────────┼──────────┼─────────┼─────────┤
│       1 │ 2026-10-01 09:04:30 │        1 │ cart    │ cart    │
│       1 │ 2026-10-01 09:51:00 │        1 │ nonbuy  │ view    │
│       1 │ 2026-10-01 09:53:15 │        1 │ nonbuy  │ cart    │
│       1 │ 2026-10-01 09:55:40 │        1 │ buy     │ buy     │
│       2 │ 2026-10-01 10:12:00 │        1 │ cart    │ cart    │
│       2 │ 2026-10-01 10:13:30 │        1 │ nonbuy  │ view    │
│       2 │ 2026-10-01 10:20:00 │        1 │ buy     │ buy     │
└─────────┴─────────────────────┴──────────┴─────────┴─────────┘
```

`match_number()` numbers the matches within each partition, and `classifier()` shows that user 1's second `cart` was consumed as a `nonbuy` row inside the single match that runs from the first cart to the purchase. This per-row detail is exactly what the pattern-as-text workarounds cannot give you.

## Immediate or Eventual

The pattern controls how strict the funnel is. Requiring the purchase to come *directly* after the cart is a two-variable pattern with nothing in between:

```sql
FROM clicks MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES cart.ts AS cart_ts, buy.ts AS buy_ts
    ONE ROW PER MATCH
    PATTERN (cart buy)
    DEFINE cart AS event = 'cart', buy AS event = 'buy'
)
ORDER BY user_id;
```

```text
┌─────────┬─────────────────────┬─────────────────────┐
│ user_id │       cart_ts       │       buy_ts        │
│  int32  │      timestamp      │      timestamp      │
├─────────┼─────────────────────┼─────────────────────┤
│       1 │ 2026-10-01 09:53:15 │ 2026-10-01 09:55:40 │
└─────────┴─────────────────────┴─────────────────────┘
```

Only user 1 has a cart that is immediately followed by a purchase. User 2 viewed another page between the cart and the buy, so there is no match.

## Adding a Time Limit

A pattern variable's condition can look at other rows in the match through the navigation functions `prev`, `first`, and `last`. To keep only purchases that happen within ten minutes of the cart, add that constraint to the `buy` definition:

```sql
FROM clicks MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES first(cart.ts) AS cart_ts, last(buy.ts) AS buy_ts
    ONE ROW PER MATCH
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (cart nonbuy* buy)
    DEFINE
        cart   AS event = 'cart',
        nonbuy AS event <> 'buy',
        buy    AS event = 'buy' AND ts <= first(cart.ts) + INTERVAL 10 MINUTE
)
ORDER BY user_id;
```

```text
┌─────────┬─────────────────────┬─────────────────────┐
│ user_id │       cart_ts       │       buy_ts        │
│  int32  │      timestamp      │      timestamp      │
├─────────┼─────────────────────┼─────────────────────┤
│       1 │ 2026-10-01 09:53:15 │ 2026-10-01 09:55:40 │
│       2 │ 2026-10-01 10:12:00 │ 2026-10-01 10:20:00 │
└─────────┴─────────────────────┴─────────────────────┘
```

User 1's first cart no longer matches: its only later purchase is 46 minutes away, outside the window. The engine then finds the second cart, which is followed by a purchase two minutes later.

## Sessions: Splitting on Gaps

A common definition of a session, popularized by web analytics tools, is a run of events where no two consecutive events are more than 30 minutes apart. That is a pattern too: a starting row, followed by any number of rows that each fall within 30 minutes of the previous one. The `prev` function reaches back to the preceding matched row:

```sql
FROM clicks MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES
        match_number() AS session_no,
        first(ts) AS started,
        last(ts) - first(ts) AS duration,
        count(*) AS events,
        string_agg(event, ' > ') AS path
    ONE ROW PER MATCH
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (strt within*)
    DEFINE within AS ts - prev(ts) <= INTERVAL 30 MINUTE
)
ORDER BY user_id, started;
```

```text
┌─────────┬────────────┬─────────────────────┬──────────┬────────┬──────────────────────────┐
│ user_id │ session_no │       started       │ duration │ events │           path           │
│  int32  │   uint64   │      timestamp      │ interval │ int64  │         varchar          │
├─────────┼────────────┼─────────────────────┼──────────┼────────┼──────────────────────────┤
│       1 │          1 │ 2026-10-01 09:00:00 │ 00:04:30 │      3 │ view > view > cart       │
│       1 │          2 │ 2026-10-01 09:51:00 │ 00:04:40 │      3 │ view > cart > buy        │
│       2 │          1 │ 2026-10-01 10:10:00 │ 00:10:00 │      4 │ view > cart > view > buy │
└─────────┴────────────┴─────────────────────┴──────────┴────────┴──────────────────────────┘
```

The `strt` variable has no `DEFINE`, so it matches any row and anchors the start of each session. Every following row is tested by `within`, and the 46-minute gap in user 1's stream breaks the match, which starts a second session on the next scan. Aggregates such as `count` and `string_agg` run over the rows of each match, so the summary comes straight out of `MEASURES`.

## Streaks: Consecutive Days

The same shape answers the streak question. Take a table of days on which users logged in:

```sql
CREATE TABLE logins (user_id INTEGER, day DATE);
INSERT INTO logins VALUES
    (1, '2026-10-01'), (1, '2026-10-02'), (1, '2026-10-03'),
    (1, '2026-10-06'), (1, '2026-10-07'),
    (2, '2026-10-02'), (2, '2026-10-04'), (2, '2026-10-05'),
    (2, '2026-10-06'), (2, '2026-10-07');
```

A streak is a starting day followed by days that are each exactly one day after the previous one. Deduplicating the days with [`SELECT DISTINCT`]({% link docs/current/sql/statements/select.md %}) first means two logins on the same day do not break the run:

```sql
FROM (SELECT DISTINCT user_id, day FROM logins) MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY day
    MEASURES first(day) AS first_day, last(day) AS last_day, count(*) AS days
    ONE ROW PER MATCH
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (strt consec*)
    DEFINE consec AS day = prev(day) + 1
)
ORDER BY user_id, first_day;
```

```text
┌─────────┬────────────┬────────────┬───────┐
│ user_id │ first_day  │  last_day  │ days  │
│  int32  │    date    │    date    │ int64 │
├─────────┼────────────┼────────────┼───────┤
│       1 │ 2026-10-01 │ 2026-10-03 │     3 │
│       1 │ 2026-10-06 │ 2026-10-07 │     2 │
│       2 │ 2026-10-02 │ 2026-10-02 │     1 │
│       2 │ 2026-10-04 │ 2026-10-07 │     4 │
└─────────┴────────────┴────────────┴───────┘
```

Adding `day + 1` to a `DATE` moves forward one day, so `day = prev(day) + 1` holds exactly on consecutive days. One more aggregation gives the longest streak per user:

```sql
SELECT user_id, max(days) AS longest_streak
FROM (
    FROM (SELECT DISTINCT user_id, day FROM logins) MATCH_RECOGNIZE (
        PARTITION BY user_id
        ORDER BY day
        MEASURES count(*) AS days
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (strt consec*)
        DEFINE consec AS day = prev(day) + 1
    )
)
GROUP BY user_id
ORDER BY user_id;
```

```text
┌─────────┬────────────────┐
│ user_id │ longest_streak │
│  int32  │     int64      │
├─────────┼────────────────┤
│       1 │              3 │
│       2 │              4 │
└─────────┴────────────────┘
```

## The Portable Version: Window Functions

Before DuckDB 2.1, these questions were answered with [window functions]({% link docs/current/sql/functions/window_functions.md %}) and a few well-known idioms. These queries still work and remain the way to express the same logic in DuckDB 2.0 and earlier.

Sessions use the "flag a boundary, then run a count" idiom. [`lag`]({% link docs/current/sql/functions/window_functions.md %}) gives the gap to the previous event, a boundary is flagged whenever the gap is too large, and a running [`count_if`]({% link docs/current/sql/functions/utility.md %}) turns the flags into session numbers:

```sql
SELECT
    user_id,
    session_no,
    min(ts) AS started,
    max(ts) - min(ts) AS duration,
    count(*) AS events,
    string_agg(event, ' > ' ORDER BY ts) AS path
FROM (
    SELECT
        *,
        count_if(new_session) OVER (PARTITION BY user_id ORDER BY ts) AS session_no
    FROM (
        SELECT
            *,
            coalesce(
                ts - lag(ts) OVER (PARTITION BY user_id ORDER BY ts) > INTERVAL 30 MINUTE,
                true
            ) AS new_session
        FROM clicks
    )
)
GROUP BY ALL
ORDER BY ALL;
```

```text
┌─────────┬────────────┬─────────────────────┬──────────┬────────┬──────────────────────────┐
│ user_id │ session_no │       started       │ duration │ events │           path           │
│  int32  │   int128   │      timestamp      │ interval │ int64  │         varchar          │
├─────────┼────────────┼─────────────────────┼──────────┼────────┼──────────────────────────┤
│       1 │          1 │ 2026-10-01 09:00:00 │ 00:04:30 │      3 │ view > view > cart       │
│       1 │          2 │ 2026-10-01 09:51:00 │ 00:04:40 │      3 │ view > cart > buy        │
│       2 │          1 │ 2026-10-01 10:10:00 │ 00:10:00 │      4 │ view > cart > view > buy │
└─────────┴────────────┴─────────────────────┴──────────┴────────┴──────────────────────────┘
```

Streaks use the *gaps and islands* trick: subtracting a [`row_number`]({% link docs/current/sql/functions/window_functions.md %}) from the date gives a value that is constant within a run of consecutive days and changes at every gap, so it can be used as a group key.

```sql
SELECT user_id, max(days) AS longest_streak
FROM (
    SELECT user_id, count(*) AS days
    FROM (
        SELECT
            user_id,
            day,
            day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::INTEGER AS island
        FROM (SELECT DISTINCT user_id, day FROM logins)
    )
    GROUP BY user_id, island
)
GROUP BY user_id
ORDER BY user_id;
```

```text
┌─────────┬────────────────┐
│ user_id │ longest_streak │
│  int32  │     int64      │
├─────────┼────────────────┤
│       1 │              3 │
│       2 │              4 │
└─────────┴────────────────┘
```

Both produce the same results as the `MATCH_RECOGNIZE` queries. They work everywhere DuckDB does, but the logic is implicit: the pattern lives in a subtraction or a running count rather than in a readable `PATTERN` clause.

## Summary

| Question | `MATCH_RECOGNIZE` | Window-function idiom |
| --- | --- | --- |
| Did a cart lead to a purchase? | `PATTERN (cart nonbuy* buy)` | Window with a `RANGE` frame and `FILTER` |
| Within N minutes? | Navigation in `DEFINE` (`first(cart.ts) + INTERVAL`) | `RANGE BETWEEN CURRENT ROW AND INTERVAL ... FOLLOWING` |
| Where does a session start? | `PATTERN (strt within*)` with `prev` | Flag with `lag`, then a running `count_if` |
| How long are runs of consecutive days? | `PATTERN (strt consec*)` | Value minus `row_number()`, then `GROUP BY` |

`MATCH_RECOGNIZE` makes the pattern explicit, labels the rows that matched, and keeps the summary in one `MEASURES` clause. Window functions remain available everywhere and are the right choice when you cannot yet move to DuckDB 2.1. Both are [parallel and handle large inputs well]({% post_url 2025-02-10-window-catchup %}), so the same queries carry over to event tables much larger than the ten rows above.

## Further Reading

* [Add `MATCH_RECOGNIZE`](https://github.com/duckdb/duckdb/pull/25255) (DuckDB pull request)
* [Row pattern recognition request](https://github.com/duckdb/duckdb/discussions/3994) (DuckDB discussion)
* [Window Functions]({% link docs/current/sql/functions/window_functions.md %}) (DuckDB documentation)
* [Aggregate Functions]({% link docs/current/sql/functions/aggregates.md %}) including `string_agg` (DuckDB documentation)
* [Windowing in DuckDB]({% post_url 2021-10-13-windowing %}) (DuckDB blog)
* [Catching up with Windowing]({% post_url 2025-02-10-window-catchup %}) (DuckDB blog)
* [Flying Through Windows]({% post_url 2025-02-14-window-flying %}) (DuckDB blog)
* [DuckDB's AsOf Joins: Fuzzy Temporal Lookups]({% post_url 2023-09-15-asof-joins-fuzzy-temporal-lookups %}) (DuckDB blog)

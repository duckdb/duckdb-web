---
layout: post
title: "When Did the Session End? Did They Buy?"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/window-functions-2.svg"
image: "/images/blog/thumbs/window-functions-2.png"
excerpt: "Splitting clicks into sessions, finding the longest run of consecutive days, and checking whether a cart was followed by a purchase are all questions about ordered rows. In this post, we answer them in DuckDB with window functions and a few common patterns."
tag: using-duckdb
---

A lot of analytical questions are about the order of rows, not just their values.

* When did a user's session end?
* What is the longest run of days on which someone logged in?
* Did a visitor buy something within ten minutes of adding it to the cart?

Some databases answer these with [`MATCH_RECOGNIZE`](https://en.wikipedia.org/wiki/SQL:2016#Row_pattern_recognition), and there is a [long-running discussion](https://github.com/duckdb/duckdb/discussions/3994) about adding it to DuckDB.

> Tip `MATCH_RECOGNIZE` support is [planned for DuckDB 2.1](https://github.com/duckdb/duckdb/discussions/3994) (not the upcoming 2.0 release). You can already try it out on a [nightly build]({% link install/preview.md %}).

Most of these questions can be answered today with [window functions]({% link docs/current/sql/functions/window_functions.md %}) and a few well-known patterns:

* **[Sessions](#sessions-splitting-on-gaps):** split a stream of events into sessions whenever the gap between consecutive events grows too large.
* **[Streaks](#streaks-gaps-and-islands):** find runs of consecutive values, the classic *gaps and islands* problem.
* **[Patterns](#patterns-a-followed-by-b):** check whether one kind of event is followed by another, either within a time window or anywhere in a session.

In this blog post, we go through all of the above.

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

## Sessions: Splitting on Gaps

A common definition of a session, popularized by web analytics tools such as Google Analytics, is a run of events where no two consecutive events are more than 30 minutes apart. The exact threshold is a convention rather than a hard rule, and most tools let you change it. The first step is to compute the gap to the previous event of the same user with [`lag`]({% link docs/current/sql/functions/window_functions.md %}):

```sql
SELECT
    user_id, ts, event,
    ts - lag(ts) OVER (PARTITION BY user_id ORDER BY ts) AS gap
FROM clicks
ORDER BY user_id, ts;
```

```text
┌─────────┬─────────────────────┬─────────┬──────────┐
│ user_id │         ts          │  event  │   gap    │
│  int32  │      timestamp      │ varchar │ interval │
├─────────┼─────────────────────┼─────────┼──────────┤
│       1 │ 2026-10-01 09:00:00 │ view    │ NULL     │
│       1 │ 2026-10-01 09:02:10 │ view    │ 00:02:10 │
│       1 │ 2026-10-01 09:04:30 │ cart    │ 00:02:20 │
│       1 │ 2026-10-01 09:51:00 │ view    │ 00:46:30 │
│       1 │ 2026-10-01 09:53:15 │ cart    │ 00:02:15 │
│       1 │ 2026-10-01 09:55:40 │ buy     │ 00:02:25 │
│       2 │ 2026-10-01 10:10:00 │ view    │ NULL     │
│       2 │ 2026-10-01 10:12:00 │ cart    │ 00:02:00 │
│       2 │ 2026-10-01 10:13:30 │ view    │ 00:01:30 │
│       2 │ 2026-10-01 10:20:00 │ buy     │ 00:06:30 │
└─────────┴─────────────────────┴─────────┴──────────┘
  10 rows                                  4 columns
```

The 46-minute gap for user 1 is where a new session starts. Turn the gap into a flag, then number the sessions with a running [`count_if`]({% link docs/current/sql/functions/utility.md %}) of the flags. Every time the flag is `true`, the count goes up by one:

```sql
CREATE TABLE sessions AS
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
    );

FROM sessions
ORDER BY user_id, ts;
```

```text
┌─────────┬─────────────────────┬─────────┬─────────────┬────────────┐
│ user_id │         ts          │  event  │ new_session │ session_no │
│  int32  │      timestamp      │ varchar │   boolean   │   int128   │
├─────────┼─────────────────────┼─────────┼─────────────┼────────────┤
│       1 │ 2026-10-01 09:00:00 │ view    │ true        │          1 │
│       1 │ 2026-10-01 09:02:10 │ view    │ false       │          1 │
│       1 │ 2026-10-01 09:04:30 │ cart    │ false       │          1 │
│       1 │ 2026-10-01 09:51:00 │ view    │ true        │          2 │
│       1 │ 2026-10-01 09:53:15 │ cart    │ false       │          2 │
│       1 │ 2026-10-01 09:55:40 │ buy     │ false       │          2 │
│       2 │ 2026-10-01 10:10:00 │ view    │ true        │          1 │
│       2 │ 2026-10-01 10:12:00 │ cart    │ false       │          1 │
│       2 │ 2026-10-01 10:13:30 │ view    │ false       │          1 │
│       2 │ 2026-10-01 10:20:00 │ buy     │ false       │          1 │
└─────────┴─────────────────────┴─────────┴─────────────┴────────────┘
  10 rows                                                  5 columns
```

The [`coalesce`]({% link docs/current/sql/functions/utility.md %}) handles the first event of each user, which has no previous event and therefore a `NULL` gap. With a session number on every row, summarizing sessions is a regular [`GROUP BY`]({% link docs/current/sql/query_syntax/groupby.md %}). An ordered [`string_agg`]({% link docs/current/sql/functions/aggregates.md %}) shows the path through each session:

```sql
SELECT
    user_id,
    session_no,
    min(ts) AS started,
    max(ts) - min(ts) AS duration,
    count(*) AS events,
    string_agg(event, ' > ' ORDER BY ts) AS path
FROM sessions
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

The same "flag, then running count" pattern works for any rule that decides where a new group starts: a change of status, a reset of a counter, or a visit that resumes after a long pause.

## Streaks: Gaps and Islands

The second pattern finds runs of consecutive values, often called *gaps and islands*. Take a table of days on which users logged in:

```sql
CREATE TABLE logins (user_id INTEGER, day DATE);
INSERT INTO logins VALUES
    (1, '2026-10-01'), (1, '2026-10-02'), (1, '2026-10-03'),
    (1, '2026-10-06'), (1, '2026-10-07'),
    (2, '2026-10-02'), (2, '2026-10-04'), (2, '2026-10-05'),
    (2, '2026-10-06'), (2, '2026-10-07');
```

The trick is to subtract the [row number]({% link docs/current/sql/functions/window_functions.md %}) from the date. Within a run of consecutive days, both go up by one at each step, so the difference stays the same. When a day is skipped, the date jumps by more than the row number and the difference changes:

```sql
SELECT
    user_id,
    day,
    row_number() OVER (PARTITION BY user_id ORDER BY day) AS rn,
    day - rn::INTEGER AS island
FROM logins
ORDER BY user_id, day;
```

```text
┌─────────┬────────────┬───────┬────────────┐
│ user_id │    day     │  rn   │   island   │
│  int32  │    date    │ int64 │    date    │
├─────────┼────────────┼───────┼────────────┤
│       1 │ 2026-10-01 │     1 │ 2026-09-30 │
│       1 │ 2026-10-02 │     2 │ 2026-09-30 │
│       1 │ 2026-10-03 │     3 │ 2026-09-30 │
│       1 │ 2026-10-06 │     4 │ 2026-10-02 │
│       1 │ 2026-10-07 │     5 │ 2026-10-02 │
│       2 │ 2026-10-02 │     1 │ 2026-10-01 │
│       2 │ 2026-10-04 │     2 │ 2026-10-02 │
│       2 │ 2026-10-05 │     3 │ 2026-10-02 │
│       2 │ 2026-10-06 │     4 │ 2026-10-02 │
│       2 │ 2026-10-07 │     5 │ 2026-10-02 │
└─────────┴────────────┴───────┴────────────┘
  10 rows                         4 columns
```

The `island` value has no meaning on its own. It only serves as a group key: all rows in one run share the same value. DuckDB also lets `rn` be reused in the same `SELECT` that defines it. Grouping on the island gives the streaks:

```sql
SELECT user_id, min(day) AS first_day, max(day) AS last_day, count(*) AS days
FROM (
    SELECT
        user_id,
        day,
        day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::INTEGER AS island
    FROM logins
)
GROUP BY user_id, island
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

Wrapping this in one more aggregation with [`max`]({% link docs/current/sql/functions/aggregates.md %}) gives the longest streak per user:

```sql
SELECT user_id, max(days) AS longest_streak
FROM (
    SELECT user_id, count(*) AS days
    FROM (
        SELECT
            user_id,
            day,
            day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::INTEGER AS island
        FROM logins
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

This assumes at most one login per user per day. Suppose user 1 logs in twice on the same day:

```sql
INSERT INTO logins VALUES (1, '2026-10-02');
```

Now two rows share a date but still get consecutive row numbers, so the date and the row number stop advancing in step and the run of October 1 to 3 is split into two islands:

```sql
SELECT
    user_id,
    day,
    row_number() OVER (PARTITION BY user_id ORDER BY day) AS rn,
    day - rn::INTEGER AS island
FROM logins
WHERE user_id = 1
ORDER BY day;
```

```text
┌─────────┬────────────┬───────┬────────────┐
│ user_id │    day     │  rn   │   island   │
│  int32  │    date    │ int64 │    date    │
├─────────┼────────────┼───────┼────────────┤
│       1 │ 2026-10-01 │     1 │ 2026-09-30 │
│       1 │ 2026-10-02 │     2 │ 2026-09-30 │
│       1 │ 2026-10-02 │     3 │ 2026-09-29 │
│       1 │ 2026-10-03 │     4 │ 2026-09-29 │
│       1 │ 2026-10-06 │     5 │ 2026-10-01 │
│       1 │ 2026-10-07 │     6 │ 2026-10-01 │
└─────────┴────────────┴───────┴────────────┘
```

Deduplicating the days first with [`SELECT DISTINCT`]({% link docs/current/sql/statements/select.md %}) puts one row per day back in place, and the islands line up again:

```sql
SELECT
    user_id,
    day,
    row_number() OVER (PARTITION BY user_id ORDER BY day) AS rn,
    day - rn::INTEGER AS island
FROM (SELECT DISTINCT user_id, day FROM logins)
WHERE user_id = 1
ORDER BY day;
```

```text
┌─────────┬────────────┬───────┬────────────┐
│ user_id │    day     │  rn   │   island   │
│  int32  │    date    │ int64 │    date    │
├─────────┼────────────┼───────┼────────────┤
│       1 │ 2026-10-01 │     1 │ 2026-09-30 │
│       1 │ 2026-10-02 │     2 │ 2026-09-30 │
│       1 │ 2026-10-03 │     3 │ 2026-09-30 │
│       1 │ 2026-10-06 │     4 │ 2026-10-02 │
│       1 │ 2026-10-07 │     5 │ 2026-10-02 │
└─────────┴────────────┴───────┴────────────┘
```

## Patterns: "A Followed by B"

The third type of question is about sequences of events. Did a cart event lead to a purchase?

### Within a Time Window

If the pattern has a time limit, a window with a [`RANGE`]({% link docs/current/sql/functions/window_functions.md %}) frame expresses it directly. For each cart event, look at the following ten minutes of the same user and find the first purchase:

```sql
SELECT
    user_id,
    ts AS cart_ts,
    min(ts) FILTER (event = 'buy') OVER (
        PARTITION BY user_id
        ORDER BY ts
        RANGE BETWEEN CURRENT ROW AND INTERVAL 10 MINUTE FOLLOWING
    ) AS bought_at
FROM clicks
QUALIFY event = 'cart'
ORDER BY ALL;
```

```text
┌─────────┬─────────────────────┬─────────────────────┐
│ user_id │       cart_ts       │      bought_at      │
│  int32  │      timestamp      │      timestamp      │
├─────────┼─────────────────────┼─────────────────────┤
│       1 │ 2026-10-01 09:04:30 │ NULL                │
│       1 │ 2026-10-01 09:53:15 │ 2026-10-01 09:55:40 │
│       2 │ 2026-10-01 10:12:00 │ 2026-10-01 10:20:00 │
└─────────┴─────────────────────┴─────────────────────┘
```

Two details make this work. The [`FILTER`]({% link docs/current/sql/query_syntax/filter.md %}) clause restricts the window aggregate to purchase events, and [`QUALIFY`]({% link docs/current/sql/query_syntax/qualify.md %}) keeps only the cart rows *after* the window has been computed. With a `WHERE event = 'cart'` instead, the purchases would be gone before the window could see them.

### As a Regular Expression over the Session

Sometimes the pattern is about the order of events, not their timing. For example: a session where a cart event is immediately followed by a purchase, with nothing in between. A simple way to check this is to encode each event as a single character, concatenate them per session, and match a [regular expression]({% link docs/current/sql/functions/regular_expressions.md %}):

```sql
SELECT
    user_id,
    session_no,
    string_agg(event[1], '' ORDER BY ts) AS codes,
    regexp_matches(codes, 'cb') AS cart_then_buy,
    regexp_matches(codes, 'c[^c]*b') AS cart_eventually_buy
FROM sessions
GROUP BY ALL
ORDER BY ALL;
```

```text
┌─────────┬────────────┬─────────┬───────────────┬─────────────────────┐
│ user_id │ session_no │  codes  │ cart_then_buy │ cart_eventually_buy │
│  int32  │   int128   │ varchar │    boolean    │       boolean       │
├─────────┼────────────┼─────────┼───────────────┼─────────────────────┤
│       1 │          1 │ vvc     │ false         │ false               │
│       1 │          2 │ vcb     │ true          │ true                │
│       2 │          1 │ vcvb    │ false         │ true                │
└─────────┴────────────┴─────────┴───────────────┴─────────────────────┘
```

Here `event[1]` takes the first character of the event name, so `view`, `cart` and `buy` become `v`, `c` and `b`. The second pattern, `c[^c]*b`, allows other events between the cart and the purchase, which is why user 2's session matches the second pattern but not the first.

This is not a replacement for `MATCH_RECOGNIZE`. It does not tell you which rows matched, and it only works when every event type maps to a distinct character. For a question like "does this sequence occur in this session", the query stays short and runs quickly as long as sessions do not grow very long.

## Summary

| Question | Pattern |
| --- | --- |
| Where does a new group start? | Flag with `lag`, then a running `count_if` |
| How long are runs of consecutive values? | Value minus `row_number()`, then `GROUP BY` |
| Did B happen within N minutes after A? | Window with a `RANGE` frame and `FILTER`, then `QUALIFY` |
| Does a sequence occur in a session? | Ordered `string_agg` of event codes plus `regexp_matches` |

Apart from the regular expression check, which uses an ordered `string_agg`, these queries are built on DuckDB's window functions. Both window functions and aggregates are [parallel and handle large inputs well]({% post_url 2025-02-10-window-catchup %}), so the same queries carry over to event tables much larger than the ten rows above.

## Further Reading

* [Window Functions]({% link docs/current/sql/functions/window_functions.md %}) (DuckDB documentation)
* [The `QUALIFY` Clause]({% link docs/current/sql/query_syntax/qualify.md %}) (DuckDB documentation)
* [The `FILTER` Clause]({% link docs/current/sql/query_syntax/filter.md %}) (DuckDB documentation)
* [Aggregate Functions]({% link docs/current/sql/functions/aggregates.md %}) including `string_agg` (DuckDB documentation)
* [Regular Expressions]({% link docs/current/sql/functions/regular_expressions.md %}) (DuckDB documentation)
* [Windowing in DuckDB]({% post_url 2021-10-13-windowing %}) (DuckDB blog)
* [Catching up with Windowing]({% post_url 2025-02-10-window-catchup %}) (DuckDB blog)
* [Flying Through Windows]({% post_url 2025-02-14-window-flying %}) (DuckDB blog)
* [DuckDB's AsOf Joins: Fuzzy Temporal Lookups]({% post_url 2023-09-15-asof-joins-fuzzy-temporal-lookups %}) (DuckDB blog)
* [Friendlier SQL with DuckDB]({% post_url 2022-05-04-friendlier-sql %}) (DuckDB blog)

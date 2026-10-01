---
layout: post
title: "Faster String Aggregations with Dimension Tables"
author: "DuckDB Team"
thumb: "/images/blog/thumbs/dimension-table.svg"
image: "/images/blog/thumbs/dimension-table.png"
excerpt: "When a query groups on long, repeated strings, move the strings into a small dimension table with sorted, narrow integer keys. Aggregate on the keys, then join the strings back in at the very end. The query works as before, though on small fixed-width integers instead of variable-length text."
tags: ["using DuckDB"]
---

Analytical workloads are full of repeated strings: product names, country names, station names, user agents, category labels. Take DuckDB's public train services dataset, which has one row for every stop a Dutch railway train makes. The data comes from the open datasets published by the [Rijden de Treinen *(Are the trains running?)* application](https://www.rijdendetreinen.nl/en/open-data/). You can query it straight from its URL:

```sql
SELECT departure_time, station_name, type
FROM 'https://blobs.duckdb.org/train_services.parquet'
LIMIT 5;
```

| departure_time | station_name | type |
| --- | --- | --- |
| 2023-05-15 00:00:00 | Rotterdam Centraal | Intercity |
| 2023-05-15 00:13:00 | Delft | Intercity |
| 2023-05-15 00:29:00 | Den Haag HS | Intercity |
| 2023-05-15 00:45:00 | Leiden Centraal | Intercity |
| 2023-05-15 01:03:00 | Schiphol Airport | Intercity |

The table has 380,959 rows but only 537 distinct station names, so each name is stored again in thousands of rows: `Amsterdam Centraal` (18 bytes) alone appears in 7,591 of them. Load it into a table to follow along, in the [web shell](https://shell.duckdb.org/) or the [DuckDB CLI]({% link docs/current/clients/cli/overview.md %}):

```sql
CREATE TABLE train_services AS
    FROM 'https://blobs.duckdb.org/train_services.parquet';
```

When you [`GROUP BY`]({% link docs/current/sql/query_syntax/groupby.md %}) the station name, DuckDB has to process the full string for every row. For example, this query counts how many trains call at each station:

```sql
SELECT station_name, count(*) AS calls
FROM train_services
GROUP BY station_name;
```

Consider what happens for a handful of rows that call at just two stations:

| Row | station_name | Work when grouping on `station_name` |
| --- | --- | --- |
| 1 | Amsterdam Centraal | hash 18 bytes; new group, so copy 18 bytes into the hash table |
| 2 | Rotterdam Centraal | hash 18 bytes; new group, so copy 18 bytes into the hash table |
| 3 | Amsterdam Centraal | hash 18 bytes; existing group, so compare 18 bytes |
| 4 | Amsterdam Centraal | hash 18 bytes; existing group, so compare 18 bytes |
| 5 | Rotterdam Centraal | hash 18 bytes; existing group, so compare 18 bytes |

The string work repeats for every row, even though there are only two distinct stations here, and only 537 across the whole table.

This post shows how to do that work on small integers instead, by giving each distinct string a number and looking up the strings only at the end.

## Background

The approach is the [star schema](https://en.wikipedia.org/wiki/Star_schema) from data warehousing, used here for query performance. It came up when we looked at a user report of [heavy memory use in a high-cardinality grouping](https://github.com/duckdb/duckdb/issues/14584).

That report turned out not to involve strings, but Richard Wesley pointed out that in his own work, building dimension tables and joining the strings back at the end made a large difference to string-heavy aggregations.

We have since added the pattern to the [schema section of the Performance Guide]({% link docs/current/guides/performance/schema.md %}).

## Why Strings Are Expensive to Group On

DuckDB computes a `GROUP BY` with a hash aggregation, keeping one hash table entry per group, as described in the [Parallel Grouped Aggregation in DuckDB]({% post_url 2022-03-07-aggregate-hashtable %}) blog post (2022). The aggregation uses the hash of each group key to find the key's slot in a hash table, then compares the key with the one stored in that slot. For integers, this takes a few CPU instructions. For strings, the cost grows with the length of the string.

In DuckDB, a string value is a [16-byte structure]({% link docs/current/clients/c/vector.md %}#strings). Strings of up to 12 bytes are stored inline. Longer strings store a 4-byte prefix plus a pointer to the actual characters. That design keeps short strings cheap, but many real-world labels are longer than 12 bytes.

For these longer strings, hashing reads every byte of every string in every row. A match can't be confirmed from the prefix alone, so DuckDB follows the pointer and compares the full string. When a new group appears, its string is copied into the hash table's own memory, which makes the table larger than it would be with fixed-width keys.

Copying strings also affects memory use. A wider hash table fits less well into CPU caches, and in larger-than-memory aggregations it reaches the memory limit sooner and has to spill more data to disk. DuckDB does apply dictionary encoding to string columns on disk, as described in the [Lightweight Compression in DuckDB]({% post_url 2022-10-28-lightweight-compression %}) blog post (2022), but that is a storage optimization: once a column is read into an aggregation, each group key is a full string again.

Integer keys avoid these costs, as their fixed width makes hashing and comparing them cheap. When the key range is small, DuckDB can avoid hashing altogether: if the statistics show that the keys fit in a small enough domain, the optimizer picks a [perfect hash aggregate]({% link docs/current/configuration/overview.md %}#global-configuration-options), controlled by the `perfect_ht_threshold` setting, which uses the key value directly as an index into an array.

## Building a Dimension Table with Sorted, Narrow Keys

The examples build on the `train_services` table loaded above. Each row records one stop: a `service_id`, the `date`, the service `type`, the `train_number`, the `station_code` and `station_name`, and the `departure_time` and `arrival_time`. The repeated string we want to encode is `station_name`.

### Step 1: Measure the Cardinality

First, find out how many distinct values the column has, since that count sets how narrow the key can be.

```sql
SELECT count(DISTINCT station_name) AS num_stations
FROM train_services;
```

This returns 537, and that count decides how wide the key needs to be. You want the narrowest integer type whose range still covers every distinct value, because a narrower key means fewer bytes per row in the fact table and a smaller entry in the hash table you group on.

The keys come from [`row_number()`]({% link docs/current/sql/functions/window_functions.md %}#row_numberorder-by-ordering), which starts at 1 and only counts upward, so an unsigned type is the right fit, spending none of its range on negative values. [`UTINYINT`]({% link docs/current/sql/data_types/numeric.md %}#fixed-width-integer-types) (1 byte) holds up to 255 distinct values, [`USMALLINT`]({% link docs/current/sql/data_types/numeric.md %}#fixed-width-integer-types) (2 bytes) up to 65,535, and [`UINTEGER`]({% link docs/current/sql/data_types/numeric.md %}#fixed-width-integer-types) (4 bytes) up to about 4.3 billion.

The 537 station names do not fit in a `UTINYINT`, so `USMALLINT` is the narrowest that works, and that is the type the next step casts to. If the number of distinct values will grow, choose a larger type so you don't run out of keys.

### Step 2: Build the Dimension Table

Next, assign each distinct string an integer key. The important detail is the [`ORDER BY`]({% link docs/current/sql/query_syntax/orderby.md %}) `station_name` inside the window: the keys are assigned in string order.

```sql
CREATE OR REPLACE TABLE stations AS
    SELECT
        station_name,
        (row_number() OVER (ORDER BY station_name))::USMALLINT AS station_id
    FROM (SELECT DISTINCT station_name FROM train_services WHERE station_name IS NOT NULL);
```

Sorted keys have two advantages. First, `ORDER BY station_id` produces the same order as `ORDER BY station_name`, so you can sort on the cheap integer. Second, the key assignment is deterministic: rebuilding the table from the same data yields the same keys.

### Step 3: Store the Key in the Fact Table

Finally, replace the string column in the fact table with its key, a rewrite of the table that you pay for once. The dimension table leaves out [`NULL`]({% link docs/current/sql/data_types/nulls.md %}), so the [`LEFT JOIN`]({% link docs/current/sql/query_syntax/from.md %}#joins) keeps the rows without a station and gives them a `NULL` key.

```sql
CREATE OR REPLACE TABLE train_services_encoded AS
    SELECT ts.* EXCLUDE (station_name), s.station_id
    FROM train_services ts
    LEFT JOIN stations s USING (station_name);
```

The `stations` dimension table holds each name once, keyed in alphabetical order:

| station_id | station_name |
| --- | --- |
| 1 | 's-Hertogenbosch |
| 2 | 's-Hertogenbosch Oost |
| 3 | 't Harde |
| 4 | Aachen Hbf |

The fact table now stores the 2-byte `USMALLINT` key, so grouping on it is cheap:

| Row | station_id | Work when grouping on `station_id` |
| --- | --- | --- |
| 1 | 28 | hash 2 bytes; new group, so store 2 bytes |
| 2 | 403 | hash 2 bytes; new group, so store 2 bytes |
| 3 | 28 | hash 2 bytes; existing group, so compare 2 bytes |
| 4 | 28 | hash 2 bytes; existing group, so compare 2 bytes |
| 5 | 403 | hash 2 bytes; existing group, so compare 2 bytes |

The keys follow string order: `Amsterdam Centraal` sorts before `Rotterdam Centraal`, so it gets the smaller key (28 versus 403). With a key range this small and dense, DuckDB can use a perfect hash aggregate, indexing directly by the key instead of hashing.

You can also leave out this step and join the dimension table on the fly inside each query. That still keeps the aggregation's hash table narrow, but every query then pays for hashing the strings once in the join. Storing the key in the fact table removes string processing from the query.

## Querying the Encoded Table

With the key in place, the query aggregates on integers and only looks up the strings once the result is small. The [`LEFT JOIN`]({% link docs/current/sql/query_syntax/from.md %}#joins) keeps the group of rows without a station.

```sql
WITH rollup AS (
    SELECT
        station_id,
        date,
        count(*) AS calls
    FROM train_services_encoded
    GROUP BY ALL
)
SELECT s.station_name, rollup.* EXCLUDE (station_id)
FROM rollup
LEFT JOIN stations s USING (station_id)
ORDER BY station_id, date;
```

[`GROUP BY ALL`]({% link docs/current/sql/query_syntax/groupby.md %}#group-by-all) groups by every selected column that is not aggregated, here `station_id` and `date`, so you don't repeat the list. The final join runs against the aggregated result, which has one row per group rather than one row per event. If the aggregation reduces a billion rows to a few hundred thousand, the join only looks up a few hundred thousand strings. Because the keys are sorted, `ORDER BY station_id` also sorts alphabetically by station name.

For top-N queries, apply the [`LIMIT`]({% link docs/current/sql/query_syntax/limit.md %}) before the join, so that only ten strings are looked up:

```sql
WITH top_stations AS (
    SELECT station_id, count(*) AS calls
    FROM train_services_encoded
    GROUP BY station_id
    ORDER BY calls DESC
    LIMIT 10
)
SELECT s.station_name, top_stations.calls
FROM top_stations
LEFT JOIN stations s USING (station_id)
ORDER BY calls DESC;
```

| station_name | calls |
| --- | --- |
| Utrecht Centraal | 7663 |
| Amsterdam Centraal | 7591 |
| Zwolle | 5013 |
| Schiphol Airport | 4961 |
| Amsterdam Sloterdijk | 4854 |
| … | … |

To filter on the string, look up its key in the dimension table and filter the fact table on the integer.

```sql
SELECT count(*)
FROM train_services_encoded
WHERE station_id IN (SELECT station_id FROM stations WHERE station_name LIKE '%Centraal%');
```

## Measuring the Effect

How much you gain depends on your data, mainly on how long the strings are and how many distinct values they have. On this 380,000-row sample the difference is small, and it grows as row counts and string lengths increase. To find out for your own data, run the same aggregation both ways and compare:

```sql
.timer on

-- Group on the string
SELECT station_name, count(*) AS calls
FROM train_services
GROUP BY station_name;

-- Group on the key, then join the strings back
WITH rollup AS (
    SELECT station_id, count(*) AS calls
    FROM train_services_encoded
    GROUP BY station_id
)
SELECT s.station_name, rollup.calls
FROM rollup
LEFT JOIN stations s USING (station_id);
```

To see where the time goes, prefix each query with [`EXPLAIN ANALYZE`]({% link docs/current/sql/statements/profiling.md %}#explain-analyze) and compare the timings of the aggregation operators. To compare memory use, set a lower [`memory_limit`]({% link docs/current/configuration/overview.md %}#global-configuration-options) with [`SET`]({% link docs/current/sql/statements/set.md %}) and check which query starts spilling to disk first.

## Variations

So far the examples use a single string column with a fixed set of values. The variations below cover a built-in alternative to the manual dimension table, encoding more than one string column, and keeping the keys current as new data arrives.

### Comparison with ENUM

DuckDB's [`ENUM` type]({% link docs/current/sql/data_types/enum.md %}) is dictionary encoding built into the type system: values are stored as small integers, and DuckDB picks the integer width for you. The [Lord of the Enums]({% post_url 2021-11-26-duck-enum %}) blog post (2021) benchmarks this, with a `GROUP BY` on an `ENUM` column running faster than the same grouping on the raw strings. You can create one from a query:

```sql
CREATE TYPE station_enum AS ENUM (
    SELECT DISTINCT station_name FROM train_services WHERE station_name IS NOT NULL ORDER BY station_name
);
```

If the set of values is known up front and rarely changes, an `ENUM` gives you most of the benefit with none of the extra joins. The dimension table is the better choice when:

- **New values keep arriving.** An `ENUM`'s values are fixed when the type is created, so inserting an unknown value fails. A dimension table can grow.
- **You need attributes.** A dimension table can carry extra columns, such as the station's city or the line it sits on, that you can group or filter on without parsing strings.
- **The data leaves DuckDB.** Integer keys and a lookup table can be exported to [Parquet]({% link docs/current/data/parquet/overview.md %}) or [CSV]({% link docs/current/data/csv/overview.md %}) and used in other tools.

### Several String Columns

The pattern applies per column: build one dimension table for each high-repetition string column. In this dataset both `station_name` and the service `type` qualify. Each key then gets its own integer type, sized to the cardinality of its column, and a query only joins back the dimensions it needs. The `type` column has only 15 distinct values, so its key fits in a `UTINYINT`, while `station_name` still needs a `USMALLINT`:

```sql
CREATE OR REPLACE TABLE service_types AS
    SELECT
        type,
        (row_number() OVER (ORDER BY type))::UTINYINT AS type_id
    FROM (SELECT DISTINCT type FROM train_services WHERE type IS NOT NULL);

CREATE OR REPLACE TABLE train_services_encoded AS
    SELECT ts.* EXCLUDE (station_name, type), s.station_id, t.type_id
    FROM train_services ts
    LEFT JOIN stations s USING (station_name)
    LEFT JOIN service_types t USING (type);
```

The fact table now carries both keys, and a query joins back only the dimensions it reads. A count of calls per station needs `stations`, while a breakdown by service type needs `service_types`.

If two columns always appear together, such as `station_code` and `station_name`, a single dimension table keyed on the combination is often simpler. The fact table then stores one key instead of two, which makes it narrower still.

### Keeping the Dimension Up to Date

When new data arrives, add unseen strings with keys that continue after the current maximum:

```sql
INSERT INTO stations
    SELECT
        n.station_name,
        ((SELECT max(station_id) FROM stations)
            + row_number() OVER (ORDER BY n.station_name))::USMALLINT AS station_id
    FROM (SELECT DISTINCT station_name FROM new_train_services WHERE station_name IS NOT NULL) n
    ANTI JOIN stations USING (station_name);
```

The [`ANTI JOIN`]({% link docs/current/sql/query_syntax/from.md %}#semi-and-anti-joins) keeps only the names that are not already in `stations`, so the existing keys stay untouched and each genuinely new name gets a key that continues past the current maximum.

Then encode the new rows the same way as in Step 3 and append them:

```sql
INSERT INTO train_services_encoded
    SELECT n.* EXCLUDE (station_name), s.station_id
    FROM new_train_services n
    LEFT JOIN stations s USING (station_name);
```

Appended keys no longer follow alphabetical order. If your queries rely on `ORDER BY station_id` matching `ORDER BY station_name`, rebuild the dimension table and re-key the fact table periodically, or sort on the string after the final join.

## Narrow Keys Do Not Reduce the Number of Groups

Dictionary encoding makes each group smaller. It does not reduce how many groups there are, and that matters for very high-cardinality aggregations.

The report that prompted this post, [duckdb/duckdb#14584](https://github.com/duckdb/duckdb/issues/14584), shows this. It grouped 9.2 billion rows into 320 million distinct groups and used far more memory than expected. The group key was already a [`UBIGINT`]({% link docs/current/sql/data_types/numeric.md %}#fixed-width-integer-types), so there were no strings to encode.

The cause is how DuckDB parallelizes aggregation. Each thread first aggregates its share of the rows in its own thread-local hash table, and the partial results are combined at the end. This works well when each thread sees many repeats of the same groups, which is typical for real-world data.

In the report, with 8 threads, each thread saw about 1.1 billion rows: only about 3 times the number of distinct values, spread without any useful pattern. Nearly every group ended up in nearly every thread's table, so memory use approached the number of threads times the number of groups.

Narrow keys make each of those entries smaller, but they cannot prevent the duplication. When the number of groups is close to the number of rows each thread processes, reducing the number of [`threads`]({% link docs/current/configuration/overview.md %}#global-configuration-options) helps more, because each thread holds its own copy of each group.

```sql
SET threads = 1;
```

This trades speed for memory, so reserve it for aggregations that would otherwise run out of memory or spill large amounts of data to disk. Data that is clustered by the group key also helps, as each thread then sees a smaller, more distinct set of groups.

## When the Pattern Does Not Help

The pattern makes the schema and the queries more complex, so it is not always worth it.

Don't use it when:

- **The strings are short.** Values of up to 12 bytes are already stored inline, so the gap to an integer key is much smaller.
- **The column is nearly unique.** If most values are distinct, such as IDs or free text, the dimension table has almost as many rows as the fact table and little is saved.
- **You query the data once.** Building the dimension table and rewriting the fact table costs a full pass over the data. That cost is only worth paying if you query the data repeatedly.
- **You don't aggregate on the column.** If you only ever filter on or display the string, the benefit is limited.

In these cases, keep the string column as it is. If you are unsure, compare both versions as described in [Measuring the Effect](#measuring-the-effect).

## Conclusion

Grouping on repeated strings is expensive. By moving them into a small dimension table with sorted, narrow integer keys, DuckDB can aggregate on fixed-width integers and keep its hash tables compact. The strings come back in a final join against a result that is already small.

This approach helps most when you repeatedly aggregate on long strings that have few distinct values. You can find a condensed version of this tip in the [Performance Guide]({% link docs/current/guides/performance/schema.md %}).

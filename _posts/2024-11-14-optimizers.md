---
layout: post
title: "Optimizers: The Low-Key MVP"
author: Tom Ebergen
tags: ["deep dive"]
thumb: "/images/blog/thumbs/query-optimization.svg"
image: "/images/blog/thumbs/query-optimization.png"
excerpt: "The query optimizer is an important part of any analytical database system as it provides considerable performance improvements compared to hand-optimized queries, even as the state of your data changes."
---

Optimizers don't often give "main character" energy in the database community. Databases are usually popular because of their performance, ease of integration, or reliability. As someone who mostly works on the optimizer in DuckDB, I have been wanting to write a blog post about how important optimizers are and why they merit more recognition. In this blog post we will analyze queries that fall into one of three categories: unoptimized, hand-optimized, and optimized by the DuckDB query optimizer. I will also explain why built-in optimizers are almost always better than any hand optimizations. Hopefully, by the end of this blog post, you will agree that optimizers play a silent, but vital role when using a database. Let's first start by understanding where in the execution pipeline query optimization happens.

Before any data is read from the database, the given SQL text must be parsed and validated. If this process finishes successfully, a tree-based query plan is created. The query plan produced by the parser is naïve, and can be extremely inefficient depending on the query. This is where the optimizer comes in, the inefficient query plan is passed to the optimizer for modification and, you guessed it, optimization. The optimizer is made up of many optimization rules. Each rule has the ability to reorder, insert, and delete query operations to create a slightly more efficient query plan that is also logically equivalent. Once all the optimization rules are applied, the optimized plan can be much more efficient than the plan produced by the parser.

> In practice an optimization rule can also be called an optimizer. For the rest of this blog post, optimizer rule will be used for a specific optimization, and optimizer will refer to the database optimizer, unless the word optimizer names a specific optimization rule, (i.e _Join Order Optimizer_).

## Normal Queries vs. Optimized Queries

To examine the effect of the DuckDB Optimizer, let's use a subset of the NYC taxi dataset. You can create native DuckDB tables with the following commands (note that [`taxi-data-2019.parquet`](https://blobs.duckdb.org/data/taxi-data-2019.zip) is approximately 1.3 GB):

```sql
CREATE TABLE taxi_data_2019 AS
    FROM 'https://blobs.duckdb.org/data/taxi-data-2019.parquet';
CREATE TABLE zone_lookups AS
    FROM 'https://blobs.duckdb.org/data/zone-lookups.parquet';
```

Now that we have all 2019 data, let's look at the unoptimized vs. optimized plans for a simple query. The following SQL query gets us the most common pickup and drop-off pairs in the Manhattan borough.

```sql
PRAGMA disable_optimizer;
PRAGMA explain_output = 'optimized_only';
EXPLAIN SELECT
    pickup.zone AS pickup_zone,
    dropoff.zone AS dropoff_zone,
    count(*) AS num_trips
FROM
    zone_lookups AS pickup, 
    zone_lookups AS dropoff,
    taxi_data_2019 AS data
WHERE pickup.LocationID = data.pickup_location_id
  AND dropoff.LocationID = data.dropoff_location_id
  AND pickup.Borough = 'Manhattan'
  AND dropoff.Borough = 'Manhattan'
GROUP BY pickup_zone, dropoff_zone
ORDER BY num_trips DESC
LIMIT 5;
```

Running this `EXPLAIN` query gives us the following plan.

<div class="small_code_block"></div>
```text
┌───────────────────────────┐
│           LIMIT           │
│    ────────────────────   │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│          ORDER_BY         │
│    ────────────────────   │
│        count_star()       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│        Expressions:       │
│             0             │
│             1             │
│         num_trips         │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         AGGREGATE         │
│    ────────────────────   │
│          Groups:          │
│        pickup_zone        │
│        dropoff_zone       │
│                           │
│        Expressions:       │
│        count_star()       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│           FILTER          │
│    ────────────────────   │
│        Expressions:       │
│       (LocationID =       │
│     pickup_location_id)   │
│       (LocationID =       │
│    dropoff_location_id)   │
│ (Borough = CAST('Manhattan│
│       ' AS VARCHAR))      │
│ (Borough = CAST('Manhattan│
│       ' AS VARCHAR))      │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       CROSS_PRODUCT       │
│    ────────────────────   ├───────────────────────────────────────────┐
└─────────────┬─────────────┘                                           │
┌─────────────┴─────────────┐                             ┌─────────────┴─────────────┐
│       CROSS_PRODUCT       │                             │          SEQ_SCAN         │
│    ────────────────────   ├──────────────┐              │    ────────────────────   │
│                           │              │              │       taxi_data_2019      │
└─────────────┬─────────────┘              │              └───────────────────────────┘
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│          SEQ_SCAN         ││          SEQ_SCAN         │
│    ────────────────────   ││    ────────────────────   │
│        zone_lookups       ││        zone_lookups       │
└───────────────────────────┘└───────────────────────────┘
```

The cross products alone make this query extremely inefficient. The cross-products produce `256 * 256 * |taxi_data_2019|` rows of data, which is 5 trillion rows of data. The filter only matches 71 million rows, which is only 0.001% of the data. The aggregate produces 4,373 rows of data, which need to be sorted by the `ORDER BY` operation, which runs in `O(N * log N)`. Producing 5 trillion tuples alone is an enormous amount of data processing, which becomes clear when you try to run the query and notice it doesn't complete. With the optimizer enabled, the query plan produced is much more efficient because the operations are re-ordered to avoid many trillions of rows of intermediate data. Below is the query plan with the optimizer enabled:

```sql
PRAGMA enable_optimizer;
EXPLAIN ...
```

<div class="small_code_block"></div>
```text
┌───────────────────────────┐
│           TOP_N           │
│    ────────────────────   │
│          ~5 Rows          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│        Expressions:       │
│             0             │
│             1             │
│         num_trips         │
│                           │
│         ~265 Rows         │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         AGGREGATE         │
│    ────────────────────   │
│          Groups:          │
│        pickup_zone        │
│        dropoff_zone       │
│                           │
│        Expressions:       │
│        count_star()       │
│                           │
│         ~265 Rows         │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      COMPARISON_JOIN      │
│    ────────────────────   │
│      Join Type: INNER     │
│                           │
│        Conditions:        ├───────────────────────────────────────────┐
│   (pickup_location_id =   │                                           │
│         LocationID)       │                                           │
│                           │                                           │
│       ~1977517 Rows       │                                           │
└─────────────┬─────────────┘                                           │
┌─────────────┴─────────────┐                             ┌─────────────┴─────────────┐
│      COMPARISON_JOIN      │                             │          SEQ_SCAN         │
│    ────────────────────   │                             │    ────────────────────   │
│      Join Type: INNER     │                             │          Filters:         │
│                           │                             │  Borough='Manhattan' AND  │
│        Conditions:        ├──────────────┐              │     Borough IS NOT NULL   │
│   (dropoff_location_id =  │              │              │                           │
│         LocationID)       │              │              │        zone_lookups       │
│                           │              │              │                           │
│       ~12744000 Rows      │              │              │          ~45 Rows         │
└─────────────┬─────────────┘              │              └───────────────────────────┘
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│          SEQ_SCAN         ││          SEQ_SCAN         │
│    ────────────────────   ││    ────────────────────   │
│       taxi_data_2019      ││          Filters:         │
│                           ││  Borough='Manhattan' AND  │
│                           ││     Borough IS NOT NULL   │
│                           ││                           │
│                           ││        zone_lookups       │
│                           ││                           │
│       ~84393604 Rows      ││          ~45 Rows         │
└───────────────────────────┘└───────────────────────────┘
```

Let's first look at the difference in execution times on my Macbook with an M1 Max and 32 GB of memory before talking about the optimizations that have taken place.

|          | Unoptimized | Optimized |
|----------|-------------|-----------|
| Runtime  | >24 hours   | 0.769 s   |

Hopefully this performance benefit illustrates how powerful the DuckDB Optimizer is. So what optimization rules are responsible for these drastic performance improvements? For the query above, there are three powerful rules that are applied when optimizing the query: _Filter Pushdown,_ _Join Order Optimization,_ and _TopN Optimization_.

The _Filter Pushdown Optimizer_ is very useful since it reduces the amount of intermediate data being processed. It is an optimization rule that is sometimes easy to miss for humans and will always result in faster execution times if the filter is selective in any way. It takes a filter, like `Borough = 'Manhattan'` and pushes it down to the operator that first introduces the filtered column, in this case the table scan. In addition, it will also detect when a filtered column like `col1` is used in an equality condition (i.e., `WHERE col1 = col2`). In these cases, the filter is duplicated and applied to the other column, `col2`, further reducing the amount of intermediate data being processed.

The _Join Order Optimizer_ recognizes that the filters `pickup.LocationID = data.pickup_location_id` and `dropoff.LocationID = data.dropoff_location_id` can be used as join conditions and rearranges the scans and joins accordingly. This optimizer rule does a lot of heavy lifting to reduce the amount of intermediate data being processed since it is responsible for removing the cross products.

The _TopN Optimizer_ is very useful when aggregate data needs to be sorted. If a query has an `ORDER BY` and a `LIMIT` operator, a TopN operator can replace these two operators. The TopN operator orders only the highest/lowest `N` values, instead of all values. If `N` is 5, then DuckDB only needs to keep 5 rows with the minimum/maximum values in memory and can throw away the rest. So if you are only interested in the top `N` values out of `M`, where `N << M`, the TopN operator can run in `O(M + N * log N)` instead of `O(M * log M)`.

These are just a few of the optimizations DuckDB has. More optimizations are explained in the section [Summary of All Optimizers](#summary-of-all-optimizers).

## Hand-Optimized Queries

For the query above, it is possible to achieve almost the same plan by carefully writing the SQL query by hand. To achieve a similar plan as the one generated by DuckDB, you can write the following.

```sql
SELECT 
    pickup.zone AS pickup_zone,
    dropoff.zone AS dropoff_zone,
    count(*) AS num_trips
FROM
    taxi_data_2019 data
INNER JOIN
    (SELECT * FROM zone_lookups WHERE Borough = 'Manhattan') pickup
    ON pickup.LocationID = data.pickup_location_id
INNER JOIN
    (SELECT * FROM zone_lookups WHERE Borough = 'Manhattan') dropoff
    ON dropoff.LocationID = data.dropoff_location_id
GROUP BY pickup_zone, dropoff_zone
ORDER BY num_trips desc
LIMIT 5;
```

Inspecting the runtimes again we get:

|          | Unoptimized | Hand-optimized | Optimized |
|----------|-------------|----------------|-----------|
| Runtime  | >24 hours   | 0.926 s        | 0.769 s   |

The SQL above results in a plan similar to the DuckDB optimized plan, but it is wordier and more error-prone to write, which can potentially lead to bugs. In very rare cases, it is possible to hand write a query that produces a more efficient plan than an optimizer. These cases are extreme outliers, and in all other cases the optimizer will produce a better plan. Moreover, a hand-optimized query is optimized for the current state of the data, which can change with many updates over time. Once a sufficient amount of changes are applied to the data, the assumptions of a hand-optimized query may no longer hold, leading to bad performance. Let's take a look at the following example.

Suppose an upstart company has an `orders` and `parts` table and every time some dashboard loads, the most popular ordered parts needs to be calculated. Since the company is still relatively new, they only have a small amount orders, but their catalog of parts is still quite large. A hand-optimized query would look like this:

```sql
CREATE OR REPLACE TABLE orders AS
    SELECT RANGE order_id, range % 10_000 pid FROM range(1_000);
CREATE TABLE parts AS
    SELECT range p_id, range::VARCHAR AS part_name FROM range(10_000);
SELECT
    parts.p_id,
    parts.part_name,
    count(*) as ordered_amount
FROM parts
INNER JOIN orders 
    ON orders.pid = parts.p_id
GROUP BY ALL;
```

Naturally, the number of orders will increase as this company gains customers and grows in popularity. If the query above continues to run without the use of an optimizer, the performance will slowly decline. This is because the execution engine will build the hash table on the orders table, which potentially will have 100 million rows. If the optimizer is enabled, the [Join Order Optimizer](#join-order-optimizer) will be able to inspect the statistics of the table during the optimization process and produce a new plan according to the new state of the data.

Here is a breakdown of running the queries with and without the optimizer as the orders table increases.

|                   | Unoptimized | Optimized |
|-------------------|------------:|----------:|
| \|orders\| = 1K   | 0.004 s     | 0.003 s   |
| \|orders\| = 10K  | 0.005 s     | 0.005 s   |
| \|orders\| = 100K | 0.013 s     | 0.008 s   |
| \|orders\| = 1M   | 0.055 s     | 0.014 s   |
| \|orders\| = 10M  | 0.240 s     | 0.044 s   |
| \|orders\| = 100M | 2.266 s     | 0.259 s   |

At first the difference in execution time is not really noticeable, so no one would think a query rewrite would be the solution. But once enough orders are reached, waiting 2 seconds every time the dashboard loads becomes tedious. If the optimizer is enabled, the query performance improves by a factor of 10×. So if you ever think you have identified a scenario where you are smarter than the optimizer, make sure you have also thought about all possible updates to the data and have hand-optimized for those as well.

## Optimizations That Are Impossible by Hand

Some optimization rules are also impossible to write by hand. For example, the TopN optimization can not be optimized by hand.

Another good example is the Join Filter Pushdown optimization. The Join Filter Pushdown optimization works in scenarios where the build side of a hash join has a subset of the join keys. In its current state the join filter pushdown optimization keeps track of the minimum value key and maximum value key and pushes a table filter into the probe side to filter out keys greater than the maximum join value and smaller than the minimum join value.

With a small change, we can use the query from above to demonstrate this. Suppose we first filter our `parts` table to only include parts with a specific prefix in the `part_name`. When the `orders` table has 100 million rows and the `parts` table only has ~20,000 after filtering, then the `orders` table will be the probe side and the `parts` table will be the hash/build side. When the hash table is built, the min and max `p_id` values in the `parts` table are recorded, in this case it could be 20,000 and 80,000. These min and max values get pushed as a filter into the `orders` table scan, filtering out all parts with `p_id > 80,000` and `pid < 20,000`. 40% of the `orders` table has a `pid` greater than 80,000, and less than 20,000 so this optimization does a lot of heavy lifting in join queries.

Imagine trying to express this logic in your favorite data frame API; it would be extremely difficult and error-prone. The library would need to implement this optimization automatically for all hash joins. The Join Filter Pushdown optimization can improve query performance by 10x, so it should be a key factor when deciding what analytical system to use.

If you use a data frame library like [collapse](https://github.com/SebKrantz/collapse), [pandas](https://github.com/pandas-dev/pandas), [data.table](https://github.com/Rdatatable/data.table), [modin](https://github.com/modin-project/modin), then you are most likely not enjoying the benefits of query optimization techniques. This means your optimizations need to be applied by hand, which is not sustainable if your data starts changing. Moreover, you are most likely writing imperatively, using a syntax specific to the dataframe library. This means the scripts responsible for analyzing data are not very portable. SQL, on the other hand, can be much more intuitive to write since it is a declarative language, and can be ported to practically any other database system.

## Summary of All Optimizers

Below is a non-exhaustive list of all the optimization rules that DuckDB applies.

### Expression Rewriter

The _Expression Rewriter_ simplifies expressions within each operator. Sometimes queries are written with expressions that are not completely evaluated or they can be rewritten in a way that takes advantage of features within the execution engine. Below is a table of common expression rewrites and the optimization rules that are responsible for them. Many of these rules rewrite expressions to use specialized DuckDB functions so expression evaluation is much faster during execution. If an expression can be evaluated to `true` in the optimizer phase, there is no need to pass the original expression to the execution engine. In addition, the optimized expressions are more likely to allow DuckDB to make further improvements to the query plan. For example, the "Move constants" rule could enable filter pushdown to occur.

| Rewriter rule                  | Original expression                   | Optimized expression       |
|--------------------------------|---------------------------------------|----------------------------|
| Move constants                 | `x + 1 = 6`                           | `x = 5`                    |
| Constant folding               | `2 + 2 = 4`                           | `true`                     |
| Conjunction simplification     | `(1 = 2 AND b)`                       | `false`                    |
| Arithmetic simplification      | `x * 1`                               | `x`                        |
| Case simplification            | `CASE WHEN true THEN x ELSE y END`    | `x`                        |
| Equal or `NULL` simplification | `a = b OR (a IS NULL AND b IS NULL)`  | `a IS NOT DISTINCT FROM b` |
| Distributivity                 | `(x AND b) OR (x AND c) OR (x AND d)` | `x AND (b OR c OR d)`      |
| Like optimization              | `regexp_matches(c, '^Prefix')`        | `LIKE 'Prefix%'`           |

### Filter Pull-Up & Filter Pushdown

_Filter Pushdown_ was explained briefly above. _Filter Pull-Up_ is also important to identify cases where a filter can be applied on columns in other tables. For example, the query below scans column `a` from both `t1` and `t2`. `t1.a` has a filter, but in the presence of the equality condition, `t2.a` can have the same filter. For example:

```sql
SELECT *
FROM t1, t2
WHERE t1.a = t2.a
  AND t1.a = 50;
```

This can be optimized to:

```sql
SELECT *
FROM t1, t2
WHERE t1.a = t2.a
  AND t1.a = 50
  AND t2.a = 50;
```

_Filter Pull-Up_ pulls up the filter `t1.a = 50` above the join, and when the filter is pushed down again, the optimizer rule recognizes the filter can be applied to both columns `t1.a` and `t2.a`.

### IN Clause Rewriter

If there is a filter with an `IN` clause, sometimes it can be re-written so execution is more efficient. Some examples are below:

| Original          | Optimized             |
|-------------------|-----------------------|
| `c1 IN (1)`       | `c1 = 1`              |
| `c1 IN (3, 4, 5)` | `c1 >= 3 AND c1 <= 5` |

In addition, the _IN Clause Rewriter_ will transform expensive `IN` expressions into `MARK` joins. If a query has an expression like `c1 IN (x1, ..., xn)` where `n` is quite large, it can be expensive to evaluate this expression for every row in the table. The runtime would be `O(n * m)` where `n` is the number of rows and `m` is the length of the list. The `IN` clause rewriter will transform the expression into `SELECT c1 FROM t1, VALUES (x1, ..., xn) t(c0) WHERE c1 = c0` turning the expression into a `HASH` join that can complete in `O(n + m)` time!

### Join Order Optimizer

The _Join Order Optimizer_ can provide an enormous performance benefit by limiting the number of intermediate tuples that are processed between joins. By processing fewer intermediate tuples, the query can execute faster.

### Statistics Propagation

_Statistics Propagation_ is another optimization that works even when the state of the data changes. By traversing the query plan and keeping note of all equality join conditions, the Statistics Propagation optimizer can create new filters by inspecting the statistics of the columns that are eventually joined. For example, suppose `t1.a` and `t2.a` will be joined with the equality condition `t1.a = t2.a`.  If our internal statistics tell us `t1.a` has a maximum value of `50` and a minimum value of `25`, the optimizer can create a new filter when scanning table `t2`. The filter would be `t2.a >= 25 AND t2.a <= 50`.

### Reorder Filters

If there are multiple filters on a column, the order in which these filters are executed also becomes important. It's best to execute the most efficient filters first, saving execution of expensive filters for later. For example, DuckDB can evaluate equality very quickly. So for a query like `... WHERE a = 50 AND md5(b) LIKE '%d77%'`, the optimizer will tell DuckDB to evaluate `a = 50` on every column first. If the value in column `a` passes the check `a = 50`, DuckDB will evaluate the `md5` hash for the values in column `b`.

## Conclusion

A well-written optimizer can provide significant performance improvements when allowed to optimize freely. Not only can the optimizer apply the many optimization rules a human might naturally miss, an optimizer can respond to changes in the data. Some optimizations can result in a performance improvement of 100×, which might be the difference when deciding to use analytical system _A_ vs. analytical system _B_. With DuckDB, all optimization rules are applied automatically to every query, so you can continually enjoy the benefits. Hopefully this blog post has convinced you to consider the optimizer next time you hear about the next database that has everyone's ears burning.

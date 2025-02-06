---
layout: docu
railroad: statements/samples.js
title: Samples
---

Samples are used to randomly select a subset of a dataset.

### Examples

Select a sample of exactly 5 rows from `tbl` using `reservoir` sampling:

```sql
SELECT *
FROM tbl
USING SAMPLE 5;
```

Select a sample of *approximately* 10% of the table using `system` sampling:

```sql
SELECT *
FROM tbl
USING SAMPLE 10%;
```

> Warning By default, when you specify a percentage, each [*vector*]({% link docs/archive/1.1/internals/vector.md %}) is included in the sample with that probability. If your table contains fewer than ~10k rows, it makes sense to specify the `bernoulli` sampling option instead, which applies the probability to each row independently. Even then, you'll sometimes get more and sometimes less than the specified percentage of the number of rows, but it is much less likely that you get no rows at all. To get exactly 10% of rows (up to rounding), you must use the `reservoir` sampling option.

Select a sample of *approximately* 10% of the table using `bernoulli` sampling:

```sql
SELECT *
FROM tbl
USING SAMPLE 10 PERCENT (bernoulli);
```

Select a sample of *exactly* 10% (up to rounding) of the table using `reservoir` sampling:

```sql
SELECT *
FROM tbl
USING SAMPLE 10 PERCENT (reservoir);
```

Select a sample of *exactly* 50 rows of the table using reservoir sampling with a fixed seed (100):

```sql
SELECT *
FROM tbl
USING SAMPLE reservoir(50 ROWS)
REPEATABLE (100);
```

Select a sample of *approximately* 20% of the table using `system` sampling with a fixed seed (377):

```sql
SELECT *
FROM tbl
USING SAMPLE 20% (system, 377);
```

Select a sample of *approximately* 20% of `tbl` **before** the join with `tbl2`:

```sql
SELECT *
FROM tbl TABLESAMPLE reservoir(20%), tbl2
WHERE tbl.i = tbl2.i;
```

Select a sample of *approximately* 20% of `tbl` **after** the join with `tbl2`:

```sql
SELECT *
FROM tbl, tbl2
WHERE tbl.i = tbl2.i
USING SAMPLE reservoir(20%);
```

### Syntax

<div id="rrdiagram"></div>

Samples allow you to randomly extract a subset of a dataset. Samples are useful for exploring a dataset faster, as often you might not be interested in the exact answers to queries, but only in rough indications of what the data looks like and what is in the data. Samples allow you to get approximate answers to queries faster, as they reduce the amount of data that needs to pass through the query engine.

DuckDB supports three different types of sampling methods: `reservoir`, `bernoulli` and `system`. By default, DuckDB uses `reservoir` sampling when an exact number of rows is sampled, and `system` sampling when a percentage is specified. The sampling methods are described in detail below.

Samples require a *sample size*, which is an indication of how many elements will be sampled from the total population. Samples can either be given as a percentage (`10%` or `10 PERCENT`) or as a fixed number of rows (`10` or `10 ROWS`). All three sampling methods support sampling over a percentage, but **only** reservoir sampling supports sampling a fixed number of rows.

Samples are probablistic, that is to say, samples can be different between runs *unless* the seed is specifically specified. Specifying the seed *only* guarantees that the sample is the same if multi-threading is not enabled (i.e., `SET threads = 1`). In the case of multiple threads running over a sample, samples are not necessarily consistent even with a fixed seed.

### `reservoir`

Reservoir sampling is a stream sampling technique that selects a random sample by keeping a *reservoir* of size equal to the sample size, and randomly replacing elements as more elements come in. Reservoir sampling allows us to specify *exactly* how many elements we want in the resulting sample (by selecting the size of the reservoir). As a result, reservoir sampling *always* outputs the same amount of elements, unlike system and bernoulli sampling.

Reservoir sampling is only recommended for small sample sizes, and is not recommended for use with percentages. That is because reservoir sampling needs to materialize the entire sample and randomly replace tuples within the materialized sample. The larger the sample size, the higher the performance hit incurred by this process.

Reservoir sampling also incurs an additional performance penalty when multi-processing is used, since the reservoir is to be shared amongst the different threads to ensure unbiased sampling. This is not a big problem when the reservoir is very small, but becomes costly when the sample is large.

> Bestpractice Avoid using reservoir sampling with large sample sizes if possible.
> Reservoir sampling requires the entire sample to be materialized in memory.

### `bernoulli`

Bernoulli sampling can only be used when a sampling percentage is specified. It is rather straightforward: every row in the underlying table is included with a chance equal to the specified percentage. As a result, bernoulli sampling can return a different number of tuples even if the same percentage is specified. The *expected* number of rows is equal to the specified percentage of the table, but there will be some *variance*.

Because bernoulli sampling is completely independent (there is no shared state), there is no penalty for using bernoulli sampling together with multiple threads.

### `system`

System sampling is a variant of bernoulli sampling with one crucial difference: every *vector* is included with a chance equal to the sampling percentage. This is a form of cluster sampling. System sampling is more efficient than bernoulli sampling, as no per-tuple selections have to be performed.

The *expected* number of rows is still equal to the specified percentage of the table, but the *variance* is `vectorSize` times higher. As such, system sampling is not suitable for data sets with fewer than ~10k rows, where it can happen that all rows will be filtered out, or all the data will be included, even when you ask for `50 PERCENT`.

## Table Samples

The `TABLESAMPLE` and `USING SAMPLE` clauses are identical in terms of syntax and effect, with one important difference: tablesamples sample directly from the table for which they are specified, whereas the sample clause samples after the entire from clause has been resolved. This is relevant when there are joins present in the query plan.

The `TABLESAMPLE` clause is essentially equivalent to creating a subquery with the `USING SAMPLE` clause, i.e., the following two queries are identical:

Sample 20% of `tbl` **before** the join:

```sql
SELECT *
FROM
    tbl TABLESAMPLE reservoir(20%),
    tbl2
WHERE tbl.i = tbl2.i;
```

Sample 20% of `tbl` **before** the join:

```sql
SELECT *
FROM
    (SELECT * FROM tbl USING SAMPLE reservoir(20%)) tbl,
    tbl2
WHERE tbl.i = tbl2.i;
```

Sample 20% **after** the join (i.e., sample 20% of the join result):

```sql
SELECT *
FROM tbl, tbl2
WHERE tbl.i = tbl2.i
USING SAMPLE reservoir(20%);
```
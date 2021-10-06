---

layout: post
title:  "Windowing in DuckDB"
author: Richard Wesley
excerpt_separator: <!--more-->

---

_TLDR: DuckDB, a free and Open-Source analytical data management system, uses state-of-the art windowing for high performance._

<!--more-->

## Under the Feathers

That is a long list of functionality, so lets have a look at how it gets implemented in DuckDB.

### Pipeline Breaking

The first thing to notice is that windowing is a "pipeline breaker".
That is, the Window operator has to read all of its inputs before it can start computing a function.
This means that if there is some other way to compute something,
it may well be faster to use a different technique.

One common analytic task is to find the last value in some group.
It is tempting to use the `RANK()` window function with a reverse sort for this task:

```sql
SELECT entity, value
FROM (
    SELECT entity, value,
        RANK() OVER (PARTITION BY entity ORDER BY date DESC) AS rank
    FROM table) t
WHERE rank = 1
```

but this requires materialising the entire table, partitioning it, sorting the partitions,
and then pulling out a single row from those partitions.
A much faster way to do this is to use a self join to filter the table:

```sql
SELECT entity, value
FROM table,
     (SELECT entity, MAX(date) AS date FROM table GROUP BY 1) dates
WHERE table.entity = dates.entity
  AND table.date = dates.date
```

This query requires two scans of the table, but the only materialised data is the filtering table
(which is probably much smaller than the original table), and there is no sorting at all.
This showed up [in a user's blog](https://bwlewis.github.io/duckdb_and_r/last/last.html)
and we found that the second query was about 20 times faster:

<img src="/images/blog/windowing/last-in-group.jpg" alt="Window takes 13 seconds, Join takes half a second" title="Last in Group Performance Comparison" style="max-width:70%"/>

Of course most analytic tasks that use windowing *do* require using the operator,
and DuckDB uses a collection of modern techniques to make the performance as fast as possible.

### Partitioning and Sorting

At one time, windowing was implemented by sorting on both the partition and the ordering fields.
This is resource intensive, both because the entire relation must be sorted,
and because sorting is `O(N log N)` in the size of the relation.
To reduce resource consumption, we use the hash partitioning scheme from
[Efficient Processing of Window Functions in Analytical SQL Queries](http://www.vldb.org/pvldb/vol8/p1058-leis.pdf). This breaks the partitions up into 1024 chunks using hashing.
The chunks still need to be sorted on all the fields because there may be hash collisions,
but each partition can now be 1024 times smaller, which reduces the runtime significantly.
Moreover, the partitions can easily be extracted and processed in parallel.

Sorting in DuckDB recently got a [big performance boost](/2021/08/27/external-sorting)
along with the ability to work on partitions that were larger than memory.
This functionality has been also added to the Window operator,
resulting in improvements in the last-in-group example:

<img src="/images/blog/windowing/last-in-group-sort.jpg" alt="Window takes X seconds, Join takes half a second" title="Last in Group Sorting Performance Comparison" style="max-width:70%"/>

### Aggregation

Most of the [general-purpose window functions](/docs/sql/window_functions) are straightforward to compute,
but windowed aggregate functions can be expensive because they need to look at multiple values for each row.
They often need to look at the same value multiple times, or repeatedly look at a large number of values,
so over the years several approaches have been taken to improve performance.

#### Basic Windowed Aggregation

Before explaining how DuckDB implements windowed aggregation,
we need to take a short detour through how regular aggregates are implemented.
Aggregate "functions" are implemented using a set of three or more operations:
* Initialize - Creates a state that will be updated. For `SUM`, this is `NULL`.
* Update - Updates the state with a new value. For `SUM`, this adds the value to the state.
* Finalize - Produces the final aggregate value from the state. For `SUM`, this just copies the value.
* Combine - Combines two states into a single state. This is optional, but when present it allows the aggregate to be computed in parallel. For `SUM`, this produces a new state with the sum of the two input values.

The simplest way to compute a windowed aggregate is to *initialize* a state,
*update* the state with all the values in the window frame,
and then use *finalize* to produce the result of the aggregate.
This naïve algorithm will always work, but it is quite inefficient.
To improve on this, some databases add additional
["moving state" operations](https://www.postgresql.org/docs/14/sql-createaggregate.html)
that can add or remove individual values incrementally.
This is an improvement, but it can only be used for certain aggregates (for example, it doesn't work for `MIN`).
Moreover, if the frame boundaries move around a lot, it can degenerate badly to `O(N^2)` run time.

#### Segment Tree Aggregation

Instead, DuckDB uses the *segment tree* approach, again from
[Efficient Processing of Window Functions in Analytical SQL Queries](http://www.vldb.org/pvldb/vol8/p1058-leis.pdf).
This works by building a tree on top of the entire partition with the aggregated values at the bottom.
Values are combined into states at nodes above them in the tree until there is a single root:

<img src="/images/blog/windowing/segment-tree.png" alt="Segment Tree for SUM aggregation" title="Figure 5: Segment Tree for sum aggregation. Only the red nodes (7, 13, 20) have to be aggregated to compute the sum of 7, 3, 10, 6, 2, 8, 4" style="max-width:70%"/>

To compute a value, the algorithm generates states for the ragged ends of the frame,
*combines* states in the tree above the values in the frame,
and *finalizes* the result from the last remaining state.
This can be used for all combinable aggregates.

#### General Windowed Aggregation

The biggest drawback of segment trees is the need to manage a potentially large number of intermediate states.
For the simple states used for standard aggregates,
this is not a problem because the states are small,
the tree keeps the number of states logarithmically low,
and the state used to compute each value is cheap.

For some aggregates, however, the state is not small.
Typically these are so-called *holistic* aggregates,
where the value depends on all the values of the frame.
Examples of such aggregates are `mode` and `quantile`,
where each state may have to contain a copy of *all* the values seen so far.
For large frames, this can be quite expensive.

To solve this problem, we use the approach from
[Incremental Computation of Common Windowed Holistic Aggregates](http://www.vldb.org/pvldb/vol9/p1221-wesley.pdf),
which generalises segment trees to aggregate-specific data structures.
The aggregate can define a fifth *window* operation,
which will be given the bottom of the tree and the bounds of the current and previous frame.
The aggregate can then create an appropriate data structure for its implementation.
For example, the `mode` function maintains a hash table of counts that it can update efficiently,
and the `quantile` function maintains a partially sorted list of frame indexes.

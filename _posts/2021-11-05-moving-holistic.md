---

layout: post
title:  "Fast Moving Holistic Aggregates"
author: Richard Wesley
excerpt_separator: <!--more-->

---

_TLDR: DuckDB, a free and Open-Source analytical data management system, has a windowing API
that can compute complex moving aggregates like interquartile ranges and median absolute deviation
much faster than the conventional approaches._

In a [previous post](/2021/10/13/windowing.html),
we described the DuckDB windowing architecture and mentioned the support for
some advanced moving aggregates.
In this post, we will compare the performance various possible moving implementations of these functions
and explain how DuckDB's performant implementations work.

<!--more-->

## What is an Aggregate Function?

When people think of aggregate functions, they typically have something simple in mind such as `SUM` or `AVG`.
But more generally, what an aggregate function does is _summarise_ a set of values into a single value.
Such summaries can be arbitrarily complex, and involve any data type.
For example, DuckDB provides aggregates for concatenating strings (`STRING_AGG`)
and constructing lists (`LIST`).
In SQL, aggregated sets come from either a `GROUP BY` clause or an `OVER` windowing specification.

### Holistic Aggregates

All of the basic SQL aggregate functions like `SUM` and `MAX` can be computed
by reading values one at a time and throwing them away.
But there are some functions that potentially need to keep track of all the values before they can produce a result.
These are called _holistic_ aggregates, and they require more care when implementing.

For some aggregates (like `STRING_AGG`) the order of the values can change the result.
This is not a problem for windowing because `OVER` clauses can specify an ordering,
but in a `GROUP BY` clause, the values are unordered.
To handle this, order sensitive aggregates can include a `WITHIN GROUP(ORDER BY <expr>)` clause
to specify the order of the values.
Because the values must all be collected and sorted,
aggregates that use the `WITHIN GROUP` clause are holistic.

### Statistical Holistic Aggregates

Because sorting the arguments to a windowed aggregate can be specified with the `OVER` clause,
you might wonder if there are any other kinds of holistic aggregates that do not use sorting,
or which use an ordering different from the one in the `OVER` clause.
It turns out that there are a number of important statistical functions that
turn into holistic aggregates in SQL.
In particular, here are the statistical holistic aggregates that DuckDB currently supports:

| Function | Description|
|:---|:---|
| `mode(x)` | The most common value in a set |
| `median(x)` | The middle value of a set |
| `quantile_disc(x, <frac>)` | The exact value corresponding to a fractional position. |
| `quantile_cont(x, <frac>)` | The interpolated value corresponding to a fractional position. |
| `quantile_disc(x, [<frac>...])` | A list of the exact values corresponding to a list of fractional positions. |
| `quantile_cont(x, [<frac>...])` | A list of the interpolated value corresponding to a list of fractional positions. |
| `mad(x)` | The median of the absolute values of the differences of each value from the median. |

Where things get really interesting is when we try to compute moving versions of these aggregates.
For example, computing a moving `AVG` is fairly straightforward:
You can subtract values that have left the frame and add in the new ones,
or use the segment tree approach from the [previous post on windowing](/2021/10/13/windowing.html).

### Python Example

Computing a moving median is not as easy.
Let's look at a simple example of how we might implement moving `median` in Python
for the following string data, using a frame that includes one element from each side:

<img src="/images/blog/holistic/python.svg" alt="Python Median Example" title="Figure 1: Python Median Example" style="max-width:90%;width:90%;height:auto"/>

For this example we are using strings so we don't have to worry about interpolating values.

```py
data = ('a', 'b', 'c', 'd', 'c', 'b',)
w = len(data)
for row in range(w):
    l = max(row - 1, 0)       # First index of the frame
    r = min(row + 1, w-1)     # Last index of the frame
    frame = list(data[l:r+1]) # Copy the frame values
    frame.sort()              # Sort the frame values
    n = (r - l) // 2          # Middle index of the frame
    median = frame[n]         # The median is the middle value
    print(row, data[row], median)
```

Each frame has a different set of values to aggregate and we can't change the order in the table,
so we have to copy them each time before we sort.
Sorting is slow, and there is a lot of repetition.

All of these holistic aggregates have similar problems
if we just reuse the simple implementations for moving versions.
Fortunately, there are much faster approaches for all of them.

## Moving Holistic Aggregation

In the [previous post on windowing](/2021/10/13/windowing.html),
we explained the component operations used to implement a generic aggregate function
(initialize, update, finalize, combine and window).
In the rest of this post, we will dig into how they can be implemented for these complex aggregates.

### Quantile

The `quantile` aggregate variants all extract the value(s) at a given fraction (or fractions) of the way
through the ordered list of values in the set.
The simplest variant is the `median` function, which we met in the introduction, which uses a fraction of `0.5`.
There are other variants depending on whether the values are
quantitative (i.e., they have a distance and the values can be interpolated)
or merely ordinal (i.e., they can be ordered, but ties have to be broken.)
Still other variants depend on whether the fraction is a single value or a list of values,
but they can all be implemented in similar ways.

A common way to implement `quantile` that we saw in the Python example is to collect all the values into the state,
sort them, and then read out the values at the requested positions.
(This is probably why the SQL standard refers to it as an "ordered-set aggregate".)
States can be combined by concatenation,
which lets us group in parallel and build segment trees for windowing.

This approach is very time-consuming because sorting is `O(N log N)`,
but happily for `quantile` we can use a related algorithm called `QuickSelect`,
which can find a positional value in only `O(N)` time by _partially sorting_ the array.
You may have run into this algorithm if you have ever used the
`std::nth_element` algorithm in the C++ standard library.
This works well for grouped quantiles, but for moving quantiles
the segment tree approach ends up being about 5% slower than just starting from scratch for each value.

To really improve the performance of moving quantiles,
we note that the partial order probably does not change much between frames.
If we maintain a list of indirect indicies into the window and call `nth_element` on the indicies,
we can reorder the partially ordered indicies instead of the values themselves.
In the common case where the frame has the same size,
we can even check to see whether the new value disrupts the partial ordering at all,
and skip the reordering!
With this approach, we can obtain a significant performance boost of 1.5-10 times.

In this example, we have a 3-element frame (green) that moves one space to the right for each value:

<img src="/images/blog/holistic/median.svg" alt="Median Example" title="Figure 2: Median Example" style="max-width:90%;width:90%;height:auto"/>

The median values in orange must be computed from scratch.
Notice that in the example, this only happens at the start of the window.
The median values in white are computed using the existing partial ordering.
In the example, this happens when the frame changes size.
Finally, the median values in blue do not require reordering
because the new value is the same as the old value.
With this algorithm, we can create a faster implementation of single-fraction `quantile` without sorting.

### InterQuartile Ranges (IQR)

We can extend this implementation to _lists_ of fractions by leveraging the fact that each call to `nth_element`
partially orders the values, which further improves performance.
The "reuse" trick can be generalised to distinguish between fractions that are undisturbed
and ones that need to be recomputed.

A common application of multiple fractions is computing
[interquartile ranges](https://en.wikipedia.org/wiki/Interquartile_range)
by using the fraction list `[0.25, 0.5, 0.75]`.
This is the fraction list we use for the multiple fraction benchmarks.
Combined with moving `MIN` and `MAX`,
this moving aggregate can be used to generate the data for a moving box-and-whisker plot.

### Median Absolute Deviation (MAD)

Maintaining the partial ordering can also be used to boost the performance of the
[median absolute deviation](https://en.wikipedia.org/wiki/Median_absolute_deviation)
(or `mad`) aggregate.
Unfortunately, the second partial ordering can't use the single value trick
because the "function" being used to partially order the values will have changed if the data median changes.
Still, the values are still probably not far off,
which again improves the performance of `nth_element`.

### Mode

The `mode` aggregate returns the most common value in a set.
One common way to implement it is to accumulate all the values in the state,
sort them and then scan for the longest run.
These states can be combined by merging,
which lets us compute the mode in parallel and build segment trees for windowing.

Once again, this approach is very time-consuming because sorting is `O(N log N)`.
It may also use more memory than necessary because it keeps _all_ the values
instead of keeping only the unique values.
If there are heavy-hitters in the list,
(which is typically what `mode` is being used to find)
this can be significant.

Another way to implement `mode` is to use a hash map for the state that maps values to counts.
Hash tables are typically `O(N)` for accumulation, which is an improvement on sorting,
and they only need to store unique values.
If the state also tracks the largest value and count seen so far,
we can just return that value when we finalize the aggregate.
States can be combined by merging,
which lets us group in parallel and build segment trees for windowing.

Unfortunately, as the benchmarks below demonstrate, this segment tree approach for windowing is quite slow!
The overhead of merging the hash tables for the segment trees turns out to be about 5% slower
than just building a new hash table for each row in the window.
But for a moving `mode` computation,
we can instead make a single hash table and update it every time the frame moves,
removing the old values, adding the new values, and updating the value/count pair.
At times the current mode value may have its count decremented,
but when that happens we can rescan the table to find the new mode.

In this example, the 4-element frame (green) moves one space to the right for each value:

<img src="/images/blog/holistic/mode.svg" alt="Mode Example" title="Figure 3: Mode Example" style="max-width:90%;width:90%;height:auto"/>

When the mode is unchanged (blue) it can be used directly.
When the mode becomes ambiguous (orange), we must recan the table.
This approach is much faster,
and in the benchmarks it comes in between 15 and 55 times faster than the other two.

## Micro-Benchmarks

To benchmark the various implementations, we run moving window queries against a 10M table of integers:

```sql
create table rank100 as
    select b % 100 as a, b from range(10000000) tbl(b)
```

The results are then re-aggregated down to one row to remove the impact of streaming the results.
The frames are 100 elements wide, and the test is repeated with a fixed trailing frame:

```sql
select quantile_cont(a, [0.25, 0.5, 0.75]) over (
    order by b asc
    rows between 100 preceding and current row) as iqr
from rank100
```

and a variable frame that moves pseudo-randomly around the current value:

```sql
select quantile_cont(a, [0.25, 0.5, 0.75]) over (
    order by b asc
    rows between mod(b * 47, 521) preceding and 100 - mod(b * 47, 521) following) as iqr
from rank100
```

The two examples here are the interquartile range queries;
the other queries use the single argument aggregates `median`, `mad` and `mode`.

As a final step, we ran the same query with `COUNT(*)`,
which has the same overhead as the other benchmarks, but is trivial to compute
(it just returns the frame size).
That overhead was subtracted from the run times to give the algorithm timings:

<img src="/images/blog/holistic/benchmarks.svg" alt="Holistic Aggregate Benchmarks" title="Figure 3: Holistic Aggregate Benchmarks" style="max-width:90%;width:90%;height:auto"/>

As can be seen, there is a substantial benefit from implementing the window operation
for all of these aggregates, often on the order of a factor of ten.

An unexpected finding was that the segment tree approach for these complex states
is always slower (by about 5%) than simply creating the state for each output row.
This suggests that when writing combinable complex aggregates,
it is well worth benchmarking the aggregate
and then considering providing a window operation instead of deferring to the segment tree machinery.

## Conclusion

DuckDB's aggregate API enables aggregate functions to define a windowing operation
that can significantly improve the performance of moving window computations for complex aggregates.
This functionality has been used to significantly speed up windowing for several statistical aggregates,
such as mode, interquartile ranges and median absolute deviation.

DuckDB is a free and open-source database management system (MIT licensed).
It aims to be the SQLite for Analytics,
and provides a fast and efficient database system with zero external dependencies.
It is available not just for Python, but also for C/C++, R, Java, and more.

[Discuss this post on Hacker News](https://news.ycombinator.com/newest)

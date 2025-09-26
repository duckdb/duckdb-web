---
layout: post
title: "Redesigning DuckDB's Sort, Again"
author: "Laurens Kuiper"
thumb: "/images/blog/thumbs/sorting-again.svg"
image: "/images/blog/thumbs/sorting-again.png"
excerpt: "After four years, we've decided to redesign DuckDB's sort implementation, again. In this post, we present and evaluate the new design."
tags: ["deep dive"]
---

[DuckDB v1.4.0 was just released]({% post_url 2025-09-16-announcing-duckdb-140 %}), which includes a complete redesign of DuckDB's sort implementation.
We [redesigned DuckDB's sort just four years ago]({% post_url 2021-08-27-external-sorting %}), which allowed DuckDB to sort more data than fits in main memory, in parallel, with highly efficient comparisons.
This implementation served us well, but since then we've implemented larger-than-memory query processing for more operators, such as the [hash join](https://github.com/duckdb/duckdb/pull/4189) and [hash aggregation](https://github.com/duckdb/duckdb/pull/7931), which both use a new and improved [spillable page layout](https://github.com/duckdb/duckdb/pull/6998). We presented this layout in an [earlier blog post]({% post_url 2024-03-29-external-aggregation %}).
We decided to integrate this layout in DuckDB's sort, and [completely redesigned the implementation](https://github.com/duckdb/duckdb/pull/17584).

Not interested in the implementation? [Jump straight to the benchmark!](#benchmark)

## Two-Phase Sorting

DuckDB implements parallel query execution using [Morsel-Driven Parallelism](https://db.in.tum.de/~leis/papers/morsels.pdf).
In DuckDB's implementation of this framework, blocking operators, i.e., _operators that must read the entire input before they can output_, such as the hash aggregation and sort operators, have the following phases:

1. __Sink__: Thread-local accumulation of data from a pipeline
2. __Combine__: Signals a thread finishing its _Sink_ phase
3. __Finalize__: Called once when all threads have called _Combine_
4. __GetData__: Output data to the next pipeline

For many decades, the preferred option to implement larger-than-memory sorting in database systems has been to [generate multiple sorted runs, followed by a merge sort](https://dl.acm.org/doi/abs/10.1145/1132960.1132964).
Specifically, a [_k_-way merge sort](https://en.wikipedia.org/wiki/K-way_merge_algorithm) produces the lowest amount of I/O during larger-than-memory sorting, which is critical to performance.
This approach maps well to Morsel-Driven Parallelism: DuckDB performs thread-local sorting in the _Sink_ phase, followed by a parallel merge sort in the _Finalize_ or _GetData_ phase.
Both have been redesigned for DuckDB v1.4.0.
We first discuss the new thread-local sort implementation before presenting the new merge design.

## Thread-Local Sorting

Sorted runs are generated thread-locally in the _Sink_ phase.
The way DuckDB parallelizes this has not changed in v1.4.0: threads generate sorted runs independently, in parallel.
What has changed is the physical sorting implementation.

### Key Normalization

Database systems that do not compile the required types into the query plan – e.g., DuckDB – suffer from interpretation overhead, [especially when comparing tuples while sorting]({% link pdf/ICDE2023-kuiper-muehleisen-sorting.pdf %}).
One way to get around this is [Key Normalization](https://dl.acm.org/doi/pdf/10.1145/359863.359892).
DuckDB's sort already used an ad-hoc version of this prior to v1.4.0, but the new implementation uses the more generic [`create_sort_key`](https://github.com/duckdb/duckdb/pull/10321) function that is available through SQL.

This function takes any number of inputs and sort conditions, and constructs a `BLOB` field that produces the specified order.
An example from the description of the PR that implemented `create_sort_key`:

```sql
SELECT
    s,
    create_sort_key(s, 'asc nulls last') AS k1,
    create_sort_key(s, 'asc nulls first') AS k2
FROM
    (VALUES ('hello'), ('world'), (NULL)) t(s);
```

```text
┌─────────┬───────────────┬───────────────┐
│    s    │      k1       │      k2       │
│ varchar │     blob      │     blob      │
├─────────┼───────────────┼───────────────┤
│ hello   │ \x01ifmmp\x00 │ \x02ifmmp\x00 │
│ world   │ \x01xpsme\x00 │ \x02xpsme\x00 │
│ NULL    │ \x02          │ \x01          │
└─────────┴───────────────┴───────────────┘
```

Because of the binary-comparable nature of the constructed BLOB, the following queries are equivalent:

```sql
SELECT * FROM tbl
ORDER BY x DESC NULLS LAST, y ASC NULLS FIRST;

SELECT * FROM tbl
ORDER BY create_sort_key(x, 'DESC NULLS LAST', y, 'ASC NULLS FIRST');
```

This fixes the problem of interpretation overhead when comparing tuples, as we now only have to consider comparing `BLOB`s, instead of arbitrary combinations of types in an `ORDER BY` clause.

### Static Integer Comparisons

It's well known that processing strings is a lot slower than processing fixed-size types such as integers.
If we would always use the `create_sort_key` function, even for integers, we'd be leaving a lot of performance on the table.
However, if we know the size of the resulting `BLOB`, we can convert it back to one or more unsigned integers, and use integer comparisons instead.

For example, if we have the following query:

```sql
SELECT *
FROM tbl
ORDER BY
    c0::INTEGER ASC NULLS LAST,
    c1::DOUBLE ASC NULLS LAST;
```

The resulting `BLOB` from `create_sort_key(c0::INTEGER, 'ASC NULLS LAST', c1::DOUBLE, 'ASC NULLS LAST')` is less than 16 bytes, so the new sorting implementation will swap the bytes (for big-endian integer comparisons) and store them in two 64-bit unsigned integers.
A simplified version of the data structure we use in C++:

```cpp
struct FixedSortKeyNoPayload {
    uint64_t part0;
    uint64_t part1;
};
struct FixedSortKeyPayload {
    uint64_t part0;
    uint64_t part1;
    data_ptr_t payload;
};
```

Which can be compared like so:

```cpp
bool LessThan(const FixedSortKeyPayload &lhs, const FixedSortKeyPayload &rhs) {
    return lhs.part0 < rhs.part0 || (lhs.part0 == rhs.part0 && lhs.part1 < rhs.part1);
}
```

The `payload` field is only present if more columns are selected, i.e.:

```sql
SELECT ⟨many columns⟩
FROM tbl
ORDER BY ⟨a few columns⟩;
```

If only columns are selected that also occur in the `ORDER BY` clause, the `payload` field is not needed, as DuckDB can [decode the normalized keys](https://github.com/duckdb/duckdb/pull/12520).

### Non-Contiguous Iteration

Prior to v1.4.0, DuckDB used fixed-size sort keys, but their size was only known when executing the query.
This necessitates comparing and moving sort keys dynamically while sorting, which is much less efficient than statically compiled code.
The C++ `struct` that DuckDB uses now, shown above, is known at compile time, which allows it to be sorted with sorting algorithms that implement the C++ [`std::iterator`](http://en.cppreference.com/w/cpp/iterator/iterator.html) interface.
This means that DuckDB no longer needs to implement a sorting algorithm: it can grab an off-the-shelf C++ implementation!

C++ comes with `std::iterator` implementations for various data structures such as `std::array` and `std::vector`.
These data structures, however, require storing all data in a contiguous block of memory.
DuckDB uses a default page allocation (= contiguous block of memory) size of 256 KiB.
The `FixedSortKeyPayload` shown above is 24 bytes, so only ~10k tuples fit in a page.
We want sorted runs to be much longer than that (for performance reasons that we will not get into in this blog post).
To be able to generate longer sorted runs, we implemented an `std::iterator` that can iterate over non-contiguous blocks of memory:

<p align="center">
    <img src="/images/blog/sorting_again/block_iterator.svg"
        alt="DuckDB's block iterator"
        width="800"
    />
</p>

While this iterator is great at sequential access, some sorting algorithms require random access.
With this design, we cannot simply add an offset to a pointer to get the address of a tuple.
Instead, we compute the page index and offset within the page using integer division/modulo, as the number of tuples per page is always the same (except for the last page).
However, integer division/modulo is not cheap compared to the simple pointer arithmetic that can be used for contiguous blocks of memory, so we use [`fastmod`](https://github.com/lemire/fastmod) to reduce the cost.

### Sorting Algorithm

With the components described so far, we are able to generate large sorted runs, that can be spilled to storage page-by-page, rather than in an all-or-nothing fashion.
We use a combination of three sorting algorithms to achieve good sorting performance and high adaptivity to pre-sorted data:

1. [Vergesort](https://github.com/Morwenn/vergesort)
2. [Ska Sort](https://github.com/skarupke/ska_sort)
3. [Pattern-defeating quicksort](https://github.com/orlp/pdqsort)

Vergesort detects and merges runs of _(almost) sorted_ data, which greatly reduces the effort it takes to process, _e.g._, time-series data, which is often stored in sorted order already.
If Vergesort cannot detect any patterns, it falls back to Ska Sort, which performs an adaptive Most Significant Digit (MSD) [radix sort](https://en.wikipedia.org/wiki/Radix_sort) on the first 64-bit integer of the sort key.
If radix partitions in the recursion become too small, or if the data is not fully sorted after the first 64-bit integer, it falls back to Pattern-defeating [quicksort](https://en.wikipedia.org/wiki/Quicksort).

## Merging

Prior to v1.4.0, DuckDB would materialize the fully-merged data.
However, with a _k_-way merge, it is possible to output chunks of sorted data directly from the sorted runs, in somewhat of a streaming fashion.
This means that data can be output before the full merge has been computed.
We visualize this for four sorted runs:

<p align="center">
    <img src="/images/blog/sorting_again/k_way_merge.svg"
        alt="Streaming k-way merge"
        width="500"
    />
</p>

Chunk 1 can be output to the next pipeline before all sorted runs have been merged.
One of the reasons that this is useful is large `ORDER BY ... LIMIT ...` queries.
If the `LIMIT` is small, DuckDB uses a min-heap, which is much faster than sorting the entire input.
However, for large `LIMIT`s, the min-heap approach becomes worse than fully sorting and then applying the `LIMIT`.
With a _k_-way merge, the merge can be stopped by a `LIMIT` at any point, meaning that the cost of fully merging the sorted runs is never incurred.

Traditionally, the _k_-way merge is evaluated sequentially using a [tournament tree](https://en.wikipedia.org/wiki/K-way_merge_algorithm).
However, with modern multi-core CPUs, this leaves a lot of performance on the table.
The question is, how can we do this in parallel?

### _K_-Way Merge Path

Various algorithms to parallelize merge sort exist, such as [Merge Path](https://arxiv.org/pdf/1406.2628), which DuckDB's sort used prior to v1.4.0, and [Bitonic Merge Sort](https://en.wikipedia.org/wiki/Bitonic_sorter).
However, these algorithms parallelize a _cascading two-way merge sort_, not a _k_-way merge sort.
So, while these algorithms are parallel and skew-resistant, they are unattractive for larger-than-memory sorting, as they produce much more I/O.

For _k_-way merging, fewer options for parallelization exist.
The work can be divided using [value-based splitting](https://pages.cs.wisc.edu/~dewitt/includes/paralleldb/parsort.pdf).
However, it is easy to see that parallelism breaks down when the input distribution is extremely skewed, e.g., when half of the input has the same value, as there is no splitting value that can divide the work into evenly-sized tasks.
After searching the web, the only skew-resistant parallel _k_-way merge that we could find is a [bachelor thesis from 2014](https://ae.iti.kit.edu/download/Bachelor-Thesis_Andreas_Eberle.pdf).
We wanted a very fine-grained approach, so instead, we _generalized Merge Path to k sorted runs_.

In the previous figure, there is a horizontal line in each sorted run that indicates how much of each sorted run went into the output chunk.
The general idea of Merge Path, as explained in [our blog post on sorting four years ago]({% post_url 2021-08-27-external-sorting %}), is to compute _where these lines are_, i.e., where the sorted runs intersect.
Merge Path does this efficiently for merging two sorted runs using _binary search_.

We generalize this approach to _k_ sorted runs, which allows us to choose an arbitrary output chunk size, and compute where the sorted runs intersect such that when they are merged, the resulting chunk will be of the chosen size.
This allows for very fine-grained skew-resistant parallelism, which is not possible when choosing specific _splitting values,_ as the size of the chunks that this produces depends on the data distribution.
This is the pseudo-code for _k_-way merge path:

```python
def compute_intersections(sorted_runs, chunk_size):
    intersections = [0 for _ in range(len(sorted_runs))]
    while chunk_size != 0:
        delta = ceil(chunk_size / len(sorted_runs))
        min_idx = 0
        min_val = sorted_runs[0][intersections[0] + delta]
        for run_idx in range(1, len(sorted_runs)):
            val = sorted_runs[run_idx][intersections[run_idx] + delta]
            if val < min_val:
                min_idx = run_idx
                min_val = val
        intersections[min_idx] += delta
        chunk_size -= delta
    return intersections
```

This has been greatly simplified, as this does not take into account any edge cases or going out-of-bounds on the sorted runs.
The general idea is that we move up the lower bound for the intersection of one sorted run in each iteration of the `while` loop.
This has a worse complexity than the binary search used in the original Merge Path, but it is also has to be called fewer times because a _k_-way merge can merge all sorted runs in a single pass, rather than in many passes.
Profiling shows that this computation takes up just 1-2% of the overall execution time.

Threads can compute the intersections independently, and, therefore, in parallel.
Once threads have computed the intersections, they are free to merge the data between the intersections, as the data is guaranteed not to overlap with that of other threads.
The merged chunks can immediately be output in parallel due to DuckDB's [_order-preserving parallelism_](https://github.com/duckdb/duckdb/pull/3700).

<a name="benchmark"></a>

## Benchmark

So, how does the new sorting implementation perform compared to the old one?
We run a few experiments on my laptop (M1 Max MacBook Pro with 10 threads and 64 GB of memory).

### Raw Performance

We first benchmark raw integer sorting performance.
We have three types of inputs (pre-sorted ascending, pre-sorted descending, and randomly ordered), at three different sizes (10, 100, and 1000 million rows).
We've generated the data using the following queries:

```sql
CREATE TABLE ascending10m AS
    SELECT range AS i FROM range(10_000_000);

CREATE TABLE descending10m AS
    SELECT range AS i FROM range(9_999_999, 0, -1);

CREATE TABLE random10m AS
    SELECT range AS i FROM range(10_000_000) ORDER BY random();

-- and so on for 100m and 1000m
```

We took the median of 5 runs of each of these queries, for each table size:

```sql
SELECT any_value(i)
FROM (FROM ascending10m ORDER BY i);

SELECT any_value(i)
FROM (FROM descending10m ORDER BY i);

SELECT any_value(i)
FROM (FROM random10m ORDER BY i);

-- etc. for 100m and 1000m
```

This query causes DuckDB to evaluate the entire sort, without materializing the whole table as a query result.
This allows us to better isolate the performance of the sorting implementation.

#### Results

| Table      | Rows [Millions] | Old [s] |   New [s] | Speedup vs. Old [x] |
| :--------- | --------------: | ------: | --------: | ------------------: |
| Ascending  |              10 |   0.110 | **0.033** |               3.333 |
| Ascending  |             100 |   0.912 | **0.181** |               5.038 |
| Ascending  |            1000 |  15.302 | **1.475** |              10.374 |
| Descending |              10 |   0.121 | **0.034** |               3.558 |
| Descending |             100 |   0.908 | **0.207** |               4.386 |
| Descending |            1000 |  15.789 | **1.712** |               9.222 |
| Random     |              10 |   0.120 | **0.094** |               1.276 |
| Random     |             100 |   1.028 | **0.587** |               1.751 |
| Random     |            1000 |  17.554 | **6.493** |               2.703 |

This shows that the new implementation is highly adaptive to pre-sorted data: it is roughly 10x faster at ascending/descending data than the old implementation.
It has much better raw sorting performance: it is more than 2× faster at sorting randomly ordered data (at 1000 million).

We also plot the results on a __log-log scale__:

<p align="center">
    <img src="/images/blog/sorting_again/integers.svg"
        alt="Integer sorting benchmark"
        height=300
    />
</p>

Here, we can see that the new implementation scales much better: the execution time of the new implementation increases less steeply with input size than the old implementation.

### Wide Table

The first benchmark evaluated raw sorting performance.
In this next benchmark, we sort a _wide table_, i.e., we select many columns to be sorted by the `ORDER BY` clause.
We sort the `lineitem` table from TPC-H which has 15 columns, by the `l_shipdate` column, at scale factors 1 (~6 million rows), 10 (~60 million rows) and 100 (~600 million rows), generated using [DuckDB's TPC-H extension]({% link docs/stable/core_extensions/tpch.md %}).


We took the median execution time of 5 runs of this query for each scale factor:

```sql
SELECT any_value(COLUMNS(*))
FROM (FROM lineitem ORDER BY l_shipdate);
```

#### Results

| Table                                   |   SF | Old [s] |    New [s] | Speedup vs. Old [x] |
| :-------------------------------------- | ---: | ------: | ---------: | ------------------: |
| TPC-H SF 1 `lineitem` by `l_shipdate`   |    1 |   0.328 |  **0.189** |               1.735 |
| TPC-H SF 10 `lineitem` by `l_shipdate`  |   10 |   3.353 |  **1.520** |               2.205 |
| TPC-H SF 100 `lineitem` by `l_shipdate` |  100 | 273.982 | **80.919** |               3.385 |

We have set the memory limit to 30 GB, so the data no longer fits in memory at scale factor 100.
The new implementation is roughly 2× faster at scale factors 1 and 10, and more than 3× faster at scale factor 100.
This shows that the new _k_-way merge sort reduces data movement and I/O, is much more efficient at sorting wide tables than the old cascaded 2-way merge sort.

Again, we plot the results on a __log-log scale__:

<p align="center">
    <img src="/images/blog/sorting_again/lineitem.svg"
        alt="Lineitem sorting benchmark"
        height=300
    />
</p>

And we can see that the new implementation scales much better, especially when the data no longer fits in main memory.

### Thread Scaling

Finally, we benchmark how well the sorting implementation scales with threads.
We sort the table with 100 million randomly ordered integers from before, with 1, 2, 4, and 8 threads.
We use the same data and query as in the first benchmark, and take the median of five runs.

#### Results

| Threads |   Old [s] |   New [s] | Old Speedup vs. 1 Thread [x] | New Speedup vs. 1 Thread [x] |
| ------: | --------: | --------: | ---------------------------: | ---------------------------: |
|       1 | **3.240** |     4.234 |                    **1.000** |                    **1.000** |
|       2 | **2.121** |     2.193 |                        1.527 |                    **1.930** |
|       4 |     1.401 | **1.216** |                        2.312 |                    **3.481** |
|       8 |     0.920 | **0.654** |                        3.521 |                    **6.474** |

As we can see, the new, single-threaded sorting performance is around 30% slower than the old one.
This is due to the new sorting implementation using an _in-place MSD radix sort_, rather than an _out-of-place Least Significant Digit (LSD) radix sort_.
This makes the old implementation perform better specifically on this workload, at the cost of using much more memory.

However, if we increase the number of threads to 2, this advantage is already gone.
At 8 threads, the old implementation has a speedup of only ~3.5× over 1 thread, while this speedup is ~6.5× for the new implementation.

Again, we plot the results on a __log-log scale__:

<p align="center">
    <img src="/images/blog/sorting_again/threads.svg"
        alt="Thread scaling benchmark"
        height=300
    />
</p>

This shows that the new implementation's parallel scaling is much better than the old implementation.

## Conclusion

DuckDB's new sorting implementation has greatly improved performance over the old sorting implementation.
It is highly adaptive to pre-sorted data, performs less I/O when sorting data that does not fit in main memory, and scales much better with additional threads.

If you've upgraded to v1.4.0, you can enjoy the improved performance when using the `ORDER BY` clause.
The new sorting implementation has already been integrated into the window operator, so we expect to see a performance improvements when using the `OVER` clause as well.
For v1.5.0, we aim to integrate the new sorting implementation into the joins that use sorting such as the `ASOF` join.

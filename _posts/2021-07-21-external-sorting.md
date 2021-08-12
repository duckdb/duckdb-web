---

layout: post  
title:  "Efficient External Sorting"
author: Laurens Kuiper  
excerpt_separator: <!--more-->

---

_TLDR: DuckDB, a free and open-source analytical data management system, has a new sorting implementation that can efficiently sort more data than fits in main memory._

Database systems use sorting for many purposes, the most obvious purpose being when a user adds an `ORDER BY` clause to their query.
Sorting is also used within a few operators, such as window functions.
DuckDB recently improved its sorting implementation, which is now able to sort data in parallel, and sort more data than fits in memory.
In this blog, we'll take a look at how DuckDB sorts, and how this compares to other data management systems.

<!--more-->

#### Sorting Relational Data
Sorting is one of the most well-studied problems in computer science.
Sorting is also very important in data management systems.
Regrettably, research into sorting algorithms does not cover how to implement sorting in a database system.
There is a lot more to sorting relational data than just sorting a large array!

Consider the following example query on a snippet of a TPC-DS table:
```sql
SELECT c_customer_sk, c_birth_country, c_birth_year
FROM customer
ORDER BY birth_country DESC,
         birth_year    ASC NULLS LAST;
```
Which yields:

| c_customer_sk | c_birth_country | c_birth_year |
|---------------|-----------------|--------------|
| 64760         | NETHERLANDS     | 1991         |
| 75011         | NETHERLANDS     | 1992         |
| 89949         | NETHERLANDS     | 1992         |
| 90766         | NETHERLANDS     | NULL         |
| 42927         | GERMANY         | 1924         |

In other words: `c_birth_country` is ordered descendingly, and where `c_birth_country` is equal, we sort on `c_birth_year` ascendingly.
Null values are treated as the lowest value in the `c_birth_year` column.
Besides the sorting key columns, payload column `c_customer_sk` is shuffled accordingly.

It easy to implement something that can evaluate the example query.
However, implementing something efficient is far more difficult.
There are many decisions to be made that impact efficiency.
Looking at the literature before starting never hurts!

#### Database Sorting Techniques
In 2006 Goetz Graefe wrote a survey on [implementing sorting in database systems](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=F975C21F899ED842450004647077C121?doi=10.1.1.83.1080&rep=rep1&type=pdf).
In this survey he collected many sorting techniques that are publicly known, but hard to come by.
This is a great guideline if you are about to start implementing in your system.

Since then hardware has changed and database systems have evolved, especially analytical ones.
DuckDB for instance uses columnar storage, operates in main memory, usually stores data on an SSD, and has a good parallelization framework.
These things were not commonplace back then.

Many of the techniques in the survey still hold up, but these developments affect how to you want to implement sorting.
However, one technique, in particular, is timeless and makes comparisons cheap.
We used this in our implementation, so let's check it out briefly!

#### Binary String Comparison
The cost of sorting will be dominated by comparing values and moving data around.
Comparing values is expensive if we have multiple `ORDER BY` clauses: Each clause has to be compared, and be checked for null values.
This becomes even more expensive if we have columnar storage, as we will have to jump between columns to compare values: This causes random access in memory, which is slow.

We can make this comparison cheaper by encoding the sorting columns.
This costs some time at the start, but makes the comparison very cheap, and therefore will pay off during sorting.
Let's take another look at 3 of the rows of the example:

| c_birth_country | c_birth_year |
|-----------------|--------------|
| NETHERLANDS     | 1991         |
| NETHERLANDS     | 1992         |
| GERMANY         | 1924         |

On a little-endian machine, the bytes that represent these values look like this in memory:
```sql
-- NETHERLANDS
01001110 01000101 01010100 01001000 01000101 01010010 01001100 01000001 01001110 01000100 01010011 00000000
-- GERMANY
01000111 01000101 01010010 01001101 01000001 01001110 01011001 00000000
-- 1991
11000111 00000111 00000000 00000000
-- 1992
11001000 00000111 00000000 00000000
-- 1924
10000100 00000111 00000000 00000000
```

The trick is to convert these to a binary string that encodes the sorting order:
```sql
-- NETHERLANDS | 1991
10110001 10111010 10101011 10110111 10111010 10101101 10110011 10111110 10110001 10111011 10101100 11111111
10000000 00000000 00000111 11000111
-- NETHERLANDS | 1992
10110001 10111010 10101011 10110111 10111010 10101101 10110011 10111110 10110001 10111011 10101100 11111111
10000000 00000000 00000111 11001000
-- GERMANY     | 1924
10111000 10111010 10101101 10110010 10111110 10110001 10100110 11111111 11111111 11111111 11111111 11111111
10000000 00000000 00000111 10000100
```

The binary string is fixed-size because this makes it much easier to move it around during sorting.

The string 'GERMANY' is shorter than 'NETHERLANDS', therefore it is padded with `00000000`'s.
All bits in column `c_birth_country` are inverted because this column is sorted descendingly.
If a string is too long we encode its prefix, and only look at the whole string if the prefixes are equal.

The bytes in `c_birth_year` are swapped because we need the big-endian representation to encode the sorting order.
The first bit is also flipped, to preserve order between positive and negative integers.
If there are NULL values, these must be encoded using an additional byte (not shown in the example).

With this binary string we can compare both columns at the same time by comparing the binary string representation.
This can be done with a single `memcmp` in __C++__!

#### Two Phase Sorting
DuckDB uses [Morsel-Driven Parallelism](https://15721.courses.cs.cmu.edu/spring2016/papers/p743-leis.pdf), a framework for parallel query execution.
For the sorting operator, this means that multiple threads collect data in parallel before the data is combined into a result.

We use this parallelism by letting each thread sort the data it collects with [Radix sort](https://en.wikipedia.org/wiki/Radix_sort).
Radix sort is a distribution-based sorting algorithm, which sorts data in _O(k * n)_, where _k_ is the length of the sorting key, which is the binary string in our case.

After the first sorting phase, each thread has one or more sorted blocks of data, which must be combined.
[Merge sort](https://en.wikipedia.org/wiki/Merge_sort) is the algorithm of choice for this task.
We merge two blocks of sorted data at a time until only one sorted block remains.

Now it becomes more difficult to use all available threads.
If we have many more sorted blocks than we have threads, we can assign each thread to merge two blocks.
However, as the blocks get merged, we will not have enough blocks to keep all threads busy.
To fully parallelize this phase, we've implemented [Merge Path](https://arxiv.org/pdf/1406.2628.pdf) by Oded Green Green et al.
Merge Path pre-computes where the sorted lists will intersect while merging, shown in the image below (all credits go to the authors).

<img src="/images/blog/sorting/merge_path.png" alt="Merge Path - A Visually Intuitive Approach to Parallel Merging" title="Merge Path by Oded Green, Saher Odeh, Yitzhak Birk" style="max-width:70%"/>

If we know where the intersections are, we can merge parts of the sorted data independently in parallel.
This allows us to use all available threads effectively.

Another technique we've used to speed up merge sort is _predication_.
With this technique we turn code with _if/else_ branches into code without branches.
Modern CPU's try to predict whether the _if_, or the _else_ branch will be predicted.
If this is hard to predict, it can slow down the code.
Take a look at the example of pseudo-code with branches below.

```c++
// continue until merged
while (l_ptr && r_ptr) {
  // check which side is smaller
  if (memcmp(l_ptr, r_ptr, entry) < 0) {
    // copy from left side and advance
    memcpy(result_ptr, l_ptr, entry);
    l_ptr += entry;
  } else {
    // copy from right side and advance
    memcpy(result_ptr, r_ptr, entry);
    r_ptr += entry;
  }
  // advance result
  result_ptr += entry;
}
```

We're merging the data from the left and right blocks into a result block, one entry at a time, by advancing pointers.
This code can be made branchless by using the comparison boolean as a 0 or 1, shown in the pseudo-code below.

```c++
// continue until merged
while (l_ptr && r_ptr) {
  // store comparison result in a bool
  bool left_less = memcmp(l_ptr, r_ptr, entry) < 0;
  bool right_less = 1 - left_less;
  // copy from either side
  memcpy(result_ptr, l_ptr, left_less * entry);
  memcpy(result_ptr, r_ptr, right_less * entry);
  // advance either one
  l_ptr += left_less * entry;
  l_ptr += right_less * entry;
  // advance result
  result_ptr += entry;
}
```

When `left_less` is true, it is equal to 1.
This means `right_less` is false, and therefore equal to 0.
We use this to copy `entry` bytes from the left side, and 0 bytes from the right side, and incrementing the left and right pointers accordingly.

With predicated code, the CPU does not have to predict which instructions to execute, which means there will be less instruction cache misses!

#### Columns or Rows?
Now let's take a look at how we're moving data around.
DuckDB has a vectorized execution engine.
Data is stored in a columnar layout, which is processed in batches at a time
This layout is great for analytical query processing.
However, for sorting rows are shuffled around, not columns!

Of course we can stick to the columnar layout while sorting: Sort the key columns, then re-order the payload columns one by one.
However, re-ordering will cause a random access pattern in memory for each column.
If there are many payload columns, this can be expensive.
Converting the columns to rows will make the memory access pattern better, but this is not free either because the data needs to be copied, and the rows have to be converted back to columns again after sorting.

Our goal is to support external sorting, i.e. to be able to sort more data than fits in memory.
In order to support this, we have to store data in buffer-managed blocks that can be offloaded to disk.
Because we have to copy the data to these blocks anyway, it becomes very attractive to use a row layout rather than a column layout.

There are a few operators that are inherently row-based, such as joins and aggregations.
DuckDB has an internal row layout for these operators, and we decided to use it for the sorting operator as well.
This layout has only been used in-memory so far.
In the next section, we'll explain how we got it to work externally as well.

#### External Sorting
The buffer manager can offload our sorted blocks from memory to disk.
Accessing disk is much slower than accessing memory, therefore it is crucial that each block is written to, and read from disk only once.
Using an SSD over a HDD also speeds things up a lot.

Offloading data to disk is easy for fixed-size columns like integers, but more difficult for variable-sized columns like strings.
Our row layout uses fixed-size rows, which cannot fit strings with arbitrary sizes.
Therefore, strings are represented by a pointer, which points into a heap.

We've changed our heap to also store strings row-by-row in buffer-managed blocks:

<img src="/images/blog/sorting/heap.svg" alt="Each fixed-size row has its own variable-sized row in the heap" title="DuckDB's row layout heap"/>

Each row has an additional 8-byte field `pointer` which points to the start of this row in the heap.
This is useless in the in-memory representation, but we'll see why it is useful for the on-disk representation in just a second.

If the data fits in memory, the heap blocks stay pinned, and only the fixed-size rows are re-ordered while sorting.
If the data does not fit in memory, the blocks need to be offloaded to disk, and the heap will also be re-ordered while sorting.
When a heap block is offloaded to disk, the pointers pointing into it are invalidated.
When we load the block back into memory, the pointers will have changed.

This is where our row-wise layout comes into play.
The 8-byte `pointer` field is overwritten with an 8-byte `offset` field, denoting where in the heap block this row's strings can be found.
This technique is called ['pointer swizzling'](https://en.wikipedia.org/wiki/Pointer_swizzling).
When we swizzle the pointers, the row layout and heap block look like this:

<img src="/images/blog/sorting/heap_swizzled.svg" alt="Pointers are 'swizzled': replaced by offsets" title="DuckDB's 'swizzled' row layout heap"/>

The pointers to the string values are also overwritten with an 8-byte relative offset, denoting how far this string is offset from the start of the row in the heap (hence every `stringA` has an offset of `0`: It is the first string in the row).
Using relative offsets within rows rather than absolute offsets is very useful during merge sort, as these relative offsets stay constant, and do not need to be updated when a row is copied.

When the blocks need to be scanned to read the sorted result, we 'unswizzle' the pointers, making them point to the string again.

With this dual row-wise representation, we can easily copy around both the fixed-size rows, and the variable-sized rows in the heap.
Besides having the buffer manager load/unload blocks, the only difference between in-memory and external sorting is that we swizzle/unswizzle pointers to the heap blocks, and copy data from the heap blocks during merge sort.

We plan to add external capabilities on all our row-based operators by means of this row layout!

#### Comparison with Other Implementations
Now that we've covered most of the techniques that are used in our sorting implementation, we want to know how we compare to the rest.
We'll compare it with a few other systems: [ClickHouse, version 21.7.5](https://clickhouse.tech), [HyPer, version 2019.2.6416](https://hyper-db.de), and [PostgreSQL, version 13.3](https://www.postgresql.org).

Benchmarking sorting in a database system is not straightforward.
Ideally, we'd like to measure only the time it takes to sort the data, not the time it takes to read the input data and show the output.
Not every system has a profiler to measure the time of the sorting operator exactly, so this is not an option if we want to have a fair comparison.

To approach a fair comparison, we will measure the end-to-end time of queries that sort the data and write the result to a temporary table, i.e.:
```sql
CREATE TEMPORARY TABLE ... AS
SELECT ...
FROM ...
ORDER BY ...;
```
There is no perfect solution to this problem, but this should give us a good comparison because the end-to-end time of this query should be dominated by sorting.

To measure stable end-to-end query time, each query is run 5 times, and only the median time is reported.
Because the other systems are disk-based, DuckDB is restarted for every query, to force it to read the data from disk as well.
However, DuckDB will keep the created table in memory if possible.

The experiments were run on a machine with an Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz, 128GB of RAM, and a 1TB Samsung SM961 SSD.
For these first experiments, the data fits fully in memory (128GB).

#### Random Integers
We'll start with a simple example.
I've generated the first 100 million integers and shuffled them.

For our first experiment see how well the systems scale with more threads.
The machine that was used for the experiments has 8 cores, and up to 16 virtual threads.

<img src="/images/blog/sorting/randints_threads.svg" alt="Sorting 100M random integers" title="Threads Experiment" style="max-width:80%"/>

__TODO:__ analyze plot. Mention that the cascaded merge sort doesn't do that well with an uneven amount of threads, and that it is expected to not see performance increase after 8 threads

For our next experiment, we'll look at how the systems scale with the number of rows.
From the initial table with integers I've made 9 more tables, with 10M, 20M, ..., 90M integers each.

<img src="/images/blog/sorting/randints_scaling.svg" alt="Sorting 10-100M random integers" title="Random Integers Experiment" style="max-width:80%"/>

__TODO:__ analyze plot
As we can see, the performance of the different systems is in the same ballpark, with DuckDB edging out slightly over the rest.

The sortedness of the table may impact the performance.
Some systems keep track of the sortedness of a table, and may decide to skip sorting altogether.
This is important for systems that use quicksort, because quicksort performs much worse on inversely sorted data than on random data.

<img src="/images/blog/sorting/randints_sortedness.svg" alt="Sorting 100M integers with different sortedness" title="Sortedness Experiment" style="max-width:80%"/>

All systems perform better on sorted data.
DuckDB has smaller difference than between sorted and unsorted data than the other systems, because DuckDB does not keep track of sortedness.
DuckDB's improved performance on sorted data is due to a better memory access pattern during Radix sort: When the data is already sorted data access is mostly sequential.

Another interesting result is that DuckDB sorts data faster than some of the other systems can read already sorted data.
This difference is partially an artifact of how the sorting performance is being measured: We measure end-to-end sorted table creation time, rather than measuring just sorting.
Nonetheless, the runtime should be dominated by sorting, therefore this is a reasonable indication of performance.

#### TPC-DS
For the next comparison, I've improvised a relational sorting benchmark on two tables from the TPC-DS benchmark.
TPC-DS is challenging for sorting implementations because it has wide tables (with many columns), and a mix of fixed- and variable-sized types.
The number of rows increases with the scale factor.
The tables we've chosen are `catalog_sales` and `customer`.

`catalog_sales` has 34 columns, all fixed-size types (integer and double), and grows to have many rows as the scale factor increases.
`customer` has 18 columns, integers and strings, and a decent amount of rows as the scale factor increases.
The row counts of both tables at each scale factor are shown in the table below.

| SF  | customer  | catalog_sales |
|-----|-----------|---------------|
| 1   | 100.000   | 1.441.548     |
| 10  | 500.000   | 14.401.261    |
| 100 | 2.000.000 | 141.430.723   |
| 300 | 5.000.000 | 260.014.080   |
 
#### Catalog Sales
Our first experiment on the `catalog_sales` table is selecting 1 column, then 2 columns, ... up to all 34, always ordering by `cs_quantity` and `cs_item_sk`.
This experiment will tell us how well the different systems can re-order payload columns.

<img src="/images/blog/sorting/tpcds_catalog_sales_payload.svg" alt="Increasing the number of payload columns for the catalog_sales table" title="Catalog Sales Payload Experiment" style="max-width:100%"/>

__TODO:__ analyze plot
What immediately stands out is that ClickHouse has the same performance regardless of the number of columns selected.
I dug into their source code on GitHub, and found that ClickHouse represents columns as large arrays, and uses [Radix Sort or Pattern Defeating Quicksort for integers](https://github.com/ClickHouse/ClickHouse/blob/9aa4a9782e66bef029ead805cca772616e4415c1/src/Columns/ColumnVector.cpp#L134), [`std::sort` for strings](https://github.com/ClickHouse/ClickHouse/blob/9aa4a9782e66bef029ead805cca772616e4415c1/src/Columns/ColumnString.cpp#L317), and [`std::partial_sort` for decimals](https://github.com/ClickHouse/ClickHouse/blob/9aa4a9782e66bef029ead805cca772616e4415c1/src/Columns/ColumnDecimal.cpp#L131).
After sorting the key columns, [each payload column is re-ordered](https://github.com/ClickHouse/ClickHouse/blob/9f5cd35a6963cc556a51218b46b0754dcac7306a/src/Interpreters/sortBlock.cpp#L217), which [copies the data](https://github.com/ClickHouse/ClickHouse/blob/master/src/Columns/ColumnVector.cpp#L451).
Both sorting and re-ordering is done in a single thread, despite explicitly calling `set max_threads=8;`.
HOW?

The other systems take more time as more payload columns are added, as expected: More data needs to be moved around.
DuckDB shows similar performance and scaling to HyPer, but is slightly faster.

Our second experiment is selecting all columns, ordering by 1 column, then 2 columns, ... up to all 34 (34 order clauses!).
This is not a realistic scenario, but this experiment will tell us something about how well the different systems handle multiple `ORDER BY` clauses.

<img src="/images/blog/sorting/tpcds_catalog_sales_sorting.svg" alt="Increasing the number of order clauses for the catalog_sales table" title="Catalog Sales Order Clauses Experiment" style="max-width:100%"/>

__TODO:__ analyze plot
ClickHouse has a jump in runtime when going from 1 to 2 order by clauses, because they do not encode the key columns as a binary string.
This means that their comparator works along the lines of: If the first key column is equal, compare the second one too.
This comparator has a branch prediction, and random access into the second column, which slows down the comparison.
Such comparators can be found in their source code [here](https://github.com/ClickHouse/ClickHouse/blob/master/src/Core/SortCursor.h#L370).
This effect diminishes as we add more key columns, because it is uncommon to have rows that have more than 2 or 3 equal columns.

DuckDB's performance goes down gradually as more clauses are added.
This is mainly because the key columns that are encoded in the binary string format are not decoded, but rather duplicated as a payload column.
This means that there is full data duplication if there are 34 order clauses.
Decoding the binary string format is possible, but this has not yet been implemented.
Still, with fewer `ORDER BY` clauses, DuckDB is ahead of the pack.

#### Customer
Not sure if I want to include these because they are not that interesting.
Instead, we can sort catalog_sales externally.

<img src="/images/blog/sorting/tpcds_customer_int.svg" alt="Increasing the number of integer string order clauses for the customer table" title="Customer Integer Order Clauses Experiment" style="max-width:100%"/>

<img src="/images/blog/sorting/tpcds_customer_string.svg" alt="Increasing the number of integer order clauses for the customer table" title="Customer String Order Clauses Experiment" style="max-width:100%"/>
---

layout: post  
title:  "Efficient External Sorting"
author: Laurens Kuiper  
excerpt_separator: <!--more-->

---

_TLDR: DuckDB, a free and open-source analytical data management system, has a new sorting implementation that can efficiently sort more data than fits in main memory._

Database systems use sorting for many purposes, the most obvious purpose being when a user adds an `ORDER BY` clause to their query.
Sorting is also used within operators, such as window functions.
DuckDB recently improved its sorting implementation, which is now able to sort data in parallel, and sort more data than fits in memory.
In this blog, we'll take a look at how DuckDB sorts, and how this compares to other data management systems.

<!--more-->

#### Sorting Relational Data
Sorting is one of the most well-studied problems in computer science, and it is an important aspect of data management.
Research into sorting algorithms tends to focus on sorting large arrays or key/value pairs.
While important, this does not cover how to implement sorting in a database system.
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
By specifying `NULLS LAST`, null values are treated as the lowest value in the `c_birth_year` column.
Whole rows are ordered, not just the columns in the order clause.
Therefore, payload column `c_customer_sk` has to be shuffled along too.

It easy to implement something that can evaluate the example query using any sorting implementation, for instance __C++__'s `std::sort`.
While `std::sort` is great, it is a single threaded approach that uses a simple API.
To achieve better performance, a hand-crafted sorting implementation is needed.
There are many optimization opportunities to make sorting faster.
We are not the first to implement relational sorting, so we dove into the literature to look for guidance.

#### Database Sorting Techniques
In 2006 Goetz Graefe wrote a survey on [implementing sorting in database systems](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=F975C21F899ED842450004647077C121?doi=10.1.1.83.1080&rep=rep1&type=pdf).
In this survey he collected many sorting techniques that are publicly known, but hard to come by.
This is a great guideline if you are about to start implementing in your system.

Since then hardware has changed and database systems have evolved, especially analytical ones.
DuckDB for instance uses columnar storage, operates in main memory, usually stores data on an SSD, and has a good parallelization framework.
These things were not commonplace back then.

While some of the techniques in the survey are affected by these developments, many still hold up.
One technique in particular, which makes comparisons cheap, is timeless.
We've implemented this in DuckDB, so let's see how it works!

#### Binary String Comparison
The cost of sorting is dominated by comparing values and moving data around.
Anything that makes these two operations cheaper will have a big impact on the total runtime.

There are two obvious ways to go about implementing a comparator when we have multiple `ORDER BY` clauses.
The first way is to loop through them: Compare columns until we find one that is not equal, or until we've compared all columns.
This is fairly complex already, as this requires a loop with an if/else inside of it.
If we have columnar storage, this comparator has to jump between columns, causing random access in memory.

The second way is to entirely sort the by the first clause, then sort by the second clause, but only where the first clause was equal, and so on.
This approach is especially inefficient when there are many duplicate values, as it requires multiple passes over the data.

The comparator can be simplified to a single binary string comparison, by encoding the sorting column.
Encoding the data is not free, but since we are using the comparator so much during sorting, it will pay off.
Let's take another look at 3 of the rows of the example:

| c_birth_country | c_birth_year |
|-----------------|--------------|
| NETHERLANDS     | 1991         |
| NETHERLANDS     | 1992         |
| GERMANY         | 1924         |

On a little-endian machine, the bytes that represent these values look like this in memory:
```sql
c_birth_country
-- NETHERLANDS
01001110 01000101 01010100 01001000 01000101 01010010 01001100 01000001 01001110 01000100 01010011 00000000
-- GERMANY
01000111 01000101 01010010 01001101 01000001 01001110 01011001 00000000

c_birth_year
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
For the sorting operator, this entails that multiple threads collect roughly an equal amount of data, in parallel, from the query pipeline under it.

We use this parallelism by letting each thread sort the data it collects with [Radix sort](https://en.wikipedia.org/wiki/Radix_sort).
Radix sort is a distribution-based sorting algorithm, which sorts data in _O(k * n)_, where _k_ is the length of the sorting key, which is the binary string in our case.

After this first sorting phase, each thread has one or more sorted blocks of data, which must be combined.
[Merge sort](https://en.wikipedia.org/wiki/Merge_sort) is the algorithm of choice for this task.
We perform a cascaded merge sort: Merge two blocks of sorted data at a time until only one sorted block remains.

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
This code can be made _branchless_ by using the comparison boolean as a 0 or 1, shown in the pseudo-code below.

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
Besides comparisons, the other big cost of sorting is moving data around.
DuckDB has a vectorized execution engine.
Data is stored in a columnar layout, which is processed in batches at a time
This layout is great for analytical query processing.
However, when relation data is sorted, rows are shuffled around, rather than columns.

We could stick to the columnar layout while sorting: Sort the key columns, then re-order the payload columns one by one.
However, re-ordering will cause a random access pattern in memory for each column.
If there are many payload columns, this can be expensive.
Converting the columns to rows will make the memory access pattern better, but this is not free either: Data needs to be copied, and rows have to be converted back to columns again after sorting.

Our goal is to support external sorting, i.e. to be able to sort more data than fits in memory.
In order to support this, we have to store data in buffer-managed blocks that can be offloaded to disk.
Because we have to copy the data to these blocks anyway, it becomes very attractive to use a row layout rather than a column layout.

There are a few operators that are inherently row-based, such as joins and aggregations.
DuckDB has an internal row layout for these operators, and we decided to use it for the sorting operator as well.
This layout has only been used in-memory so far.
In the next section, we'll explain how we got it to work externally as well.

#### External Sorting
The buffer manager can unload blocks from memory to disk.
This is not something we actively do in our sorting implementation, but rather something that the buffer manager decides to do if memory would fill up otherwise.
It uses a least-recently-used queue to decide which blocks to write.

When we need a block, we pin it, which reads it from disk if it is not loaded already.
Accessing disk is much slower than accessing memory, therefore it is crucial that we minimize the number of reads and writes.
Some important things to help minimize this are:
1. Destroying blocks as soon as you are done reading them. This frees up memory and prevents the buffer manager from unnecessarily writing it to disk.
2. Zig-zagging through the pairs of blocks to merge in the cascaded merge sort. This is illustrated in the image below. By zig-zagging through through these iterations, we start an iteration by merge the last blocks that were merged in the previous iteration. Those blocks are likely still in memory, saving us some read/write operations.

<img src="/images/blog/sorting/zigzag.svg" alt="Zig-zagging through the merge sort iterations to reduce read and write operations" title="Zig-zagging to reduce I/O"/>

Using a SSD over a HDD also speeds things up a lot.

Unloading data to disk is easy for fixed-size columns like integers, but more difficult for variable-sized columns like strings.
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
This technique is called [_'pointer swizzling'_](https://en.wikipedia.org/wiki/Pointer_swizzling).
When we swizzle the pointers, the row layout and heap block look like this:

<img src="/images/blog/sorting/heap_swizzled.svg" alt="Pointers are 'swizzled': replaced by offsets" title="DuckDB's 'swizzled' row layout heap"/>

The pointers to the string values are also overwritten with an 8-byte relative offset, denoting how far this string is offset from the start of the row in the heap (hence every `stringA` has an offset of `0`: It is the first string in the row).
Using relative offsets within rows rather than absolute offsets is very useful during merge sort, as these relative offsets stay constant, and do not need to be updated when a row is copied.

When the blocks need to be scanned to read the sorted result, we _'unswizzle'_ the pointers, making them point to the string again.

With this dual row-wise representation, we can easily copy around both the fixed-size rows, and the variable-sized rows in the heap.
Besides having the buffer manager load/unload blocks, the only difference between in-memory and external sorting is that we swizzle/unswizzle pointers to the heap blocks, and copy data from the heap blocks during merge sort.

We plan to add external capabilities on all our row-based operators by means of this row layout!

#### Comparison with Other Systems
Now that we've covered most of the techniques that are used in our sorting implementation, we want to know how we compare to other systems.
DuckDB is often used for interactive data analysis, and is therefore often compared to tools like pandas and [dplyr](https://dplyr.tidyverse.org).
In this setting, people are usually running on laptops or PCs, therefore we will run these experiments on a 2020 MacBook Pro.
This laptop has an ARM M1 CPU, and [one of the fastest SSD's found in a laptop](https://eclecticlight.co/2020/12/12/how-fast-is-the-ssd-inside-an-m1-mac/).

We'll be comparing against the following systems:
1. [pandas](https://pandas.pydata.org), version 1.3.2
2. [SQLite](https://www.sqlite.org/index.html), version 3.36.0
3. [ClickHouse](https://clickhouse.tech), version 21.7.5
5. [HyPer](https://hyper-db.de), version 2021.2.1.12564

ClickHouse was built for M1 using [this guide](https://clickhouse.tech/docs/en/development/build-osx/).
All but DuckDB and HyPer have a single-threaded sorting implementation, so naturally these will have an advantage over the other systems.
This list gives us a mix of different types of systems.
We have single-/multi-threaded, embedded/stand-alone, OLAP/OLTP, and in-memory/external sorting.

HyPer is [Tableau's data engine](https://www.tableau.com/products/new-features/hyper), originally created by the [database group at the University of Munich](http://db.in.tum.de).
It does not run natively (yet) on ARM-based processors like the M1.
We will use [Rosetta 2](https://en.wikipedia.org/wiki/Rosetta_(software)#Rosetta_2), MacOS's x86 emulator to run it.
Emulation causes some overhead, so we we will also include one experiment on a Linux machine for a more fair comparison with HyPer.

Benchmarking sorting in database systems is not straightforward.
Ideally, we'd like to measure only the time it takes to sort the data, not the time it takes to read the input data and show the output.
Not every system has a profiler to measure the time of the sorting operator exactly, so this is not an option.

To approach a fair comparison, we will measure the end-to-end time of queries that sort the data and write the result to a temporary table, i.e.:
```sql
CREATE TEMPORARY TABLE output AS
SELECT ...
FROM ...
ORDER BY ...;
```
There is no perfect solution to this problem, but this should give us a good comparison because the end-to-end time of this query should be dominated by sorting.
For pandas we will use `sort_values` with `inplace=False` to mimic this query.
In ClickHouse, temporary tables can only exists in memory, which is problematic for our out-of-core experiments.
Therefore we will use a regular `TABLE`, but we also need to choose a table engine.
Most of the table engines apply compression or create an index, which we do not want.
Therefore I've chosen the [File](https://clickhouse.tech/docs/en/engines/table-engines/special/file/#file)table engine, with format [Native](https://clickhouse.tech/docs/en/interfaces/formats/#native).

To measure stable end-to-end query time, each query is run 5 times, and report the median run time.
DuckDB is restarted for every query, to force it to read the input data from disk, like the other database systems.
We cannot force pandas to read/write to/from disk, so both the input and output dataframe will be in memory.
DuckDB will not write the output table to disk unless there is enough room to keep it in memory, and therefore also has a slight advantage.

#### Random Integers
We'll start with a simple example.
I've generated the first 100 million integers and shuffled them.

For our first experiment see how well the systems scale with more threads.
The M1 processor has 8 cores, 4 high-performance ones, and 4 energy-efficient ones.

<img src="/images/blog/sorting/randints_threads.svg" alt="Sorting 100M random integers" title="Threads Experiment" style="max-width:80%"/>

Going from 1 to 2 threads does not yield much improved performance for DuckDB, mainly because Radix Sort is so much faster than Merge Sort.
Nonetheless, DuckDB good scaling up to 4 threads, which is to be expected from the M1.
For the rest of the experiments, DuckDB will use 4 threads.

For our next experiment, we'll look at how the systems scale with the number of rows.
From the initial table with integers I've made 9 more tables, with 10M, 20M, ..., 90M integers each.

<img src="/images/blog/sorting/randints_scaling.svg" alt="Sorting 10-100M random integers" title="Random Integers Experiment" style="max-width:80%"/>

Being a traditional disk-based database system, SQLite always opts for an external sorting strategy, despite the data fitting in main-memory, therefore it is much slower.
The performance of other systems is in the same ballpark, with the clear winner being DuckDB.

For our next experiment we'll see how the sortedness of the input may impact performance.
Some systems keep track of the sortedness of a table, and may decide to skip sorting altogether.
This is especially important to do in systems that use quicksort, because quicksort performs much worse on inversely sorted data than on random data.

<img src="/images/blog/sorting/randints_sortedness.svg" alt="Sorting 100M integers with different sortedness" title="Sortedness Experiment" style="max-width:80%"/>

Not surprisingly, all systems perform better on sorted data, sometimes by a large margin, indicating some kind of optimization regarding sortedness.
DuckDB does not keep track of sortedness, but still has a very small difference than between sorted and unsorted data.
This is due to a better memory access pattern during sorting: When the data is already sorted the access pattern is mostly sequential.

Another interesting result is that DuckDB sorts data faster than some of the other systems can read already sorted data.
This difference is partially an artifact of how the sorting performance is being measured: We measure end-to-end sorted table creation time, rather than measuring just sorting.
Nonetheless, the runtime should be dominated by sorting, therefore this is a reasonable indication of performance.

#### TPC-DS
For the next comparison, I've improvised a relational sorting benchmark on two tables from the TPC-DS benchmark.
TPC-DS is challenging for sorting implementations because it has wide tables (with many columns), and a mix of fixed- and variable-sized types.
The number of rows increases with the scale factor.
The tables are `catalog_sales` and `customer`.

`catalog_sales` has 34 columns, all fixed-size types (integer and double), and grows to have many rows as the scale factor increases.
`customer` has 18 columns, 10 integers and 8 strings, and a decent amount of rows as the scale factor increases.
The row counts of both tables at each scale factor are shown in the table below.

| SF  | customer  | catalog_sales |
|-----|-----------|---------------|
| 1   | 100.000   | 1.441.548     |
| 10  | 500.000   | 14.401.261    |
| 100 | 2.000.000 | 143.997.065   |
| 300 | 5.000.000 | 260.014.080   |

The `customer` table fits in memory for every scale factor.
The `catalog_sales` table however, does not.
With 34 columns of numeric types, each 4 bytes wide, the `catalog_sales` table does not fit into memory at SF100 and SF300, having an approximate size of \~20 GB and \~35 GB, respectively.

The data was generated using DuckDB's TPC-DS extension, then exported to CSV in a random order to undo any ordering patterns that could have been in the generated data.
 
#### Catalog Sales
Our first experiment on the `catalog_sales` table is selecting 1 column, then 2 columns, ... up to all 34, always ordering by `cs_quantity` and `cs_item_sk`.
This experiment will tell us how well the different systems can re-order payload columns.
SF300 is not included as the runtime became too long, and I need my laptop to do other things!

<img src="/images/blog/sorting/tpcds_catalog_sales_payload.svg" alt="Increasing the number of payload columns for the catalog_sales table" title="Catalog Sales Payload Experiment" style="max-width:100%"/>

We see very similar trends at SF1 and SF10, which is always nice to see; unexpected jumps in performance are undesirable.
At SF100 things get more interesting: At around 10 payload columns or so, the data does not fit in memory, and  HyPer has a big drop in performance.
As far as I'm aware, HyPer uses [`mmap`](https://man7.org/linux/man-pages/man2/mmap.2.html), which creates a mapping between memory and and a file.
This allows the operating system to move data between memory and disk.
While useful, it is no substitute for a proper external sort, as it creates random access to disk, which is very slow.
Eventually, it errors out with the following message:
```
ERROR:  Cannot allocate 333982248 bytes of memory: The `global memory limit` limit of 12884901888 bytes was exceeded.
```

ClickHouse has very interesting scaling as the number of columns increases.
While they do have an [external sort implementation](https://clickhouse.tech/docs/en/sql-reference/statements/select/order-by/#implementation-details), it is actually not used here, even at SF100.
ClickHouse sticks to its columnar format while sorting, and each individual column does fit in memory.
I dug into their source code on GitHub, and found that ClickHouse uses [Radix Sort or Pattern Defeating Quicksort for integers](https://github.com/ClickHouse/ClickHouse/blob/9aa4a9782e66bef029ead805cca772616e4415c1/src/Columns/ColumnVector.cpp#L134), [`std::sort` for strings](https://github.com/ClickHouse/ClickHouse/blob/9aa4a9782e66bef029ead805cca772616e4415c1/src/Columns/ColumnString.cpp#L317), and [`std::partial_sort` for decimals](https://github.com/ClickHouse/ClickHouse/blob/9aa4a9782e66bef029ead805cca772616e4415c1/src/Columns/ColumnDecimal.cpp#L131).
After sorting the key columns, [each payload column is re-ordered](https://github.com/ClickHouse/ClickHouse/blob/9f5cd35a6963cc556a51218b46b0754dcac7306a/src/Interpreters/sortBlock.cpp#L217), which [copies the data](https://github.com/ClickHouse/ClickHouse/blob/master/src/Columns/ColumnVector.cpp#L451).
Both sorting and re-ordering is done in a single thread, despite explicitly calling `set max_threads=4;`.

__TODO:__ how does ClickHouse scale this well????

The other systems take more time as more payload columns are added, as expected: More data needs to be moved around.
Pandas performs surprisingly well on SF100, despite the data not fitting in memory.
This is because MacOS dynamically increases swap size.
Most operating systems do not do this, and would fail to load the data at all.
While loading the data, swap size grows to an impressive \~40 GB: Both the file and the read dataframe are fully in memory/swap at the same time, rather than streamed into memory.
This goes down to \~20 GB of memory/swap when the file is done being read.
After that, Pandas actually has an impressive performance despite relying on swap so heavily.
However, it eventually crashed with the following error:
```
UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
```

DuckDB performs well both in-memory and external, and there is no clear visible point at which data no longer fits in memory: Runtime is fast and reliable.

As promised, we'll also run an experiment on a Linux machine with plenty of memory to get a better comparison with HyPer.
This machine has an Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz, which has 8 cores (up to 16 vthreads), and 128 GB of RAM.

<img src="/images/blog/sorting/jewels_payload.svg" alt="Increasing the number of payload columns for the catalog_sales table (jewels)" title="Catalog Sales Payload Experiment (on bigger machine)" style="max-width:100%"/>

I've included ClickHouse and Pandas in this comparison as well.
What we can immediately see is that the ClickHouse and Pandas perform worse, because they use single-threaded implementations, and this CPU has a lower single-thread performance.
Again, pandas crashes with an error:
```
numpy.core._exceptions.MemoryError: Unable to allocate 6.32 GiB for an array with shape (6, 141430723) and data type float64
```

Looking at HyPer's results, there is not that much difference between the emulated version on the ARM M1 and the native version on the Intel CPU.
DuckDB still wins out by a large margin.

<!-- Our second experiment is selecting all columns, ordering by 1 up to 4 columns.
The columns used are:
1. `cs_sold_time_sk`
2. `cs_sold_date_sk`
3. `cs_ship_date_sk`
4. `cs_bill_customer_sk`

__TODO:__ maybe these columns should be different?

This experiment will tell us something about how well the different systems handle multiple `ORDER BY` clauses.

<img src="/images/blog/sorting/tpcds_catalog_sales_sorting.svg" alt="Increasing the number of order clauses for the catalog_sales table" title="Catalog Sales Order Clauses Experiment" style="max-width:100%"/>

__TODO:__ analyze plot MAYBE MAKE IT RELATIVE INCREASE AS MORE COLUMNS ARE ADDED?
ClickHouse has a jump in runtime when going from 1 to 2 order by clauses, because they do not encode the key columns as a binary string.
This means that their comparator works along the lines of: If the first key column is equal, compare the second one too.
This comparator has a branch prediction, and random access into the second column, which slows down the comparison.
Such comparators can be found in their source code [here](https://github.com/ClickHouse/ClickHouse/blob/master/src/Core/SortCursor.h#L370).
This effect diminishes as we add more key columns, because it is uncommon to have rows that have more than 2 or 3 equal columns.

DuckDB's performance goes down gradually as more clauses are added.
This is mainly because the key columns that are encoded in the binary string format are not decoded, but rather duplicated as a payload column.
This means that there is full data duplication if there are 34 order clauses.
Decoding the binary string format is possible, but this has not yet been implemented.
Still, with fewer `ORDER BY` clauses, DuckDB is ahead of the pack. -->

#### Customer
Now that we've seen how the systems handle large amounts of fixed-size types, it's time to see some variable-size types!
For our first experiment on the `customer` table, we'll select all columns, and order them by either 3 integer columns (`c_birth_year`, `c_birth_month`, `c_birth_day`), or by 2 string columns (`c_first_name`, `c_last_name`).
Comparing strings is more difficult than comparing integers, so we'd expect ordering by strings to take more time.

<img src="/images/blog/sorting/tpcds_customer_type_sort_barplot.svg" alt="Comparing sorting speed with different sorting key types" title="Customer Sort Type Experiment" style="max-width:100%"/>

As expected, ordering by strings is more expensive that ordering by integers.
All systems except Pandas have only a small difference between ordering by integers and ordering by strings.
This difference could be explained by an expensive comparator between strings.

In our previous experiment we saw that Pandas is very fast at re-ordering the payload columns.
In our next experiment we'll zoom in on this.
We want to know good the systems are at re-ordering string payload columns, compared to integer payload columns.
Remember, `customer` has 10 integer columns, and 8 string columns.
Again, we'd expect it to be more difficult to re-order integer columns than it is to re-order string columns.

<img src="/images/blog/sorting/tpcds_customer_type_payload_barplot.svg" alt="Comparing sorting speed with different payload types" title="Customer Payload Type Experiment" style="max-width:100%"/>

As expected, re-ordering strings takes more time than re-ordering integers, but only by a little.

__TODO:__ analyze results, why is Pandas so quick?

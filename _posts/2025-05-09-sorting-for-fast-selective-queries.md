---
layout: post
title: "Approximate Sorting for Fast Selective Queries"
author: "Alex Monahan"
thumb: "/images/blog/thumbs/indexing-tips.svg"
image: "/images/blog/thumbs/indexing-tips.png"
excerpt: "Sorting data when loading speeds up selective read queries by an order of magnitude using DuckDB's automatic min-max indexes (also known as zone maps). Approximate sorting expands this technique to work when filtering on multiple columns and also works well with timestamps. Converting strings to numeric representations allows them to also benefit from space filling curve approaches like Morton (Z-order) and Hilbert encodings."
tags: ["deep dive"]
---

<!--
Minified Plotly library downloaded from here:
https://github.com/plotly/plotly.js/blob/master/dist/README.md

Cartesian was the smallest distribution that included box plots
-->
<script src="{{ site.baseurl }}/js/plotly-cartesian-3.0.1.min.js"></script>

<div align="center">
<img src="/images/blog/sorting-for-fast-selective-queries/Hilbert-curve_rounded-gradient-animated.gif" alt="Animated Hilbert Encoding across 2 axes." width="600"/>

<a href="https://commons.wikimedia.org/w/index.php?curid=67998181">An animated Hilbert space filling curve</a> by <a href="//commons.wikimedia.org/w/index.php?title=User:TimSauder&amp;action=edit&amp;redlink=1" class="new" title="User:TimSauder (page does not exist)">TimSauder</a> – <span class="int-own-work" lang="en">Own work</span>, <a href="https://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>

</div>

The fastest way to read data is to not read data.
It's as simple as that!
This post is all about how to read as little data as possible to answer multiple different patterns of selective read queries.

> Feel free to skip right to the [experiments](#experimental-results)!

The cases where these techniques are most useful are when read performance is more critical than write performance.
In these cases, we can deliberately add ordering steps that will slow down our writes, but will greatly speed up our reads.

If reading the entire dataset is required for each query in your read workload, then these pruning techniques will not help either!
However, in practice filters are common, especially to look at recent data points.

Using any kind of sorting will be helpful when:

- Your dataset is large and doesn't fit entirely in memory
- You access your data via HTTP(S)
- Your data lives in the cloud on object storage such as AWS S3

These advanced techiques help when one of these situations occur:

- Queries filter on different columns
- Query patterns are not perfectly predictable
- Queries filter by time and at least one other column

Cases like those appear often in the wild!

These examples use the DuckDB file format, but thanks to DuckDB's [partial reading support]({% link docs/stable/extensions/httpfs/https.md %}#partial-reading), these techniques can be generally applied to nearly any columnar file format or database.
This is a great way to speed up querying Parquet files on remote endpoints!

## The “On-Time Flights” Dataset

Ever wondered how likely you will be delayed when you are getting ready to fly?
If you are traveling in the US, you can use a government dataset to see how on-time each route is!
You can [get more details on the dataset at its official site](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFD%20&Yv0x=D), but I grabbed a [Parquet version of the data from Kaggle](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022).
It includes almost 5 years of data on US flights.
Combined, the Parquet files are about 1.1 GB.
This is fairly small when accessed locally but can be more of a challenge over a slow remote connection.
In the rest of the post, we'll run different benchmarks to demonstrate how pruning can help reducing the amount of network traffic required to answer certain queries.

Our hypothetical use case is to serve a dashboard where people can explore a single `origin`, a single `dest` (destination), or an `origin`–`dest` pair.
The `origin` and `dest` columns are three-letter airport codes (like `LAX` or `JFK`).
We assume once you have picked one of those filters, you want all the rows that match and a few arbitrary columns.

Our second experiment will add in a time component and additionally filter to the latest 1, 13, or 52 weeks of data in the dataset.

## Experimental Results

### Multi-Column Sorting

We will show a few approaches to sort data approximately or using space-filling curves to speed up retrieval.
Let's have a look at some illustrative results first and dive into the details in subsequent sections.

The control groups are:

- `random`: Sort by a hash – the worst case scenario!
- `origin`: Single-column sort on `origin`
- `origin-dest`: Sort on `origin`, then on `destination`

Our alternative sorting approaches are:

- `zipped_varchar`: Sort by one letter at a time, alternating between `origin` and `destination`. This approach is implemented using a custom SQL macro – see the [Appendix](#appendix-experiment-details) for details!
- `morton`: Convert `origin` and `destination` into integers, then order by [Morton encoding (Z-order)](https://en.wikipedia.org/wiki/Z-order_curve)
- `hilbert`: Convert `origin` and `destination` into integers, then order by [Hilbert encoding](https://en.wikipedia.org/wiki/Hilbert_curve)

> The Morton and Hilbert encoding functions come from the [`lindel` DuckDB community extension]({% link community_extensions/extensions/lindel.md %}), contributed by [Rusty Conover](https://github.com/rustyconover).
> Thank you to Rusty and the folks who have built the [`lindel` Rust crate](https://crates.io/crates/lindel) upon which the DuckDB extension is based!
> The [`spatial` extension]({% link docs/stable/extensions/spatial/overview.md %}) also contains an [`ST_Hilbert` function]({% link docs/stable/extensions/spatial/functions.md %}#st_hilbert) that works similarly.
> Thanks to [Max Gabrielsson](https://github.com/Maxxen) and the GDAL community!

Both Morton and Hilbert are space filling curve algorithms that are designed to combine multiple columns into an order that preserves some approximate ordering for both columns.
In the geospatial world, they are often used to preserve approximate ordering of latitude and longitude.
They operate on integers or floats, so a SQL macro is used to convert the first few characters of a `VARCHAR` column into an integer as a pre-processing step.
More details are included in the [Appendix](#appendix-experiment-details)!

These plots display query runtime when pulling from a DuckDB file hosted on S3.
Querying a local DuckDB file showed very similar patterns, but with much faster query times overall!

<div id="remote_s3_query_performance_by_origin" style="width:100%;height:400px;min-width:720px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/zonemaps/remote_s3_query_performance_by_origin.json')
        .then(res => res.json())
        .then(parsed_json => {
            let my_element = document.getElementById('remote_s3_query_performance_by_origin');
            Plotly.newPlot( my_element, parsed_json.data, parsed_json.layout );
            });
</script>

We can see that when filtering **by `origin`**, the `origin` single column sort is a full order of magnitude faster than randomly distributed data, requiring only 1.6 seconds instead of 16.
Our advanced techniques are nearly as fast as the dedicated sort on `origin`.

<div id="remote_s3_query_performance_by_destination" style="width:100%;height:400px;min-width:720px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/zonemaps/remote_s3_query_performance_by_destination.json')
        .then(res => res.json())
        .then(parsed_json => {
            let my_element = document.getElementById('remote_s3_query_performance_by_destination');
            Plotly.newPlot( my_element, parsed_json.data, parsed_json.layout );
            });
</script>

However, if you look at the plot **by `destination`**, we see the value of the more balanced techniques.
The `origin_dest` approach of just appending `destination` to the list of sorted columns misses out on much of the benefits.

<div id="remote_s3_query_performance_by_origin_destination" style="width:100%;height:400px;min-width:720px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/zonemaps/remote_s3_query_performance_by_origin_destination.json')
        .then(res => res.json())
        .then(parsed_json => {
            let my_element = document.getElementById('remote_s3_query_performance_by_origin_destination');
            Plotly.newPlot( my_element, parsed_json.data, parsed_json.layout );
            });
</script>

When querying for a **specific `origin` and `destination` pair,** all approaches are significantly faster than random.
However, zooming in on the non-random techniques, the more advanced sorting approaches are as fast or slightly faster than sorting by `origin` or by `origin` and then `destination`.
Performance is also faster than the other experiments, as less data needs to be read (since the filter is more selective).

### Approximate Time Sorting

More recent data tends to be more useful data, so frequently queries filter on a time column.
However, often queries filter on time and on other columns as well.

**Don't just sort on the timestamp column!**
You will miss out on performance benefits.
This is because timestamps tend to be so granular, that in practical terms the data is only sorted by timestamp.
How many rows of your data were inserted at exactly `2025-01-01 01:02:03.456789`?
Probably just one!

To sort on multiple columns as well as a time column, first sort by a truncated timestamp and then on the other columns.
In this experiment, we truncate the `flightdate` column to three levels of granularity: day, month, and year.
We then use our most effective multi-column approach and sort by Hilbert encoding of `origin` and `dest` next.

For each of the query patterns tested previously (filters on `origin`, `destination`, and `origin` / `destination`), we filter on 3 time ranges: the latest 1 week, 13 weeks, and 52 weeks.
This yields a total of 9 scenarios.

<div id="remote_s3_query_performance_by_date_origin" style="width:100%;height:400px;min-width:720px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/zonemaps/remote_s3_query_performance_by_date_origin.json')
        .then(res => res.json())
        .then(parsed_json => {
            let my_element = document.getElementById('remote_s3_query_performance_by_date_origin');
            Plotly.newPlot( my_element, parsed_json.data, parsed_json.layout );
            });
</script>

When querying a week of data for a specific `origin`, sorting at the daily level performs the best.
However, sorting by a more approximate time (month or year) performs better when analyzing the latest 13 or 52 weeks of data.
This is because the more approximate time buckets allow the Hilbert encoding to separate `origin`s into different row groups more effectively.

<div id="remote_s3_query_performance_by_date_destination" style="width:100%;height:400px;min-width:720px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/zonemaps/remote_s3_query_performance_by_date_destination.json')
        .then(res => res.json())
        .then(parsed_json => {
            let my_element = document.getElementById('remote_s3_query_performance_by_date_destination');
            Plotly.newPlot( my_element, parsed_json.data, parsed_json.layout );
            });
</script>

Querying by time and destination follows a very similar pattern, with the ideal sort order being highly dependent on how far back in time is analyzed.

<div id="remote_s3_query_performance_by_date_origin_destination" style="width:100%;height:400px;min-width:720px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/zonemaps/remote_s3_query_performance_by_date_origin_destination.json')
        .then(res => res.json())
        .then(parsed_json => {
            let my_element = document.getElementById('remote_s3_query_performance_by_date_origin_destination');
            Plotly.newPlot( my_element, parsed_json.data, parsed_json.layout );
            });
</script>

Filtering by `origin` and `destination` shows a very different outcome, with a yearly granularity being superior across the board!
This is because the `origin` and `destination` filters are much more effective at skipping row groups when the timestamp ordering is very approximate.

As a result, the best compromise across those three workloads is likely to be the very approximate yearly granularity.
See!
Don't just sort by timestamp!

## How Does it Work?

Let's build up some intuition around these approaches.
Later we will look at metrics that can be used to measure how well sorted each column is.

DuckDB stores data in a columnar fashion (meaning that values within a column are stored together in the same set of blocks).
However, columnar does not mean storing the entire column contiguously!
Before storing data, DuckDB breaks tables up into chunks of rows called row groups.
Within each row group, the data related to a single column is stored contiguously together on disk in one or more blocks.

So, how does this help?
By itself, it does not!
However, at the start of each row group, DuckDB also stores metadata about the column data being stored.
This includes the minimum and maximum values of that column within that row group.
We call these _zone maps_ or _min-max indexes._

When DuckDB receives a SQL query that contains a filter, before reading the column segments off of disk, it checks the metadata first.
Could this filter value possibly fall within the minimum/maximum range of this column segment?
If it is not possible, then DuckDB can skip reading the data in that entire row group.

For example, if we are searching for an `origin` of `PHX`, but the minimum `origin` in a segment is `ABQ` and the maximum is `ATL`, then we can skip reading the data in that segment.
However, if in another segment the min-max were `ABQ` and `SFO`, then we must read that segment and check each row for `PHX`.

So our goal is to sort our data so that each subset of the data we want to retrieve is only stored in a few row groups.
Ideally, you could aim for pulling just a single row group!
However, since DuckDB is multithreaded, you should still see high performance as long as the number of row groups is less than the number of threads (~CPU cores) DuckDB is using.

## Measuring Sortedness

The most effective way to choose a sort order is to simulate your production workload, like in the experiments above.
However, this is not always feasible or easy to do.
Instead, we can measure how well sorted the dataset is on the columns of interest.
The metric we will use is “Number of row groups per Value”.
The way to interpret this is that for selective queries to work effectively, each value being filtered on should only be present in a small number of row groups.
Smaller is better!
However, there are likely diminishing returns when this metric is below the number of threads DuckDB is using.

<div id="number_of_rowgroups_per_value" style="width:100%;height:400px;min-width:720px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/zonemaps/number_of_rowgroups_per_value.json')
        .then(res => res.json())
        .then(parsed_json => {
            let my_element = document.getElementById('number_of_rowgroups_per_value');
            Plotly.newPlot( my_element, parsed_json.data, parsed_json.layout );
            });
</script>

What can be interpreted from this graph?
The random ordering spreads nearly every value across 100 or more row groups (the visualization is truncated at 100 row groups).
This highlights how a random ordering will be very slow for selective queries!
Sorting by `origin` greatly reduces the number of row groups that each `origin` is spread across, but `destination`s are still spread widely.
Sorting by `origin` and `destination` retains the tight distribution of `origin`s and slightly improves the metric for `destination`s.

The three advanced approaches (`zipped_varchar`, `morton`, and `hilbert`) are more balanced, with both `origin`s and `destination`s only occuring in a moderate number of row groups.
While they score worse in the `origin` metric than when sorting directly by `origin`, most `origin`s are spread across fewer row groups than a modern laptop processor's core count, so high performance is retained.
The Hilbert encoding is the most balanced, so by this metric it would be declared the victor!

To calculate this metric, we define several SQL macros using dynamic SQL and the `query` table function.

<details markdown='1'>
<summary markdown='span'>
    Expand for details!
</summary>

```sql
CREATE OR REPLACE FUNCTION sq(my_varchar) AS (
    '''' || replace(my_varchar,'''', '''''') || ''''
);
CREATE OR REPLACE FUNCTION dq(my_varchar) AS (
    '"' || replace(my_varchar,'"', '""') || '"'
);
CREATE OR REPLACE FUNCTION nq(my_varchar) AS (
    replace(my_varchar, ';', 'No semicolons are permitted here')
);


CREATE OR REPLACE FUNCTION dq_list(my_list) AS (
    list_transform(my_list, (i) -> dq(i))
);
CREATE OR REPLACE FUNCTION nq_list(my_list) AS (
    list_transform(my_list, (i) -> nq(i))
);

CREATE OR REPLACE FUNCTION dq_concat(my_list, separator) AS (
    list_reduce(dq_list(my_list), (x, y) -> x || separator || y)
);
CREATE OR REPLACE FUNCTION nq_concat(my_list, separator) AS (
    list_reduce(nq_list(my_list), (x, y) -> x || separator || y)
);


CREATE OR REPLACE FUNCTION rowgroup_counts(table_name, column_list) AS TABLE (
    FROM query('
    WITH by_row group_id AS (
        FROM ' || dq(table_name) || '
        SELECT
        ceiling((count(*) over ()) / 122880) AS total_row groups,
        floor(rowid / 122880) AS row group_id,
        ' || dq_concat(column_list, ',') || '
    ), row group_id_counts AS (
    FROM by_row group_id
    SELECT
        case ' ||
        nq_concat(list_transform(column_list, (i) -> ' when grouping('||dq(i)||') = 0 then alias('||dq(i)||') '),' ')
            || ' end AS column_name,
        coalesce(*columns(* exclude (row group_id, total_row groups))) AS column_value,
        first(total_row groups) AS total_row groups,
        count(distinct row group_id) AS row group_id_count
    GROUP BY
        GROUPING SETS ( ' || nq_concat(list_transform(dq_list(column_list), (j) -> '('||j||')'), ', ') ||' )
    )
    FROM row group_id_counts
    SELECT
        '||sq(table_name)||' AS table_name,
        *
    ORDER BY
        column_name
    ')
);

-- This is an optional function that can summarize the data
-- as an alternative to boxplot charts
CREATE OR REPLACE FUNCTION summarize_rowgroup_counts(table_name, column_list) AS TABLE (
    FROM rowgroup_counts(table_name, column_list)
    SELECT
        table_name,
        column_name,
        total_row groups,
        min(row group_id_count) AS min_cluster_depth,
        avg(row group_id_count) AS avg_cluster_depth,
        max(row group_id_count) AS max_cluster_depth,
        map([0.1, 0.25, 0.5, 0.75, 0.9], quantile_cont(row group_id_count, [0.1, 0.25, 0.5, 0.75, 0.9]))::json AS quantiles,
        histogram(row group_id_count,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 32, 64, 128, 256])::json AS histograms,
    GROUP BY ALL
    ORDER BY ALL
);
```

</details>

We can then call the `rowgroup_counts` function on any table and any columns!

```sql
FROM rowgroup_counts('flights_hilbert', ['origin', 'dest']);
```

| table_name      | column_name | column_value | total_row groups | row group_id_count |
| :-------------- | :---------- | :----------- | --------------: | ----------------: |
| flights_hilbert | dest        | PSG          |             238 |                 2 |
| flights_hilbert | dest        | ESC          |             238 |                 2 |
| flights_hilbert | dest        | YUM          |             238 |                 2 |
| flights_hilbert | dest        | TWF          |             238 |                 2 |
| flights_hilbert | dest        | TUL          |             238 |                 7 |
| ...             | ...         | ...          |             ... |               ... |

The `row group_id_count` column is a measurement of how many distinct row groups that a specific column value is present in, so it is an indicator of how much work DuckDB would need to do to pull all data associated with that value.

> This calculation uses the [pseudo-column `rowid`]({% link docs/preview/sql/statements/select.md %}#row-ids), and it requires data to have been inserted in a single batch to be perfectly accurate.
> It is directionally correct for data inserted in batches.

## Additional Techniques

There are more ways to take full advantage of the min-max indexes in DuckDB!

### Avoid Small Inserts

If a workload is inserting data in small batches or a single row at a time, there is not an opportunity to effectively sort the data when it is being inserted.
Instead, the data will be sorted largely by insertion time, which will only provide effective pruning for time-based filters.
If possible, bulk inserts or batching will allow the sorting to work more effectively for other columns.
As an alternative, there can be a periodic re-sorting job, which is analogous to a re-indexing task in transactional systems.

### Sort in Chunks

Sorting can be a computationally expensive operation for large tables.
One way to reduce the amount of memory (or disk spill) required when sorting is to process the table in pieces by looping through multiple SQL statements, each filtered to a specific chunk.
Since SQL does not have a looping construct, this would be handled by a host language (Python, Jinja templating, etc.).
The pseudocode would be to:

```sql
CREATE OR REPLACE TABLE sorted_table AS
    FROM unsorted_table
    WITH NO DATA;

for chunk in chunks:
    INSERT INTO sorted_table
        FROM unsorted_table
        WHERE chunking_column = chunk
        ORDER BY other_columns...;
```

This will have the effect of sorting initially by the chunking column, and then by the `other_columns`.
It may also take longer to run (since the data must be scanned once per chunk), but memory use is likely to be much lower.

### Sort the First Few Characters of Strings

Approximate sorting works well for improving read performance, and the runtime of [DuckDB's radix sort algorithm]({% post_url 2021-08-27-external-sorting %}) is sensitive to the length of strings (by design!).
The time complexity of the algorithm is `O(nk)`, where `n` is the number of rows, and `k` is the width of the sorting key.
Sorting by just the first few characters of a `VARCHAR` can be quicker and less compute intensive while achieving similar read performance.
DuckDB's `VARCHAR` data type also inlines the first 12 bytes of the string, so sorting by less than those 12 bytes (so, under 12 characters when using ASCII) can improve performance.
For example:

```sql
CREATE OR REPLACE TABLE sorted_table AS
    FROM unsorted_table
    ORDER BY varchar_column_to_sort[:12];
```

### Filter by More Columns

Adding filters to a `WHERE` clause can be helpful if those columns being filtered have any kind of approximate order.
For example, instead of just filtering by `customer_id`, if the table is sorted by `customer_type`, include that in the query also.
Often, if the `customer_id` is known at query time, it is possible to know other metadata as well.

### Adjust the Row Group Size

One parameter that can be tuned for specific workloads is the number of rows within a row group (the `ROW_GROUP_SIZE`).
If there are many unique values within a column being filtered on, then a smaller number of rows per row group could reduce the total number of rows that must be scanned.
However, there is an overhead of checking metadata more often when row groups are smaller, so there is a tradeoff.

A larger row group size may actually be preferable if a table is particularly large and queries are very selective.
For example, if querying a large fact table with years of history, but filtering to only the last week of data.
Larger row group sizes reduce the number of metadata checks that are necessary to reach the recent data.
However, each row group is larger, so there is a tradeoff there as well.

To adjust the row group size, pass in a parameter when attaching a database.
Note that a row group size should be a power of 2.
The minimum row group size is the vector size of DuckDB, which by default is 2048.

```sql
ATTACH './smaller_row groups.duckdb' (ROW_GROUP_SIZE 8192);
```

## Conclusion

Ordering data upon insert can significantly speed up read queries that include filters.
Creative sorting approaches that use space filling curves and/or rounded timestamp columns allow this approach to work effectively across multiple columns.
Once your dataset becomes large or you are storing it remotely, consider applying these techniques.
Plus, these approaches can be used in nearly any columnar file format or database!

Happy analyzing!

## Appendix: Experiment Details

All experiments were run on an M1 MacBook Pro with DuckDB v1.2.2.
Note that the remote S3 tests were run over WiFi (which adds a bit of variability...), so please feel free to benchmark independently!

### Table Creation Time

Creating a DuckDB table from Parquet files without sorting took slightly over 21 seconds.
Each other approach copied from the unsorted DuckDB table and created a new table.
The various methods of sorting required similar amounts of time (between 48 and 61 seconds), so we are free to choose the one with the most effective results without considering relative insert performance.
However, it is worth noting that overall insert performance slows down by nearly 3× with any sorting.

| Table name       | Creation time (s) |
| :--------------- | ----------------: |
| `from_parquet`   |              21.4 |
| `random`         |              60.2 |
| `origin`         |              51.9 |
| `origin_dest`    |              48.7 |
| `zipped_varchar` |              58.2 |
| `morton`         |              54.6 |
| `hilbert`        |              58.5 |
| `hilbert_day`    |              58.7 |
| `hilbert_month`  |              53.8 |
| `hilbert_year`   |              60.2 |

### Basic Sorting

<details markdown='1'>
<summary markdown='span'>
    For reproducibility, here are the very standard queries used to initially load the data from Parquet, sort randomly, sort by `origin`, and sort by `origin` and then `destination`.
</summary>

```sql
CREATE TABLE IF NOT EXISTS flights AS
    FROM './Combined_Flights*.parquet';

CREATE TABLE IF NOT EXISTS flights_random AS
    FROM flights
    ORDER BY
        hash(rowid + 42);

CREATE TABLE IF NOT EXISTS flights_origin AS
    FROM flights
    ORDER BY
        origin;

CREATE TABLE IF NOT EXISTS flights_origin_dest AS
    FROM flights
    ORDER BY
        origin,
        dest;
```

</details>

## Sorting by Zipped `VARCHAR` Columns

As an example of an approach that does not require an extension, this SQL macro roughly approximates a space filling curve approach, but using alphanumeric characters instead of integers.
The outcome is a dataset that is somewhat sorted by one column and somewhat sorted by another.

```sql
CREATE OR REPLACE FUNCTION main.zip_varchar(i, j, num_chars := 6) AS (
    -- By default using 6 characters from each string so that
    -- if data is ASCII, we can fit it all in the 12 byte inline portion of DuckDB's string representation
    [
        list_value(z[1], z[2])
        FOR z
        IN list_zip(
            substr(i, 1, num_chars).rpad(num_chars, ' ').string_split(''),
            substr(j, 1, num_chars).rpad(num_chars, ' ').string_split('')
        )
    ].flatten().array_to_string(' ')
);

CREATE TABLE IF NOT EXISTS flights_zipped_varchar AS
    FROM flights
    ORDER BY
        main.zip_varchar(origin, dest, num_chars := 3);
```

Here is an example of the output that the `zip_varchar` function produces:

```sql
SELECT
    'ABC' AS origin,
    'XYZ' AS dest,
    main.zip_varchar(origin, dest, num_chars := 3) AS zipped_varchar;
```

| origin | dest | zipped_varchar |
| ------ | ---- | -------------- |
| ABC    | XYZ  | AXBYCZ         |

## Space Filling Curves

The goal of a space filling curve is to map multiple dimensions (in our case, two: `origin` and `destination`) down to a single dimension, but to preserve the higher dimension locality between data points.
One application of space filling curves is in geospatial analytics and it is a helpful illustration.
If our dataset contained the latitude and longitude coordinates of every café on earth (one row per café), but we wanted to sort so that cafés that are physically close to one another are near each other in the list, we could use a space filling curve.
cafés that are somewhat close in both latitude and longitude will receive a similar Morton or Hilbert encoding value.
This will allow us to quickly execute queries like “Find all cafés within this rectangular region on a map”.
(A rectangle like that is called a bounding box in geospatial-land!)

Morton and Hilbert encodings are designed to accept integers or floating point numbers.
However, in our examples, we want to apply these techniques to `VARCHAR` columns.
Strings actually encode a substantial amount of data per length of the string.
This is because numbers can only have 10 values per digit (in our base 10 numbering system), but a string can have many more (all lowercase letters, capital letters, or symbols).
As a result, we are not able to encode very long strings into integers – only the first few characters.
This will still work for our approximate sorting use case!

This SQL function can convert a `VARCHAR` containing ASCII characters (up to 8 characters in length) into a `UBIGINT`.
It splits the `VARCHAR` up into individual characters, calculates the ASCII number for that character, converts that to bits, concatenates the bits together, then converts to a `UBIGINT`.

```sql
CREATE OR REPLACE FUNCTION main.varchar_to_ubigint(i, num_chars := 8) AS (
    -- The maximum number of characters that will fit in a UBIGINT is 8
    -- and a UBIGINT is the largest type that the lindel community extension accepts for Hilbert or Morton encoding
    list_reduce(
        [
            ascii(my_letter)::UTINYINT::BIT::VARCHAR
            FOR my_letter
            IN (i[:num_chars]).rpad(num_chars, ' ').string_split('')
        ],
        (x, y) -> x || y
    )::BIT::UBIGINT
);
```

The `morton_encode` and `hilbert_encode` functions from the [`lindel` community extension]({% link community_extensions/extensions/lindel.md %}) can then be used within the `ORDER BY` clause to sort by the Morton or Hilbert encoding.

```sql
INSTALL lindel FROM community;
LOAD lindel;

CREATE TABLE IF NOT EXISTS flights_morton AS
    FROM flights
    ORDER BY
        morton_encode([
            varchar_to_ubigint(origin, num_chars := 3),
            varchar_to_ubigint(dest, num_chars := 3)
        ]::UBIGINT[2]);

CREATE TABLE IF NOT EXISTS flights_hilbert AS
    FROM flights
    ORDER BY
        hilbert_encode([
            varchar_to_ubigint(origin, num_chars := 3),
            varchar_to_ubigint(dest, num_chars := 3)
        ]::UBIGINT[2]);
```

Alternatively, the [`spatial` extension]({% link docs/stable/extensions/spatial/overview.md %}) can be used to execute a Hilbert encoding.
It requires a bounding box to be supplied, as this helps determine the granularity of the encoding for geospatial use cases.
It performed similarly to the Hilbert approach included in the above plots.

```sql
SET VARIABLE bounding_box = (
    WITH flights_converted_to_ubigint AS (
        FROM flights
            SELECT
            *,
            varchar_to_ubigint(origin, num_chars := 3) AS origin_ubigint,
            varchar_to_ubigint(dest, num_chars := 3) AS dest_ubigint
        )
    FROM flights_converted_to_ubigint
    SELECT {
        min_x: min(origin_ubigint),
        min_y: min(dest_ubigint),
        max_x: max(origin_ubigint),
        max_y: max(dest_ubigint)
    }::BOX_2D
);
CREATE OR REPLACE TABLE flights_hilbert_spatial AS
    FROM flights
    ORDER BY
        ST_Hilbert(
            varchar_to_ubigint(origin, num_chars := 3),
            varchar_to_ubigint(dest, num_chars := 3),
            getvariable('bounding_box')
        );
```

## Approximate Time Sorting

Sorting by an “approximate time” involves truncating the time to the nearest value of a certain time granularity.
This can be accomplished with the `date_trunc` function.
Once data is sorted by an approximate time, other sorting techniques can be applied.
In this case, the dataset is subsequently sorted by the Hilbert encoding of `origin` and `dest`.

```sql
CREATE TABLE IF NOT EXISTS flights_hilbert_day AS
    FROM flights
    ORDER BY
        date_trunc('day', flightdate),
        hilbert_encode([
            varchar_to_ubigint(origin, num_chars := 3),
            varchar_to_ubigint(dest, num_chars := 3)
        ]::UBIGINT[2]);

CREATE TABLE IF NOT EXISTS flights_hilbert_month AS
    FROM flights
    ORDER BY
        date_trunc('month', flightdate),
        hilbert_encode([
            varchar_to_ubigint(origin, num_chars := 3),
            varchar_to_ubigint(dest, num_chars := 3)
        ]::UBIGINT[2]);

CREATE TABLE IF NOT EXISTS flights_hilbert_year AS
    FROM flights
    ORDER BY
        date_trunc('year', flightdate),
        hilbert_encode([
            varchar_to_ubigint(origin, num_chars := 3),
            varchar_to_ubigint(dest, num_chars := 3)
        ]::UBIGINT[2]);
```

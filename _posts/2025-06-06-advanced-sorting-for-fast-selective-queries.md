---
layout: post
title: "Faster Dashboards with Multi-Column Approximate Sorting"
author: "Alex Monahan"
thumb: "/images/blog/thumbs/indexing-tips.svg"
image: "/images/blog/thumbs/indexing-tips.png"
excerpt: "With any columnar data format, using advanced multi-column sorting when loading data can improve performance on a wide variety of selective read queries. Space filling curve encodings like Morton (Z-Order) and Hilbert approximately sort multiple columns together. Sorting by rounded timestamps adds additional benefits when filtering on recent data."
tags: ["deep dive"]
---

<!--
Minified Plotly library downloaded from here:
https://github.com/plotly/plotly.js/blob/master/dist/README.md

Cartesian was the smallest distribution that included box plots
-->
<script src="{{ site.baseurl }}/js/plotly-cartesian-3.0.1.min.js"></script>

<div align="center" id="hilbert-curve">
<img src="/images/blog/sorting-for-fast-selective-queries/Hilbert-curve_rounded-gradient-animated.gif" alt="Animated Hilbert Encoding across 2 axes." width="600"/>

<a href="https://commons.wikimedia.org/w/index.php?curid=67998181">An animated Hilbert space filling curve</a> by <a href="//commons.wikimedia.org/w/index.php?title=User:TimSauder&amp;action=edit&amp;redlink=1" class="new" title="User:TimSauder (page does not exist)">TimSauder</a> – <span class="int-own-work" lang="en">Own work</span>, <a href="https://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>

</div>

It is rare to have a dashboard with a single chart.
It is even more rare to only query your data one way.
It is rarer still to query your data with no filters at all!

When queries read a subset of the total rows, sorting data while loading provides significant benefits.
Please have a look at [the prior post in this series]({% post_url 2025-05-14-sorting-for-fast-selective-queries %}) to understand how this approach works and for practical tips!

In order to see these benefits in a wider variety of real world cases, we have to get a bit more creative.
These advanced techniques help when one of these situations occur:

- Queries filter on different columns
- Query patterns are not perfectly predictable
- Queries filter by time and at least one other column

In this post, we describe several advanced sorting strategies, compare them with some experiments (microbenchmarks), and then calculate a metric to measure their effectiveness.

## The Strategy

Instead of sorting precisely by one or a small number of columns, we want to sort approximately by a larger number of columns.
That will allow queries with different `WHERE` clauses to all benefit from DuckDB's [min-max indexes (zone maps)]({% link docs/stable/sql/indexes.md %}#min-max-index-zonemap).
This post introduces two high-level approaches with several examples of each: sorting by space filling curves, and sorting by truncated timestamps.

### Space Filling Curves

Both Morton and Hilbert are space filling curve algorithms that are designed to combine multiple columns into an order that preserves some approximate ordering for both columns.
One application of space filling curves is in geospatial analytics and it is a helpful illustration.

If a dataset contained the latitude and longitude coordinates of every café on earth (one row per café), but we wanted to sort so that cafés that are physically close to one another are near each other in the list, we could use a space filling curve.
Cafés that are somewhat close in both latitude and longitude will receive a similar Morton or Hilbert encoding value.
This will allow us to quickly execute queries like “Find all cafés within this rectangular region on a map”.
(A rectangular region like that is called a bounding box in geospatial-land!)
The [GIF at the top of this post](#hilbert-curve) shows various levels of granularity of a Hilbert encoding – imagine if the x axis were longitude and the y axis were latitude.
The "zig-zag" line of the Hilbert algorithm is the list of cafés, sorted approximately.

Both Morton and Hilbert operate on integers or floats, but this post outlines a way to use them to sort `VARCHAR` columns as well.
A SQL macro is used to convert the first few characters of a `VARCHAR` column into an integer as a pre-processing step.

### Truncated Timestamps

More recent data tends to be more useful data, so frequently queries filter on a time column.
However, often queries filter on time and on other columns as well.

**Don't just sort on the timestamp column!**
You will miss out on performance benefits.
This is because timestamps tend to be so granular, that in practical terms the data is only sorted by timestamp.
How many rows of your data were inserted at exactly `2025-01-01 01:02:03.456789`?
Probably just one!

To sort on multiple columns as well as a time column, first sort by a truncated timestamp (truncated to the start of the day, week, year, etc.) and then on the other columns.

## The “On-Time Flights” Dataset

Ever wondered how likely you will be delayed when you are getting ready to fly?
If you are traveling in the US, you can use a government dataset to see how on-time each route is!
You can [get more details on the dataset at its official site](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFD%20&Yv0x=D), but I grabbed a [Parquet version of the data from Kaggle](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022).
It includes almost 5 years of data on US flights.
Combined, the Parquet files are about 1.1 GB.
This is fairly small when accessed locally but can be more of a challenge over a slow remote connection.
In the rest of the post, we'll run different benchmarks to demonstrate how pruning can help reducing the amount of network traffic required to answer certain queries.

Our first experiment is a hypothetical use case to serve a dashboard where people can explore a single `origin`, a single `dest` (destination), or an `origin`–`dest` pair.
The `origin` and `dest` columns are three-letter airport codes (like `LAX` or `JFK`).
We assume once you have picked one of those filters, you want all the rows that match and a few arbitrary columns.

Our second experiment will add in a time component where our hypothetical users could additionally filter to the latest 1, 13, or 52 weeks of data in the dataset.

## Experimental Design

We will show a few approaches to sort data approximately to speed up retrieval.

The control groups are:

- `random`: Sort by a hash – the worst case scenario!
- `origin`: Single-column sort on `origin`
- `origin-dest`: Sort on `origin`, then on `destination`

Our alternative sorting approaches are:

- `zipped_varchar`: Sort by one letter at a time, alternating between `origin` and `destination`.
    – For example, an `origin` of `ABC` and a `destination` of `XYZ` would become `AXBYCZ`, which would then be sorted.
- `morton`: Convert `origin` and `destination` into integers, then order by [Morton encoding (Z-order)](https://en.wikipedia.org/wiki/Z-order_curve)
- `hilbert`: Convert `origin` and `destination` into integers, then order by [Hilbert encoding](https://en.wikipedia.org/wiki/Hilbert_curve)

> The `zipped_varchar` algorithm is implemented using a SQL macro so no extensions are needed.
> It also handles arbitrary length strings.

> The Morton and Hilbert encoding functions come from the [`lindel` DuckDB community extension]({% link community_extensions/extensions/lindel.md %}), contributed by [Rusty Conover](https://github.com/rustyconover).
> Thank you to Rusty and the folks who have built the [`lindel` Rust crate](https://crates.io/crates/lindel) upon which the DuckDB extension is based!
> The [`spatial` extension]({% link docs/stable/core_extensions/spatial/overview.md %}) also contains an [`ST_Hilbert` function]({% link docs/stable/core_extensions/spatial/functions.md %}#st_hilbert) that works similarly.
> Thanks to [Max Gabrielsson](https://github.com/Maxxen) and the GDAL community!

These plots display query runtime when pulling from a DuckDB file hosted on S3.
These same techniques can also be successfully applied to the [DuckLake](https://ducklake.select/) integrated data lake and catalog format!
DuckLake is the modern evolution of the cloud data Lakehouse – take a minute to check out the [launch post]({% post_url 2025-05-27-ducklake %}) if you haven't yet!
DuckLake has an [additional concept of a partition](https://ducklake.select/docs/stable/duckdb/advanced_features/partitioning), which enables entire files to be skipped.
To take full advantage of DuckLake, first partition your data (by time or otherwise) and then apply the techniques in this post when loading your data.

All experiments were run on an M1 MacBook Pro with DuckDB v1.2.2.
The tests were conducted with the DuckDB Python client with results returned as Apache Arrow tables.
In between each query, the DuckDB connection is closed and recreated (this time is not measured as a part of the results).
This is to better simulate a single user's experience accessing the dashboard in our hypothetical use case.

<details markdown='1' style="font-size:19px;margin-bottom:15px;">
<summary markdown='span'>
    Expand to see the basic sorting queries
</summary>

For reproducibility, here are the very standard queries used to initially load the data from Parquet, sort randomly, sort by `origin`, and sort by `origin` and then `destination`.
The parquet files were downloaded [from Kaggle](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022).

```sql
CREATE TABLE IF NOT EXISTS flights AS
    FROM './Combined_Flights*.parquet';

-- The hash function is used instead of random
-- for consistency across re-runs
CREATE TABLE IF NOT EXISTS flights_random AS
    FROM flights
    ORDER BY hash(rowid + 42);

CREATE TABLE IF NOT EXISTS flights_origin AS
    FROM flights
    ORDER BY origin;

CREATE TABLE IF NOT EXISTS flights_origin_dest AS
    FROM flights
    ORDER BY origin, dest;
```
</details>
<details markdown='1' style="font-size:19px;margin-bottom:15px;">
<summary markdown='span'>
    Expand to see the Zipped `VARCHAR` sorting queries
</summary>

As an example of an approach that does not require an extension, this SQL macro roughly approximates a space filling curve approach, but using alphanumeric characters instead of integers.
The outcome is a dataset that is somewhat sorted by one column and somewhat sorted by another.

```sql
CREATE OR REPLACE FUNCTION main.zip_varchar(i, j, num_chars := 6) AS (
    -- By default using 6 characters from each string so that
    -- if data is ASCII, we can fit it all in 12 bytes so that it is stored inline
    -- rather than requiring a pointer
    [
        list_value(z[1], z[2])
        FOR z
        IN list_zip(
            substr(i, 1, num_chars).rpad(num_chars, ' ').string_split(''),
            substr(j, 1, num_chars).rpad(num_chars, ' ').string_split('')
        )
    ].flatten().array_to_string('')
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

</details>
<details markdown='1' style="font-size:19px;margin-bottom:15px;">
<summary markdown='span'>
    Expand to see the Morton and Hilbert sorting queries
</summary>

The goal of a space filling curve is to map multiple dimensions (in our case, two: `origin` and `destination`) down to a single dimension, but to preserve the higher dimension locality between data points.
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

Alternatively, the [`spatial` extension]({% link docs/stable/core_extensions/spatial/overview.md %}) can be used to execute a Hilbert encoding.
It requires a bounding box to be supplied, as this helps determine the granularity of the encoding for geospatial use cases.
It performed similarly to the Hilbert approach included in the experimental results.

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
</details>

<details markdown='1' style="font-size:19px;margin-bottom:15px;">
<summary markdown='span'>
    Expand to see the selective read queries used to measure performance
</summary>

In summary, this microbenchmark tests:

1. Querying tables sorted by the 6 different approaches (3 control and 3 advanced)
1. Filtering using three query patterns: filters on `origin`, `destination`, and `origin` / `destination`
1. Filtering with 4 different `origin`/`dest` pairs:
    1. SFO – LAX
    1. LAX – SFO
    1. ORD – LGA
    1. LGA – ORD

Each of these 72 unique queries are repeated 3 times for a total of 216 queries.
All are included in the resulting plots.

```sql
FROM ⟨sorted_table⟩
SELECT flightdate, airline, origin, dest, deptime, arrtime
WHERE origin = ⟨origin⟩;

FROM ⟨sorted_table⟩
SELECT flightdate, airline, origin, dest, deptime, arrtime
WHERE dest = ⟨dest⟩;

FROM ⟨sorted_table⟩
SELECT flightdate, airline, origin, dest, deptime, arrtime
WHERE origin = ⟨origin⟩ AND dest = ⟨dest⟩;
```

</details>

## Experimental Results

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

The Hilbert encoding method provides the most consistent performance across the three query patterns.
It would be the best choice to support all 3 workloads.

### Approximate Time Sorting

Sorting by an “approximate time” involves truncating the time to the nearest value of a certain time granularity.
In this experiment, we load the data with 3 different sorting approaches.
We first sort on a truncation of the `flightdate` column, truncated to either day, month, or year.
We then use our most effective multi-column approach and sort by the Hilbert encoding of `origin` and `dest` next.

When measuring performance, we test each of the query patterns tested previously (filters on `origin`, `destination`, and `origin` / `destination`), but additionally filter on three different time ranges: the latest 1 week, 13 weeks, and 52 weeks.

<details markdown='1' style="font-size:19px;margin-bottom:15px;">
<summary markdown='span'>
    Expand to see the approximate time sorting queries
</summary>

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
</details>

<details markdown='1' style="font-size:19px;margin-bottom:15px;">
<summary markdown='span'>
    Expand to see the selective read queries used to measure performance
</summary>

In summary, this microbenchmark tests:
1. Querying tables sorted with `flightdate` truncated to three levels of granularity: day, month, and year, then by Hilbert encoding.
1. Filtering on three time ranges: the latest 1 week, 13 weeks, and 52 weeks
1. Filtering on `origin`, `destination`, and `origin` / `destination`
1. Filtering with 4 different `origin`/`dest` pairs:
    1. SFO – LAX
    1. LAX – SFO
    1. ORD – LGA
    1. LGA – ORD

Each of these 108 unique queries are repeated 3 times for a total of 324 queries.

```sql
FROM ⟨sorted_table⟩
SELECT flightdate, airline, origin, dest, deptime, arrtime
WHERE
    origin = ⟨origin⟩
    AND flightdate >= ('2022-07-31'::TIMESTAMP – INTERVAL ⟨time_range⟩ WEEKS);

FROM ⟨sorted_table⟩
SELECT flightdate, airline, origin, dest, deptime, arrtime
WHERE
    dest = ⟨dest⟩
    AND flightdate >= ('2022-07-31'::TIMESTAMP – INTERVAL ⟨time_range⟩ WEEKS);

FROM ⟨sorted_table⟩
SELECT flightdate, airline, origin, dest, deptime, arrtime
WHERE
    origin = ⟨origin⟩
    AND dest = ⟨dest⟩
    AND flightdate >= ('2022-07-31'::TIMESTAMP – INTERVAL ⟨time_range⟩ WEEKS);
```

</details>
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

### Table Creation Time

The upfront investment required to see these benefits is the time required to sort the data when inserting.
Typically this is still a good trade off – data inserts tend to happen in the background, but nobody wants to be staring at dashboard loading spinners!

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

## Measuring Sortedness

The most effective way to choose a sort order is to simulate your production workload, like in the experiments above.
However, this is not always feasible or easy to do.
Instead, we can measure how well sorted the dataset is on the columns of interest.
The metric we will use is “Number of Row Groups per Value”.
The way to interpret this is that for selective queries to work effectively, each value being filtered on should only be present in a small number of row groups.
Smaller is better!
However, there are likely diminishing returns when this metric is below the number of threads DuckDB is using.

> Other database systems measure a similar metric called "Clustering Depth".

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
The random ordering spreads nearly every value across 100 or more row groups (the visualization is truncated at 100 row groups for readability).
This highlights how a random ordering will be very slow for selective queries!
Sorting by `origin` greatly reduces the number of row groups that each `origin` is spread across, but `destination`s are still spread widely.
Sorting by `origin` and `destination` retains the tight distribution of `origin`s and slightly improves the metric for `destination`s.

The three advanced approaches (`zipped_varchar`, `morton`, and `hilbert`) are more balanced, with both `origin`s and `destination`s only occuring in a moderate number of row groups.
While they score worse in the `origin` metric than when sorting directly by `origin`, most `origin`s are spread across fewer row groups than a modern laptop processor's core count, so high performance is retained.
The Hilbert encoding is the most balanced, so by this metric it would be declared the victor as well!

To calculate this metric, we define several SQL macros using dynamic SQL and the `query` table function.

<details markdown='1' style="font-size:19px;margin-bottom:15px;">
<summary markdown='span'>
    Expand to see the macros for calculating “Number of Row Groups per Value”
</summary>

```sql
-- These are helper functions for writing dynamic SQL
-- sq = single quotes
-- dq = double quotes
-- nq = no quotes
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

-- This function produces the "Number of row groups per Value" boxplot
CREATE OR REPLACE FUNCTION rowgroup_counts(table_name, column_list) AS TABLE (
    FROM query('
    WITH by_rowgroup_id AS (
        FROM ' || dq(table_name) || '
        SELECT
        ceiling((count(*) OVER ()) / 122_880) AS total_row_groups,
        floor(rowid / 122_880) AS rowgroup_id,
        ' || dq_concat(column_list, ',') || '
    ), rowgroup_id_counts AS (
    FROM by_rowgroup_id
    SELECT
        case ' ||
        nq_concat(list_transform(column_list, (i) -> ' when grouping(' || dq(i) || ') = 0 then alias(' || dq(i) || ') '),' ')
            || ' end AS column_name,
        coalesce(*columns(* exclude (rowgroup_id, total_row_groups))) AS column_value,
        first(total_row_groups) AS total_row_groups,
        count(distinct rowgroup_id) AS rowgroup_id_count
    GROUP BY
        GROUPING SETS ( ' || nq_concat(list_transform(dq_list(column_list), (j) -> '(' || j || ')'), ', ') ||' )
    )
    FROM rowgroup_id_counts
    SELECT
        ' || sq(table_name) || ' AS table_name,
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
        total_row_groups,
        min(rowgroup_id_count) AS min_cluster_depth,
        avg(rowgroup_id_count) AS avg_cluster_depth,
        max(rowgroup_id_count) AS max_cluster_depth,
        map([0.1, 0.25, 0.5, 0.75, 0.9], quantile_cont(rowgroup_id_count, [0.1, 0.25, 0.5, 0.75, 0.9]))::JSON AS quantiles,
        histogram(rowgroup_id_count, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 32, 64, 128, 256])::JSON AS histograms,
    GROUP BY ALL
    ORDER BY ALL
);
```

</details>

We can then call the `rowgroup_counts` function on any table and any columns!

```sql
FROM rowgroup_counts('flights_hilbert', ['origin', 'dest']);
```

| table_name      | column_name | column_value | total_row_groups | rowgroup_id_count |
| :-------------- | :---------- | :----------- | --------------: | ----------------: |
| flights_hilbert | dest        | PSG          |             238 |                 2 |
| flights_hilbert | dest        | ESC          |             238 |                 2 |
| flights_hilbert | origin      | YUM          |             238 |                 2 |
| ...             | ...         | ...          |             ... |               ... |

The `rowgroup_id_count` column is a measurement of how many distinct row groups that a specific column value is present in, so it is an indicator of how much work DuckDB would need to do to pull all data associated with that value.

> This calculation uses the [pseudo-column `rowid`]({% link docs/preview/sql/statements/select.md %}#row-ids), and it requires data to have been inserted in a single batch to be perfectly accurate.
> It is only an approximate metric when data is inserted in batches.

## Conclusion

When storing data in a columnar file format like a DuckDB database or a Parquet file, approximately sorting by multiple columns can lead to fast read queries across a variety of query patterns.
Sorting using the Hilbert encoding provided high performance across multiple workloads, and sorting by year and then by Hilbert performed well when also filtering by time.

Thanks to the "Number of Row Groups per Value" calculation, we can measure the sortedness of any table by any column, and it was predictive of the experimental performance we observed.
This way we can experiment with different sorting approaches and quickly forecast their effectiveness, without having to benchmark read workloads each time.

Using these approaches can greatly speed up dashboard interactivity when users are unpredictable (which we always are!).
They can also be used in combination with the [the additional techniques outlined in the prior post]({% post_url 2025-05-14-sorting-for-fast-selective-queries %}#additional-techniques) for further benefits.
Data is always different, so we get to be creative!

Happy analyzing, folks!

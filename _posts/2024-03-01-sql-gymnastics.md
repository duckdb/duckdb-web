---
layout: post
title: "SQL Gymnastics: Bending SQL into flexible new shapes"
author: Alex Monahan
avatar: "/images/blog/authors/alex_monahan.jpg"
thumb: "/images/blog/thumbs/240301.png"
excerpt: "Combining multiple features of DuckDB’s friendly SQL allows for highly flexible queries that can be reused across tables."
---

<img src="/images/blog/duck_gymnast.jpg"
     alt="Duck Gymnast"
     width="300"
     />

DuckDB's [especially](/2022/05/04/friendlier-sql) [friendly](/2023/08/23/even-friendlier-sql) [SQL dialect](/docs/guides/sql_features/friendly_sql) simplifies common query operations.
However, these features also unlock new and flexible ways to write advanced SQL! 
In this post we will combine multiple friendly features to both move closer to real-world use cases and stretch your imagination.
These queries are useful in their own right, but their component pieces are even more valuable to have in your toolbox.

What is the craziest thing you have built with SQL? 
We want to hear about it! 
Tag [DuckDB on X](https://twitter.com/duckdb) (the site formerly known as Twitter) or [LinkedIn](https://www.linkedin.com/company/duckdb/mycompany/), and join the [DuckDB Discord community](https://discord.duckdb.org/).

<!--more-->

## Traditional SQL is too rigid to reuse

SQL queries are typically crafted specifically for the unique tables within a database.
This limits reusability. 
For example, have you ever seen a library of high-level SQL helper functions?
SQL as a language typically is not flexible enough to build reusable functions.
Today, we are flying towards a more flexible future!

## Dynamic aggregates macro

In SQL, typically the columns to `SELECT` and `GROUP BY` must be specified individually. 
However, in many business intelligence workloads, groupings and aggregate functions must be easily user-adjustable.
Imagine an interactive charting workflow – first I want to plot total company revenue over time.
Then if I see a dip in revenue in that first plot, I want to adjust the plot to group the revenue by business unit to see which section of the company caused the issue.
This typically requires templated SQL, using a language that compiles down to SQL (like [Malloy](https://www.malloydata.dev/)), or building a SQL string using another programming language.
How much we can do with just SQL?

Let's have a look at a flexible SQL-only approach and then break down how it is constructed. 

<details markdown='1'>
<summary markdown='span'>
    First we will create an example data table. `col1` is unique on each row, but the other columns are various groupings of the rows. 
</summary>

```sql
CREATE OR REPLACE TABLE example AS 
    SELECT x % 11 AS col1, x % 5 AS col2, x % 2 AS col3, 1 AS col4
    FROM range(1, 11) t(x);
FROM example;
```
</details>

| col1 | col2 | col3 | col4 |
|-----:|-----:|-----:|-----:|
| 1    | 1    | 1    | 1    |
| 2    | 2    | 0    | 1    |
| 3    | 3    | 1    | 1    |
| 4    | 4    | 0    | 1    |
| 5    | 0    | 1    | 1    |
| 6    | 1    | 0    | 1    |
| 7    | 2    | 1    | 1    |
| 8    | 3    | 0    | 1    |
| 9    | 4    | 1    | 1    |
| 10   | 0    | 0    | 1    |

### Creating the macro

The macro below accepts lists of columns to include or exclude, a list of columns to aggregate, and an aggregate function to apply.
All of these can be passed in as parameters from the host language that is querying the database.

```sql
-- We use a table macro (or function) for reusability
CREATE OR REPLACE MACRO dynamic_aggregates(
        included_columns,
        excluded_columns,
        aggregated_columns,
        aggregate_function
    ) AS TABLE (
    FROM example 
    SELECT 
        -- Use a COLUMNS expression to only select the columns
        -- we include or do not exclude
        COLUMNS(c -> (
            -- If we are not using an input parameter (list is empty),
            -- ignore it
            (list_contains(included_columns, c) OR
             len(included_columns) = 0)
            AND
            (NOT list_contains(excluded_columns, c) OR
             len(excluded_columns) = 0)
            )),
        -- Use the list_aggregate function to apply an aggregate
        -- function of our choice
        list_aggregate(
            -- Convert to a list (to enable the use of list_aggregate)
            list(
                -- Use a COLUMNS expression to choose which columns
                -- to aggregate
                COLUMNS(c -> list_contains(aggregated_columns, c))
            ), aggregate_function
        )
    GROUP BY ALL -- Group by all selected but non-aggregated columns
    ORDER BY ALL -- Order by each column from left to right 
);
```

#### Executing the macro

Now we can use that macro for many different aggregation operations.
For illustrative purposes, the 3 queries below show different ways to achieve identical results.

Select col3 and col4, and take the minimum values of col1 and col2:

```sql
FROM dynamic_aggregates(
    ['col3', 'col4'], [], ['col1', 'col2'], 'min'
);
```

Select all columns except col1 and col2, and take the minimum values of col1 and col2:

```sql
FROM dynamic_aggregates(
    [], ['col1', 'col2'], ['col1', 'col2'], 'min'
);
```

If the same column is in both the included and excluded list, it is excluded (exclusions win ties).
If we include col2, col3, and col4, but we exclude col2, then it is as if we only included col3 and col4:

```sql
FROM dynamic_aggregates(
    ['col2', 'col3', 'col4'], ['col2'], ['col1', 'col2'], 'min'
);
```

Executing either of those queries will return this result:

| col3 | col4 | list_aggregate(list(example.col1), 'min') | list_aggregate(list(example.col2), 'min') |
|------|------|-------------------------------------------|-------------------------------------------|
| 0    | 1    | 2                                         | 0                                         |
| 1    | 1    | 1                                         | 0                                         |

#### Understanding the design

The first step of our flexible [table macro](/docs/sql/statements/create_macro#table-macros) is to choose a specific table using DuckDB's [`FROM`-first syntax](/2023/08/23/even-friendlier-sql#from-first-in-select-statements).
Well that's not very dynamic! 
If we wanted to, we could work around this by creating a copy of this macro for each table we want to expose to our application.
However, we will show another approach in our next example, and completely solve the issue in a follow up blog post with an in-development DuckDB feature.
Stay tuned!

Then we `SELECT` our grouping columns based on the list parameters that were passed in.
The [`COLUMNS` expression](/docs/sql/expressions/star#columns-expression) will execute a [lambda function](/docs/sql/functions/lambda) to decide which columns meet the criteria to be selected.

The first portion of the lambda function checks if a column name was passed in within the `included_columns` list. 
However, if we choose not to use an inclusion rule (by passing in a blank `included_columns` list), we want to ignore that parameter.
If the list is blank, `len(included_columns) = 0` will evaluate to `true` and effectively disable the filtering on `included_columns`.
This is a common pattern for optional filtering that is generically useful across a variety of SQL queries.
(Shout out to my mentor and friend Paul Bloomquist for teaching me this pattern!)

We repeat that pattern for `excluded_columns` so that it will be used if populated, but ignored if left blank. 
The `excluded_columns` list will also win ties, so that if a column is in both lists, it will be excluded.

Next, we apply our aggregate function to the columns we want to aggregate. 
It is easiest to follow the logic of this part of the query by working from the innermost portion outward.
The `COLUMNS` expression will acquire the columns that are in our `aggregated_columns` list.
Then, we do a little bit of gymnastics (it had to happen sometime...).

If we were to apply a typical aggregation function (like `sum` or `min`), it would need to be specified statically in our macro.
To pass it in dynamically as a string (potentially all the way from the application code calling this SQL statement), we take advantage of a unique property of the [`list_aggregate` function](/docs/sql/functions/nested#list-aggregates).
It accepts the name of a function (as a string) in its second parameter.
So, to use this unique property, we use the [`list` aggregate function](/docs/sql/aggregates#general-aggregate-functions) to transform all the values within each group into a list.
Then we use the `list_aggregate` function to apply the `aggregate_function` we passed into the macro to each list.

Almost done!
Now [`GROUP BY ALL`](/docs/sql/query_syntax/groupby#group-by-all) will automatically choose to group by the columns returned by the first `COLUMNS` expression.
The [`ORDER BY ALL`](/docs/sql/query_syntax/orderby#order-by-all) expression will order each column in ascending order, moving from left to right.

We made it!

> Extra credit! In the next release of DuckDB, version 0.10.1, we will be able to [apply a dynamic alias](https://github.com/duckdb/duckdb/pull/10774) to the result of a `COLUMNS` expression.
> For example, each new aggregate column could be renamed in the pattern `agg_[the original column name]`.
> This will unlock the ability to chain together these type of macros, as the naming will be predictable.  

#### Takeaways

Several of the approaches used within this macro can be applied in a variety of ways in your SQL workflows.
Using a lambda function in combination with the `COLUMNS` expression can allow you to select any arbitrary list of columns.
The `OR len(my_list) = 0` trick allows list parameters to be ignored when blank.
Once you have that arbitrary set of columns, you can even apply a dynamically chosen aggregation function to those columns using `list` and `list_aggregate`.

However, we still had to specify a table at the start.
We are also limited to aggregate functions that are available to be used with `list_aggregate`.
Let's relax those two constraints!

### Creating version 2 of the macro

This approach takes advantage of two key concepts:

* Macros can be used to create temporary aggregate functions
* A macro can query a [Common Table Expression (CTE) / `WITH` clause](/docs/sql/query_syntax/with) that is in scope during execution

```sql
CREATE OR REPLACE MACRO dynamic_aggregates_any_cte_any_func(
    included_columns,
    excluded_columns,
    aggregated_columns
    /* No more aggregate_function */
) AS TABLE (
    FROM any_cte -- No longer a fixed table!
    SELECT 
        COLUMNS(c -> (
            (list_contains(included_columns, c) OR
            len(included_columns) = 0)
            AND 
            (NOT list_contains(excluded_columns, c) OR
            len(excluded_columns) = 0)
            )),
        -- We no longer convert to a list, 
        -- and we refer to the latest definition of any_func 
        any_func(COLUMNS(c -> list_contains(aggregated_columns, c))) 
    GROUP BY ALL 
    ORDER BY ALL 
);
```

#### Executing version 2

When we call this macro, there is additional complexity.
We no longer execute a single statement, and our logic is no longer completely parameterizable (so some templating or SQL construction will be needed).
However, we can execute this macro against any arbitrary CTE, using any arbitrary aggregation function.
Pretty powerful and very reusable!

```sql
-- We can define or redefine any_func right before calling the macro 
CREATE OR REPLACE TEMP FUNCTION any_func(x)
    AS 100.0 * sum(x) / count(x);

-- Any table structure is valid for this CTE!
WITH any_cte AS (
    SELECT
        x % 11 AS id,
        x % 5 AS my_group,
        x % 2 AS another_group,
        1 AS one_big_group
    FROM range(1, 101) t(x)
)
FROM dynamic_aggregates_any_cte_any_func(
    ['another_group', 'one_big_group'], [], ['id', 'my_group']
);
```

| another_group | one_big_group | any_func(any_cte.id) | any_func(any_cte.my_group) |
|---------------|---------------|----------------------|----------------------------|
| 0             | 1             | 502.0                | 200.0                      |
| 1             | 1             | 490.0                | 200.0                      |

#### Understanding version 2

Instead of querying the very boldly named `example` table, we query the possibly more generically named `any_cte`.
Note that `any_cte` has a different schema than our prior example – the columns in `any_cte` can be anything!
When the macro is created, `any_cte` doesn't even exist. 
When the macro is executed, it searches for a table-like object named `any_cte`, and it was defined in the CTE as the macro was called.

Similarly, `any_func` does not exist initially. 
It only needs to be created (or recreated) at some point before the macro is executed.
Its only requirements are to be an aggregate function that operates on a single column. 

> `FUNCTION` and `MACRO` are synonyms in DuckDB and can be used interchangeably! 

#### Takeaways from version 2

A macro can act on any arbitrary table by using a CTE at the time it is called.
This makes our macro far more reusable – it can work on any table!
Not only that, but any custom aggregate function can be used. 

Look how far we have stretched SQL – we have made a truly reusable SQL function! 
The table is dynamic, the grouping columns are dynamic, the aggregated columns are dynamic, and so is the aggregate function.
Our daily gymnastics stretches have paid off. 
However, stay tuned for a way to achieve similar results with a simpler approach in a future post.

## Custom summaries for any dataset

Next we have a truly production-grade example!
This query powers a portion of the MotherDuck Web UI's [Column Explorer](https://motherduck.com/blog/introducing-column-explorer/) component.
[Hamilton Ulmer](https://www.linkedin.com/in/hamilton-ulmer-28b97817/) led the creation of this component and is the author of this query as well!
The purpose of the Column Explorer, and this query, is to get a high-level overview of the data in all columns within a dataset as quickly and easily as possible.

DuckDB has a built-in [`SUMMARIZE` keyword](/docs/guides/meta/summarize) that can calculate similar metrics across an entire table. 
However, for larger datasets, `SUMMARIZE` can take a couple of seconds to load. 
This query provides a custom summarization capability that can be tailored to the properties of your data that you are most interested in. 

Traditionally, databases required that every column be referred to explicitly, and work best when data is arranged in separate columns.
This query takes advantage of DuckDB's ability to apply functions to all columns at once, its ability to [`UNPIVOT`](/docs/sql/statements/unpivot) (or stack) columns, and its [`STRUCT`](/docs/sql/data_types/struct) data type to store key/value pairs.
The result is a clean, pivoted summary of all the rows and columns in a table.

Let's take a look at the entire function, then break it down piece by piece. 

This [example dataset](https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset) comes from [Hugging Face](https://huggingface.co/), which hosts [DuckDB-accessible Parquet files](https://huggingface.co/blog/hub-duckdb) for many of their datasets. 
First, we create a local table populated from this remote Parquet file.

### Creation

```sql
CREATE OR REPLACE TABLE spotify_tracks AS (
    FROM 'https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet?download=true'
);
```

Then we create and execute our `custom_summarize` macro. 
We use the same `any_cte` trick from above to allow this to be reused on any query result or table.

```sql
CREATE OR REPLACE MACRO custom_summarize() AS TABLE (
    WITH metrics AS (
        FROM any_cte 
        SELECT 
            {
                name: first(alias(COLUMNS(*))),
                type: first(typeof(COLUMNS(*))),
                max: max(COLUMNS(*))::VARCHAR,
                min: min(COLUMNS(*))::VARCHAR,
                approx_unique: approx_count_distinct(COLUMNS(*)),
                nulls: count(*) - count(COLUMNS(*)),
            }
    ), stacked_metrics AS (
        UNPIVOT metrics 
        ON COLUMNS(*)
    )
    SELECT value.* FROM stacked_metrics
);
```

### Execution

The `spotify_tracks` dataset is effectively renamed to `any_cte` and then summarized.

```sql
WITH any_cte AS (FROM spotify_tracks)
FROM custom_summarize();
```

The result contains one row for every column in the raw dataset, and several columns of summary statistics.

|       name       |  type   |                           max                           |             min              | approx_unique | nulls |
|------------------|---------|---------------------------------------------------------|------------------------------|--------------:|------:|
| Unnamed: 0       | BIGINT  | 113999                                                  | 0                            | 114089        | 0     |
| track_id         | VARCHAR | 7zz7iNGIWhmfFE7zlXkMma                                  | 0000vdREvCVMxbQTkS888c       | 89815         | 0     |
| artists          | VARCHAR | 龍藏Ryuzo                                               | !nvite                       | 31545         | 1     |
| album_name       | VARCHAR | 당신이 잠든 사이에 Pt. 4 Original Television Soundtrack | ! ! ! ! ! Whispers ! ! ! ! ! | 47093         | 1     |
| track_name       | VARCHAR | 행복하길 바래                                           | !I'll Be Back!               | 72745         | 1     |
| popularity       | BIGINT  | 100                                                     | 0                            | 99            | 0     |
| duration_ms      | BIGINT  | 5237295                                                 | 0                            | 50168         | 0     |
| explicit         | BOOLEAN | true                                                    | false                        | 2             | 0     |
| danceability     | DOUBLE  | 0.985                                                   | 0.0                          | 1180          | 0     |
| energy           | DOUBLE  | 1.0                                                     | 0.0                          | 2090          | 0     |
| key              | BIGINT  | 11                                                      | 0                            | 12            | 0     |
| loudness         | DOUBLE  | 4.532                                                   | -49.531                      | 19436         | 0     |
| mode             | BIGINT  | 1                                                       | 0                            | 2             | 0     |
| speechiness      | DOUBLE  | 0.965                                                   | 0.0                          | 1475          | 0     |
| acousticness     | DOUBLE  | 0.996                                                   | 0.0                          | 4976          | 0     |
| instrumentalness | DOUBLE  | 1.0                                                     | 0.0                          | 5302          | 0     |
| liveness         | DOUBLE  | 1.0                                                     | 0.0                          | 1717          | 0     |
| valence          | DOUBLE  | 0.995                                                   | 0.0                          | 1787          | 0     |
| tempo            | DOUBLE  | 243.372                                                 | 0.0                          | 46221         | 0     |
| time_signature   | BIGINT  | 5                                                       | 0                            | 5             | 0     |
| track_genre      | VARCHAR | world-music                                             | acoustic                     | 115           | 0     |

So how was this query constructed? 
Let's break down each CTE step by step.

### Step by step breakdown

#### Metrics CTE

First let's have a look at the `metrics` CTE and the shape of the data that is returned:

```sql
FROM any_cte 
SELECT 
    {
        name: first(alias(COLUMNS(*))),
        type: first(typeof(COLUMNS(*))),
        max: max(COLUMNS(*))::VARCHAR,
        min: min(COLUMNS(*))::VARCHAR,
        approx_unique: approx_count_distinct(COLUMNS(*)),
        nulls: count(*) - count(COLUMNS(*)),
    };
```

| main.struct_pack("name" := first(alias(subset."Unnamed: 0")), ... | main.struct_pack("name" := first(alias(subset.track_id)), ... | ... | main.struct_pack("name" := first(alias(subset.time_signature)), ... | main.struct_pack("name" := first(alias(subset.track_genre)), ... |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| {'name': Unnamed: 0, 'type': BIGINT, 'max': 113999, 'min': 0, 'approx_unique': 114089, 'nulls': 0}                                                                                                                                                                                                                                   | {'name': track_id, 'type': VARCHAR, 'max': 7zz7iNGIWhmfFE7zlXkMma, 'min': 0000vdREvCVMxbQTkS888c, 'approx_unique': 89815, 'nulls': 0}                                                                                                                                                                        | ... | {'name': time_signature, 'type': BIGINT, 'max': 5, 'min': 0, 'approx_unique': 5, 'nulls': 0}                                                                                                                                                                                                                                                  | {'name': track_genre, 'type': VARCHAR, 'max': world-music, 'min': acoustic, 'approx_unique': 115, 'nulls': 0}                                                                                                                                                                                                                  |


This intermediate result maintains the same number of columns as the original dataset, but only returns a single row of summary statistics.
The names of the columns are truncated due to their length.
The default naming of `COLUMNS` expressions will be improved in DuckDB 0.10.1, so names will be much cleaner!

The data in each column is organized into a `STRUCT` of key-value pairs. 
You can also see that a clean name of the original column is stored within the `STRUCT` thanks to the use of the `alias` function.
While we have calculated the summary statistics, the format of those statistics is difficult to visually interpret. 

The query achieves this structure using the `COLUMNS(*)` expression to apply multiple summary metrics to all columns, and the `{...}` syntax to create a `STRUCT`.
The keys of the struct represent the names of the metrics (and what we want to use as the column names in the final result). 
We use this approach since we want to transpose the columns to rows and then split the summary metrics into their own columns.

#### Stacked_metrics CTE

Next, the data is unpivoted to reshape the table from one row and multiple columns to two columns and multiple rows. 

```sql
UNPIVOT metrics 
ON COLUMNS(*);
```

|           name           |                                                                           value                                                                            |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| main.struct_pack("name" := first(alias(spotify_tracks."Unnamed: 0")), ... | {'name': Unnamed: 0, 'type': BIGINT, 'max': 113999, 'min': 0, 'approx_unique': 114089, 'nulls': 0}                                                                             |
| main.struct_pack("name" := first(alias(spotify_tracks.track_id)), ... | {'name': track_id, 'type': VARCHAR, 'max': 7zz7iNGIWhmfFE7zlXkMma, 'min': 0000vdREvCVMxbQTkS888c, 'approx_unique': 89815, 'nulls': 0}                                          |
|           ...            |                                                                            ...                                                                             |
| main.struct_pack("name" := first(alias(spotify_tracks.time_signature)), ... | {'name': time_signature, 'type': BIGINT, 'max': 5, 'min': 0, 'approx_unique': 5, 'nulls': 0}                                                                                   |
| main.struct_pack("name" := first(alias(spotify_tracks.track_genre)), ... | {'name': track_genre, 'type': VARCHAR, 'max': world-music, 'min': acoustic, 'approx_unique': 115, 'nulls': 0}                                                                  |

By unpivoting on `COLUMNS(*)`, we take all columns and pivot them downward into two columns: one for the auto-generated `name` of the column, and one for the `value` that was within that column.

#### Return the results

The final step is the most gymnastics-like portion of this query.
We explode the `value` column's struct format so that each key becomes its own column using the [`STRUCT.*` syntax](/docs/sql/data_types/struct#struct).
This is another way to make a query less reliant on column names – the split occurs automatically based on the keys in the struct.

```sql
SELECT value.*
FROM stacked_metrics;
```

We have now split apart the data into multiple columns, so the summary metrics are nice and interpretable.

|       name       |  type   |                           max                           |             min              | approx_unique | nulls |
|------------------|---------|---------------------------------------------------------|------------------------------|--------------:|------:|
| Unnamed: 0       | BIGINT  | 113999                                                  | 0                            | 114089        | 0     |
| track_id         | VARCHAR | 7zz7iNGIWhmfFE7zlXkMma                                  | 0000vdREvCVMxbQTkS888c       | 89815         | 0     |
| artists          | VARCHAR | 龍藏Ryuzo                                               | !nvite                       | 31545         | 1     |
| album_name       | VARCHAR | 당신이 잠든 사이에 Pt. 4 Original Television Soundtrack | ! ! ! ! ! Whispers ! ! ! ! ! | 47093         | 1     |
| track_name       | VARCHAR | 행복하길 바래                                           | !I'll Be Back!               | 72745         | 1     |
| popularity       | BIGINT  | 100                                                     | 0                            | 99            | 0     |
| duration_ms      | BIGINT  | 5237295                                                 | 0                            | 50168         | 0     |
| explicit         | BOOLEAN | true                                                    | false                        | 2             | 0     |
| danceability     | DOUBLE  | 0.985                                                   | 0.0                          | 1180          | 0     |
| energy           | DOUBLE  | 1.0                                                     | 0.0                          | 2090          | 0     |
| key              | BIGINT  | 11                                                      | 0                            | 12            | 0     |
| loudness         | DOUBLE  | 4.532                                                   | -49.531                      | 19436         | 0     |
| mode             | BIGINT  | 1                                                       | 0                            | 2             | 0     |
| speechiness      | DOUBLE  | 0.965                                                   | 0.0                          | 1475          | 0     |
| acousticness     | DOUBLE  | 0.996                                                   | 0.0                          | 4976          | 0     |
| instrumentalness | DOUBLE  | 1.0                                                     | 0.0                          | 5302          | 0     |
| liveness         | DOUBLE  | 1.0                                                     | 0.0                          | 1717          | 0     |
| valence          | DOUBLE  | 0.995                                                   | 0.0                          | 1787          | 0     |
| tempo            | DOUBLE  | 243.372                                                 | 0.0                          | 46221         | 0     |
| time_signature   | BIGINT  | 5                                                       | 0                            | 5             | 0     |
| track_genre      | VARCHAR | world-music                                             | acoustic                     | 115           | 0     |


## Conclusion

We have shown that it is now possible to build reusable SQL macros in a highly flexible way. 
You can now build a macro that:
* Operates on any dataset
* Selects any columns
* Groups by any columns
* Aggregates any number of columns with any function.

Phew! 

Along the way we have covered some useful tricks to have in your toolbox:
* Applying a macro to any dataset using a CTE
* Selecting a dynamic list of columns by combining the `COLUMNS` expression with a lambda and the `list_contains` function
* Passing in an aggregate function as a string using `list_aggregate`
* Applying any custom aggregation function within a macro
* Making list parameters optional using `OR len(list_parameter) = 0`
* Using the `alias` function with a `COLUMNS` expression to store the original name of all columns
* Summarizing all columns and then transposing that summary using `UNPIVOT` and `STRUCT.*`

The combination of these friendly SQL features is more powerful than using any one individually.
We hope that we have inspired you to take your SQL to new limits!

As always, we welcome your feedback and suggestions. 
We also have more flexibility in mind that will be demonstrated in future posts.
Please share the times you have stretched SQL in imaginative ways!

Happy analyzing!

---
layout: post
title: "Creating a SQL-Only Extension for Excel-Style Pivoting in DuckDB"
author: "Alex Monahan"
excerpt: "Now you can easily create sharable extensions using only SQL MACROs that can apply to any table and any columns. We demonstrate the power of this capability with the pivot_table extension that provides Excel-style pivoting"
---
<!-- 
1015

The vision
    Shareable helper libraries, built entirely in SQL
    Usable across all client languages supported by DuckDB
    Now with version 1.1, DuckDB supports dynamic table names as well as dynamic column names
        so any TABLE FUNCTION can be used on any table
    A powerful way to contribute to the DuckDB community if you are a SQL expert and not a C++ expert
    Allows for direct parameterization from your host language to ensure safety
    This can scale up to significant complexity (and therefore significant community value!), as we will demonstrate with the pivot_table extension

Capabilities of the pivot_table extension
    The pivot_table extension supports advanced pivoting functionality that was previously only available in spreadsheets, dataframe libraries, or custom host language functions.
    Supports the Excel pivoting API: values, rows, columns, filters
    It accepts arbitrary combinations of these parameters and can handle as many inputs as desired
    Plus advanced options like subtotals and grand totals
    If multiple values are in use, there is an option to create a separate column per value or a separate row per value

    Why was this hard for SQL in the past? The query syntax used to handle groupings and the syntax used to handle pivots is very different, and the Excel API supports both use cases.
        If no columns parameter is supplied, then a group by should be used. 
        Otherwise, a PIVOT is required

Operate on any table with query_table

Create SQL dynamically with query 
    Since this is really just operating on strings, we can modularize this
    It is also safe since it does not allow DDL statements (CREATE, UPDATE, and DELETE are disallowed)

Do valuable dynamic work thanks to list lambdas
    One way to operate on user-specified columns

Operate on user-specified columns with the columns expression

How to create your own
    Extension template
    Cover the exact C++ syntax so that it isn't intimidating

The pivot_table example
    Maybe a diagram of the various functions in use and how they call each other?
        Maybe just a list or table instead, with a quick description
        Start with the broadest function (root function)
    

-->


## The Power of SQL-Only Extensions

SQL is not a new language.
As a result, it has historically been missing some of the modern luxuries we take for granted.
With version 1.1, DuckDB has launched community extensions, bringing the incredible power of a package manager to the SQL language.
One goal for these extensions is to enable C++ libraries to be accessible through SQL across all of the languages with a DuckDB library.
For extension builders, compilation and distribution are much easier.
For the user community, installation is as simple as a single command:

```sql
INSTALL pivot_table FROM community;
```

However, not all of us are C++ developers! 
Can we, as a SQL community, build up a set of SQL helper functions?
What would it take to build these extensions with *just SQL*? 

### Reusability

Traditionally, SQL is highly customized to the schema of the database on which it was written. 
Can we make it reusable?
Some techniques for reusability were discussed in the SQL Gymnasics post, but now we can go even further.
<!-- TODO: add the link -->
With version 1.1, DuckDB's world-class friendly SQL dialect makes it possible to create MACROs that can be applied:
* To any tables
* On any columns
* Using any functions
The new ability to work on any tables is thanks to the `query` and `query_table` functions!

### Community Extensions as a Central Repository

Traditionally, there has been no central repository for SQL functions across databases, let alone across companies!
DuckDB's community extensions can be that knowledge base.
If you are a DuckDB fan and a SQL user, you can share your expertise back to the community with an extension.
This post will show you how!
No C++ knowledge is needed - just a little bit of copy/paste and GitHub actions handles all the compilation. 
If I can do it, you can do it!

### Powerful SQL

All that said, just how valuable can a SQL `MACRO` be? 
Can we do more than make small snippets?
I'll make the case that you can do quite complex and powerful operations in DuckDB SQL using the `pivot_table` extension as an example.

So, we now have all 3 ingredients we will need: a central package manager, reusable `MACRO`s, and enough syntactic flexibility to do valuable work.

## Capabilities of the `pivot_table` Extension

The `pivot_table` extension supports advanced pivoting functionality that was previously only available in spreadsheets, dataframe libraries, or custom host language functions.
It uses the Excel pivoting API: `values`, `rows`, `columns`, and `filters`.
It can handle 0 or more of each of those parameters.
However, not only that, but it supports `subtotals` and `grand_totals`.
If multiple `values` are passed in, the `values_axis` parameter allows the user to choose if each value should get its own column or its own row.

> Note The only missing Excel feature I am aware of is columnar subtotals, but not even Pandas supports that!
> And we are officially open to contributions now... :-)

Why is this a good example of how DuckDB moves beyond traditional SQL?
The Excel pivoting API requires dramatically different SQL syntax depending on which parameters are in use.
If no `columns` are pivoted outward, a `GROUP BY` is all that is needed.
However, once `columns` are involved, a `PIVOT` is required.

This function can operate on one or more `table_names` that are passed in as a parameter.
Any set of tables will first be vertically stacked and then pivoted.

## Example Using `pivot_table`

<details markdown='1'>
<summary markdown='span'>
    First we will create an example data table. We are a duck product disributor.
</summary>

```sql
CREATE OR REPLACE TABLE business_metrics (
    product_line VARCHAR, product VARCHAR, year INTEGER, quarter VARCHAR, revenue integer, cost integer
);
INSERT INTO business_metrics VALUES
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q1', 100, 100),
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q2', 200, 100),
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q3', 300, 100),
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q4', 400, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q1', 500, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q2', 600, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q3', 700, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q4', 800, 100),

    ('Duck Duds', 'Duck suits', 2022, 'Q1', 10, 10),
    ('Duck Duds', 'Duck suits', 2022, 'Q2', 20, 10),
    ('Duck Duds', 'Duck suits', 2022, 'Q3', 30, 10),
    ('Duck Duds', 'Duck suits', 2022, 'Q4', 40, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q1', 50, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q2', 60, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q3', 70, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q4', 80, 10),

    ('Duck Duds', 'Duck neckties', 2022, 'Q1', 1, 1),
    ('Duck Duds', 'Duck neckties', 2022, 'Q2', 2, 1),
    ('Duck Duds', 'Duck neckties', 2022, 'Q3', 3, 1),
    ('Duck Duds', 'Duck neckties', 2022, 'Q4', 4, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q1', 5, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q2', 6, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q3', 7, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q4', 8, 1),
;

FROM business_metrics;
```
</details>

|     product_line     |    product    | year | quarter | revenue | cost |
|----------------------|---------------|-----:|---------|--------:|-----:|
| Waterfowl watercraft | Duck boats    | 2022 | Q1      | 100     | 100  |
| Waterfowl watercraft | Duck boats    | 2022 | Q2      | 200     | 100  |
| Waterfowl watercraft | Duck boats    | 2022 | Q3      | 300     | 100  |
| Waterfowl watercraft | Duck boats    | 2022 | Q4      | 400     | 100  |
| Waterfowl watercraft | Duck boats    | 2023 | Q1      | 500     | 100  |
| Waterfowl watercraft | Duck boats    | 2023 | Q2      | 600     | 100  |
| Waterfowl watercraft | Duck boats    | 2023 | Q3      | 700     | 100  |
| Waterfowl watercraft | Duck boats    | 2023 | Q4      | 800     | 100  |
| Duck Duds            | Duck suits    | 2022 | Q1      | 10      | 10   |
| Duck Duds            | Duck suits    | 2022 | Q2      | 20      | 10   |
| Duck Duds            | Duck suits    | 2022 | Q3      | 30      | 10   |
| Duck Duds            | Duck suits    | 2022 | Q4      | 40      | 10   |
| Duck Duds            | Duck suits    | 2023 | Q1      | 50      | 10   |
| Duck Duds            | Duck suits    | 2023 | Q2      | 60      | 10   |
| Duck Duds            | Duck suits    | 2023 | Q3      | 70      | 10   |
| Duck Duds            | Duck suits    | 2023 | Q4      | 80      | 10   |
| Duck Duds            | Duck neckties | 2022 | Q1      | 1       | 1    |
| Duck Duds            | Duck neckties | 2022 | Q2      | 2       | 1    |
| Duck Duds            | Duck neckties | 2022 | Q3      | 3       | 1    |
| Duck Duds            | Duck neckties | 2022 | Q4      | 4       | 1    |
| Duck Duds            | Duck neckties | 2023 | Q1      | 5       | 1    |
| Duck Duds            | Duck neckties | 2023 | Q2      | 6       | 1    |
| Duck Duds            | Duck neckties | 2023 | Q3      | 7       | 1    |
| Duck Duds            | Duck neckties | 2023 | Q4      | 8       | 1    |

Now we can build pivot tables like the one below. 
There is a little bit of boilerplate required, and the details of how this works are explained later in the post.

```sql
DROP TYPE IF EXISTS columns_parameter_enum;

CREATE TYPE columns_parameter_enum AS ENUM (
    FROM build_my_enum(['business_metrics'], ['year', 'quarter'], [])
);

FROM pivot_table(['business_metrics'],          -- table_names
                 ['sum(revenue)', 'sum(cost)'], -- values
                 ['product_line', 'product'],   -- rows
                 ['year', 'quarter'],           -- columns
                 [],                            -- filters
                 subtotals:=1,
                 grand_totals:=1,
                 values_axis:='rows'
                 );
```

|     product_line     |    product    | value_names  | 2022_Q1 | 2022_Q2 | 2022_Q3 | 2022_Q4 | 2023_Q1 | 2023_Q2 | 2023_Q3 | 2023_Q4 |
|----------------------|---------------|--------------|---------|---------|---------|---------|---------|---------|---------|---------|
| Duck Duds            | Duck neckties | sum(cost)    | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       |
| Duck Duds            | Duck neckties | sum(revenue) | 1       | 2       | 3       | 4       | 5       | 6       | 7       | 8       |
| Duck Duds            | Duck suits    | sum(cost)    | 10      | 10      | 10      | 10      | 10      | 10      | 10      | 10      |
| Duck Duds            | Duck suits    | sum(revenue) | 10      | 20      | 30      | 40      | 50      | 60      | 70      | 80      |
| Duck Duds            | Subtotal      | sum(cost)    | 11      | 11      | 11      | 11      | 11      | 11      | 11      | 11      |
| Duck Duds            | Subtotal      | sum(revenue) | 11      | 22      | 33      | 44      | 55      | 66      | 77      | 88      |
| Waterfowl watercraft | Duck boats    | sum(cost)    | 100     | 100     | 100     | 100     | 100     | 100     | 100     | 100     |
| Waterfowl watercraft | Duck boats    | sum(revenue) | 100     | 200     | 300     | 400     | 500     | 600     | 700     | 800     |
| Waterfowl watercraft | Subtotal      | sum(cost)    | 100     | 100     | 100     | 100     | 100     | 100     | 100     | 100     |
| Waterfowl watercraft | Subtotal      | sum(revenue) | 100     | 200     | 300     | 400     | 500     | 600     | 700     | 800     |
| Grand Total          | Grand Total   | sum(cost)    | 111     | 111     | 111     | 111     | 111     | 111     | 111     | 111     |
| Grand Total          | Grand Total   | sum(revenue) | 111     | 222     | 333     | 444     | 555     | 666     | 777     | 888     |

## Create Your Own SQL Extension

Let's walk through the steps to creating your own SQL-only extension.

### Writing the Extension

#### Extension Setup

The first step is to create your own GitHub repo from the [DuckDB Extension Template](https://github.com/duckdb/extension-template) by clicking `Use this template`. 

Then clone your new repository onto your local machine using the terminal:
```sh
git clone --recurse-submodules https://github.com/<you>/<your-new-extension-repo>.git
```
Note that `--recurse-submodules` will ensure DuckDB is pulled which is required to build the extension.

Next, replace the name of the example extension with the name of your extension in all the right places by running the Python script below.

> Note If you don't have Python installed, head to [python.org](https://python.org) and follow those instructions.
> This script doesn't require any libraries, so Python is all you need! (No need to set up any environments)

```python
python3 ./scripts/bootstrap-template.py <extension_name_you_want>
```

#### Initial Extension Test

At this point, you can follow the directions in the README to build and test locally if you would like.
However, even easier, you can simply commit your changes to git and push them to GitHub, and GitHub actions can do the compilation for you!

> Note The instructions are not written for a Windows audience, so we recommend GitHub Actions in that case!

```sh
git add -A
git commit -m "Initial commit of my SQL extension!"
git push
```


<!-- Screenshot of GitHub actions and looking at the test results? -->

#### Write Your SQL Macros

It it likely a bit faster to iterate if you test our your macros directly in DuckDB. 
The example we will use demonstrates how to pull a dynamic set of columns from a dynamic table name.

```sql
CREATE OR REPLACE MACRO select_distinct_columns_from_table(table_name, columns_list) AS TABLE (
    SELECT DISTINCT
        COLUMNS(column_name -> list_contains(columns_list, column_name))
    FROM query_table(table_name)
);
```

#### Add SQL Macros

Technically, this is the C++ part, but we are going to do some copy/paste and use GitHub actions for compiling so it won't feel that way!

DuckDB supports both scalar and table macros, and they have slightly different syntax.
The extension template has an example for each (and code comments too!) inside the file named `<your_extension_name>.cpp`.
Let's add a table macro here since it is the more complex one.
We will copy the example and modify it!

```cpp
static const DefaultTableMacro <your_extension_name>_table_macros[] = {
	{DEFAULT_SCHEMA, "times_two_table", {"x", nullptr}, {{"two", "2"}, {nullptr, nullptr}},  R"(SELECT x * two as output_column;)"},
	{
        DEFAULT_SCHEMA, // Leave the schema as the default
        "select_distinct_columns_from_table", // Function name
        {"table_name", "columns_list", nullptr}, // Parameters
        {{nullptr, nullptr}}, // Optional parameter names and values (we choose not to have any here)
        // The SQL text inside of your SQL Macro, wrapped in R"( )", which is a raw string in C++
        R"(
            SELECT DISTINCT
                COLUMNS(column_name -> list_contains(columns_list, column_name))
            FROM query_table(table_name)
        )"
    },
	{nullptr, nullptr, {nullptr}, {{nullptr, nullptr}}, nullptr}
	};
```

That's it! 
All we had to provide were the name of the function, the names of the parameters, and the text of our SQL `MACRO`.

Now, just add, commit, and push your changes to GitHub like before, and GitHub actions will compile your extension and upload it to AWS S3!

### Testing the Extension

For testing purposes, we can use any DuckDB client, but this example uses the CLI.

> Note We need to run DuckDB with the -unsigned flag since our extension hasn't been signed yet.
> It will be signed after we upload it to the community repository

```shell
duckdb -unsigned
```

Next, run the SQL command below to point DuckDB's extension loader to the S3 bucket that was automatically created for you.

```sql
SET custom_extension_repository='bucket.s3.eu-west-1.amazonaws.com/<your_extension_name>/latest';
```
Note that the `/latest` path will allow you to install the latest extension version available for your current version of
DuckDB. To specify a specific version, you can pass the version instead.

After running these steps, you can install and load your extension using the regular INSTALL/LOAD commands in DuckDB:
```sql
INSTALL <your_extension_name>;
LOAD <your_extension_name>;

SELECT *
FROM select_distinct_columns_from_table('business_metrics', ['product_line', 'product']);
```

|     product_line     |    product    |
|----------------------|---------------|
| Waterfowl watercraft | Duck boats    |
| Duck Duds            | Duck neckties |
| Duck Duds            | Duck suits    |


### Uploading to the Community Extensions Repository

Once you are happy with your extension, it's time to share it with the DuckDB community!
Follow the steps in [the Community Extensions post]({% post_url 2024-07-05-community-extensions %}#developer-experience).
A summary of those steps is:

1. Send a PR with a metadata file `description.yml` contains the description of the extension. For example:

   ```yaml
   extension:
     name: h3
     description: Hierarchical hexagonal indexing for geospatial data
     version: 1.0.0
     language: C++
     build: cmake
     license: Apache-2.0
     maintainers:
       - isaacbrodsky

   repo:
     github: isaacbrodsky/h3-duckdb
     ref: 3c8a5358e42ab8d11e0253c70f7cc7d37781b2ef
   ```

2. Wait for approval from the maintainers!




<!-- 

Operate on any table with query_table

Create SQL dynamically with query 
    Since this is really just operating on strings, we can modularize this
    It is also safe since it does not allow DDL statements (CREATE, UPDATE, and DELETE are disallowed)

Do valuable dynamic work thanks to list lambdas
    One way to operate on user-specified columns

Operate on user-specified columns with the columns expression

How to create your own
    Extension template
    Cover the exact C++ syntax so that it isn't intimidating

The pivot_table example
    Maybe a diagram of the various functions in use and how they call each other?
        Maybe just a list or table instead, with a quick description
        Start with the broadest function (root function) -->
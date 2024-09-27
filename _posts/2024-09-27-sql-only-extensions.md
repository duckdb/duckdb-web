---
layout: post
title: "Creating a SQL-Only Extension for Excel-Style Pivoting in DuckDB"
author: "Alex Monahan"
excerpt: "Easily create sharable extensions using only SQL macros that can apply to any table and any columns. We demonstrate the power of this capability with the pivot_table extension that provides Excel-style pivoting."
---

## The Power of SQL-Only Extensions

SQL is not a new language.
As a result, it has historically been missing some of the modern luxuries we take for granted.
With version 1.1, DuckDB has launched community extensions, bringing the incredible power of a package manager to the SQL language.
A bold goal of ours is for DuckDB to become a convenient way to wrap any C++ library, much the way that Python does today, but across any language with a DuckDB client.

For extension builders, compilation and distribution are much easier.
For the user community, installation is as simple as two commands:

```sql
INSTALL pivot_table FROM community;
LOAD pivot_table;
```

The extension can then be used in any query through SQL functions.

However, **not all of us are C++ developers**!
Can we, as a SQL community, build up a set of SQL helper functions?
What would it take to build these extensions with *just SQL*?

### Reusability

Traditionally, SQL is highly customized to the schema of the database on which it was written.
Can we make it reusable?
Some techniques for reusability were discussed in the [SQL Gymnasics post]({% post_url 2024-03-01-sql-gymnastics %}), but now we can go even further.
With version 1.1, DuckDB's world-class friendly SQL dialect makes it possible to create macros that can be applied:

* To any tables
* On any columns
* Using any functions

The new ability to work **on any tables** is thanks to the [`query` and `query_table` functions]({% post_url 2024-09-09-announcing-duckdb-110 %}#query-and-query_table-functions)!
The `query` function is a safe way to execute `SELECT` statements defined by SQL strings, while `query_table` is a way to make a `FROM` clause pull from multiple tables at once.
They are very powerful when used in combination with other friendly SQL features like the `COLUMNS` expression and  `LIST` lambda functions.

### Community Extensions as a Central Repository

Traditionally, there has been no central repository for SQL functions across databases, let alone across companies!
DuckDB's community extensions can be that knowledge base.
DuckDB extensions can be used across all languages with a DuckDB client, including Python, NodeJS, Java, Rust, Go, and even WebAssembly (Wasm)!

If you are a DuckDB fan and a SQL user, you can share your expertise back to the community with an extension.
This post will show you how!
No C++ knowledge is needed - just a little bit of copy/paste and GitHub Actions handles all the compilation. 
If I can do it, you can do it!

### Powerful SQL

All that said, just how valuable can a SQL `MACRO` be?
Can we do more than make small snippets?
I'll make the case that you can do quite complex and powerful operations in DuckDB SQL using the `pivot_table` extension as an example.
The `pivot_table` function allows for Excel-style pivots, including `subtotals`, `grand_totals`, and more.
It is also very similar to the Pandas `pivot_table` function, but with all the scalability and speed benefits of DuckDB.
It contains over **250 tests**, so it is intended to be useful beyond just an example!

To achieve this level of flexibility, the `pivot_table` extension uses many friendly and advanced SQL features:

* The [`query` function]({% post_url 2024-09-09-announcing-duckdb-110 %}#query-and-query_table-functions) to execute a SQL string
* The [`query_table` function]({% post_url 2024-09-09-announcing-duckdb-110 %}#query-and-query_table-functions) to query a list of tables
* The [`COLUMNS` expression]({% link docs/sql/expressions/star.md %}#columns-expression) to select a dynamic list of columns
* [List lambda functions]({% link docs/sql/functions/lambda.md %}) to build up the SQL statement passed into `query`
    * [`list_transform`]({% link docs/sql/functions/lambda.md %}#list_transformlist-lambda) for string manipulation like quoting
    * [`list_reduce`]({% link docs/sql/functions/lambda.md %}#list_reducelist-lambda) to concatenate strings together
    * [`list_aggregate`]({% link docs/sql/functions/list.md %}#list_aggregatelist-name) to sum multiple columns and identify subtotal and grand total rows
* [Bracket notation for string slicing]({% link docs/sql/functions/char.md %}#stringbeginend)
* [`UNION ALL BY NAME`]({% link docs/sql/query_syntax/setops.md %}#union-all-by-name) to stack data by column name for subtotals and grand totals
* [`SELECT * REPLACE`]({% link docs/sql/expressions/star.md %}#replace-clause) to dynamically clean up subtotal columns
* [`SELECT * EXCLUDE`]({% link docs/sql/expressions/star.md %}#exclude-clause) to remove internally generated columns from the final result
* [`GROUPING SETS` and `ROLLUP`]({% link docs/sql/query_syntax/grouping_sets.md %}) to generate subtotals and grand totals
* [`UNNEST`]({% link docs/sql/query_syntax/unnest.md %}) to convert lists into separate rows for `values_axis := 'rows'`
* [`MACRO`s]({% link docs/sql/statements/create_macro.md %}) to modularize the code
* [`ORDER BY ALL`]({% link docs/sql/query_syntax/orderby.md %}#order-by-all) to order the result dynamically
* [`ENUM`s]({% link docs/sql/statements/create_type.md %}) to determine what columns to pivot horizontally
* And of course the [`PIVOT` function]({% link docs/sql/statements/pivot.md %}) for horizontal pivoting!

DuckDB's innovative syntax makes this extension possible!

So, we now have all 3 ingredients we will need: a central package manager, reusable macros, and enough syntactic flexibility to do valuable work.

## Create Your Own SQL Extension

Let's walk through the steps to creating your own SQL-only extension.

### Writing the Extension

#### Extension Setup

The first step is to create your own GitHub repo from the [DuckDB Extension Template for SQL](https://github.com/duckdb/extension-template-sql) by clicking `Use this template`.

Then clone your new repository onto your local machine using the terminal:

```batch
git clone --recurse-submodules https://github.com/<you>/<your-new-extension-repo>.git
```

Note that `--recurse-submodules` will ensure DuckDB is pulled which is required to build the extension.

Next, replace the name of the example extension with the name of your extension in all the right places by running the Python script below.

> Note If you don't have Python installed, head to [python.org](https://python.org) and follow those instructions.
> This script doesn't require any libraries, so Python is all you need! (No need to set up any environments.)

```python
python3 ./scripts/bootstrap-template.py <extension_name_you_want>
```

#### Initial Extension Test

At this point, you can follow the directions in the README to build and test locally if you would like.
However, even easier, you can simply commit your changes to git and push them to GitHub, and GitHub Actions can do the compilation for you!
GitHub Actions will also run tests on your extension to validate it is working properly.

> Note The instructions are not written for a Windows audience, so we recommend GitHub Actions in that case!

```batch
git add -A
git commit -m "Initial commit of my SQL extension!"
git push
```

#### Write Your SQL Macros

It it likely a bit faster to iterate if you test your macros directly in DuckDB. 
After you have written your SQL, we will move it into the extension.
The example we will use demonstrates how to pull a dynamic set of columns from a dynamic table name (or a view name!).

```sql
CREATE OR REPLACE MACRO select_distinct_columns_from_table(table_name, columns_list) AS TABLE (
    SELECT DISTINCT
        COLUMNS(column_name -> list_contains(columns_list, column_name))
    FROM query_table(table_name)
    ORDER BY ALL
);

FROM select_distinct_columns_from_table('duckdb_types', ['type_category']);
```

| type_category |
|---------------|
| BOOLEAN       |
| COMPOSITE     |
| DATETIME      |
| NUMERIC       |
| STRING        |
| NULL          |

#### Add SQL Macros

Technically, this is the C++ part, but we are going to do some copy/paste and use GitHub Actions for compiling so it won't feel that way!

DuckDB supports both scalar and table macros, and they have slightly different syntax.
The extension template has an example for each (and code comments too!) inside the file named `<your_extension_name>.cpp`.
Let's add a table macro here since it is the more complex one.
We will copy the example and modify it!

{% raw %}
```cpp
static const DefaultTableMacro <your_extension_name>_table_macros[] = {
	{DEFAULT_SCHEMA, "times_two_table", {"x", nullptr}, {{"two", "2"}, {nullptr, nullptr}}, R"(SELECT x * two as output_column;)"},
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
            ORDER BY ALL
        )"
    },
	{nullptr, nullptr, {nullptr}, {{nullptr, nullptr}}, nullptr}
	};
```
{% endraw %}

That's it!
All we had to provide were the name of the function, the names of the parameters, and the text of our SQL macro.

### Testing the Extension

We also recommend adding some tests for your extension to the `<your_extension_name>.test` file.
This uses [sqllogictest]({% link docs/dev/sqllogictest/intro.md %}) to test with just SQL!
Let's add the example from above.

> Note In sqllogictest, `query I` indicates that there will be 1 column in the result.
> We then add `----` and the resultset in tab separated format with no column names.

```sql
query I
FROM select_distinct_columns_from_table('duckdb_types', ['type_category']);
----
BOOLEAN
COMPOSITE
DATETIME
NUMERIC
STRING
NULL
```

Now, just add, commit, and push your changes to GitHub like before, and GitHub Actions will compile your extension and test it!

If you would like to do further ad-hoc testing of your extension, you can download the extension from your GitHub Actions run's artifacts and then [install it locally using these steps]({% link docs/extensions/overview.md %}#unsigned-extensions).

### Uploading to the Community Extensions Repository

Once you are happy with your extension, it's time to share it with the DuckDB community!
Follow the steps in [the Community Extensions post]({% post_url 2024-07-05-community-extensions %}#developer-experience).
A summary of those steps is:

1. Send a PR with a metadata file `description.yml` that contains the description of the extension. For example, the [`h3` Community Extension](https://community-extensions.duckdb.org/extensions/h3.html) uses the following YAML configuration:

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

2. Wait for approval from the maintainers

And there you have it!
You have created a shareable DuckDB Community Extension.
Now let's have a look at the `pivot_table` extension as an example of just how powerful a SQL-only extension can be.

## Capabilities of the `pivot_table` Extension

The `pivot_table` extension supports advanced pivoting functionality that was previously only available in spreadsheets, dataframe libraries, or custom host language functions.
It uses the Excel pivoting API: `values`, `rows`, `columns`, and `filters` - handling 0 or more of each of those parameters.
However, not only that, but it supports `subtotals` and `grand_totals`.
If multiple `values` are passed in, the `values_axis` parameter allows the user to choose if each value should get its own column or its own row.

Why is this a good example of how DuckDB moves beyond traditional SQL?
The Excel pivoting API requires dramatically different SQL syntax depending on which parameters are in use.
If no `columns` are pivoted outward, a `GROUP BY` is all that is needed.
However, once `columns` are involved, a `PIVOT` is required.

This function can operate on one or more `table_names` that are passed in as a parameter.
Any set of tables (or views!) will first be vertically stacked and then pivoted.

## Example Using `pivot_table`

<!-- markdownlint-disable MD034 -->

[Check out a live example using the extension in the DuckDB Wasm shell here](https://shell.duckdb.org/#queries=v0,CREATE-OR-REPLACE-TABLE-business_metrics-(-----product_line-VARCHAR%2C-product-VARCHAR%2C-year-INTEGER%2C-quarter-VARCHAR%2C-revenue-integer%2C-cost-integer-)~,INSERT-INTO-business_metrics-VALUES-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2022%2C-'Q1'%2C-100%2C-100)%2C-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2022%2C-'Q2'%2C-200%2C-100)%2C-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2022%2C-'Q3'%2C-300%2C-100)%2C-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2022%2C-'Q4'%2C-400%2C-100)%2C-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2023%2C-'Q1'%2C-500%2C-100)%2C-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2023%2C-'Q2'%2C-600%2C-100)%2C-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2023%2C-'Q3'%2C-700%2C-100)%2C-----('Waterfowl-watercraft'%2C-'Duck-boats'%2C-2023%2C-'Q4'%2C-800%2C-100)%2C------('Duck-Duds'%2C-'Duck-suits'%2C-2022%2C-'Q1'%2C-10%2C-10)%2C-----('Duck-Duds'%2C-'Duck-suits'%2C-2022%2C-'Q2'%2C-20%2C-10)%2C-----('Duck-Duds'%2C-'Duck-suits'%2C-2022%2C-'Q3'%2C-30%2C-10)%2C-----('Duck-Duds'%2C-'Duck-suits'%2C-2022%2C-'Q4'%2C-40%2C-10)%2C-----('Duck-Duds'%2C-'Duck-suits'%2C-2023%2C-'Q1'%2C-50%2C-10)%2C-----('Duck-Duds'%2C-'Duck-suits'%2C-2023%2C-'Q2'%2C-60%2C-10)%2C-----('Duck-Duds'%2C-'Duck-suits'%2C-2023%2C-'Q3'%2C-70%2C-10)%2C-----('Duck-Duds'%2C-'Duck-suits'%2C-2023%2C-'Q4'%2C-80%2C-10)%2C------('Duck-Duds'%2C-'Duck-neckties'%2C-2022%2C-'Q1'%2C-1%2C-1)%2C-----('Duck-Duds'%2C-'Duck-neckties'%2C-2022%2C-'Q2'%2C-2%2C-1)%2C-----('Duck-Duds'%2C-'Duck-neckties'%2C-2022%2C-'Q3'%2C-3%2C-1)%2C-----('Duck-Duds'%2C-'Duck-neckties'%2C-2022%2C-'Q4'%2C-4%2C-1)%2C-----('Duck-Duds'%2C-'Duck-neckties'%2C-2023%2C-'Q1'%2C-5%2C-1)%2C-----('Duck-Duds'%2C-'Duck-neckties'%2C-2023%2C-'Q2'%2C-6%2C-1)%2C-----('Duck-Duds'%2C-'Duck-neckties'%2C-2023%2C-'Q3'%2C-7%2C-1)%2C-----('Duck-Duds'%2C-'Duck-neckties'%2C-2023%2C-'Q4'%2C-8%2C-1)%2C~,FROM-business_metrics~,INSTALL-pivot_table-from-community~,LOAD-'https%3A%2F%2Fcommunity extensions.duckdb.org%2Fv1.1.1%2Fwasm_eh%2Fpivot_table.duckdb_extension.wasm'~,DROP-TYPE-IF-EXISTS-columns_parameter_enum~,CREATE-TYPE-columns_parameter_enum-AS-ENUM-(FROM-build_my_enum(['business_metrics']%2C-['year'%2C-'quarter']%2C-[]))~,FROM-pivot_table(['business_metrics']%2C['sum(revenue)'%2C-'sum(cost)']%2C-['product_line'%2C-'product']%2C-['year'%2C-'quarter']%2C-[]%2C-subtotals-%3A%3D-1%2C-grand_totals-%3A%3D-1%2C-values_axis-%3A%3D-'rows')~)!

<!-- markdownlint-enable MD034 -->

<details markdown='1'>
<summary markdown='span'>
    First we will create an example data table. We are a duck product distributor, and we are tracking our fowl finances.
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

Next, we install the extension from the community repository:

```sql
INSTALL pivot_table FROM community;
LOAD pivot_table;
```

Now we can build pivot tables like the one below. 
There is a little bit of boilerplate required, and the details of how this works will be explained shortly.

```sql
DROP TYPE IF EXISTS columns_parameter_enum;

CREATE TYPE columns_parameter_enum AS ENUM (
    FROM build_my_enum(['business_metrics'],    -- table_names
                       ['year', 'quarter'],     -- columns
                       [])                      -- filters
);

FROM pivot_table(['business_metrics'],          -- table_names
                 ['sum(revenue)', 'sum(cost)'], -- values
                 ['product_line', 'product'],   -- rows
                 ['year', 'quarter'],           -- columns
                 [],                            -- filters
                 subtotals := 1,
                 grand_totals := 1,
                 values_axis := 'rows'
                 );
```

|     product_line&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     |    product&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    | value_names  | 2022_Q1 | 2022_Q2 | 2022_Q3 | 2022_Q4 | 2023_Q1 | 2023_Q2 | 2023_Q3 | 2023_Q4 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
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

## How the `pivot_table` extension works

The `pivot_table` extension is a collection of multiple scalar and table SQL macros.
This allows the logic to be modularized. 
You can see below that the functions are used as building blocks to create more complex functions.
This is typically difficult to do in SQL, but it is easy in DuckDB!

The functions and a brief description of each follows.

### Building block scalar functions

* `nq`: "No quotes" - Escape semicolons in a string to prevent SQL injection
* `sq`: "Single quotes" - Wrap a string in single quotes and escape embedded single quotes
* `dq`: "Double quotes" - Wrap in double quotes and escape embedded double quotes
* `nq_list`: Escape semicolons for each string in a list. Uses `nq`.
* `sq_list`: Wrap each string in a list in single quotes. Uses `sq`.
* `dq_list`: Wrap each string in a list in double quotes. Uses `dq`.
* `nq_concat`: Concatenate a list of strings together with semicolon escaping. Uses `nq_list`.
* `sq_concat`: Concatenate a list of strings together, wrapping each in single quotes. Uses `sq_list`.
* `dq_concat`: Concatenate a list of strings together, wrapping each in double quotes. Uses `dq_list`.

### Functions creating during refactoring for modularity

* `totals_list`: Build up a list as a part of enabling `subtotals` and `grand_totals`.
* `replace_zzz`: Rename `subtotal` and `grand_total` indicators after sorting so they are more friendly.

### Core pivoting logic functions

* `build_my_enum`: Determine which new columns to create when pivoting horizontally. Returns a table. See below for details.
* `pivot_table`: Based on inputs, decide whether to call `no_columns`, `columns_values_axis_columns` or `columns_values_axis_rows`. Execute `query` on the SQL string that is generated. Returns a table. See below for details.
    * `no_columns`: Build up the SQL string for `query` to execute when no `columns` are pivoted out.
    * `columns_values_axis_columns`: Build up the SQL string for `query` to execute when pivoting horizontally with each entry in `values` receiving a separate column.
    * `columns_values_axis_rows`: Build up the SQL string for `query` to execute when pivoting horizontally with each entry in `values` receiving a separate row.
* `pivot_table_show_sql`: Return the SQL string that would have been executed by `query` for debugging purposes.

### The `build_my_enum` function

The first step in using the `pivot_table` extension's capabilities is to define an `ENUM` (a user-defined type) containing all of the new column names to create when pivoting horizontally called `columns_parameter_enum`.
DuckDB's automatic `PIVOT` syntax can automatically define this, but in our case, we need 2 explicit steps.
The reason for this is that automatic pivoting runs 2 statements behind the scenes, but a `MACRO` must only be a single statement.
If the `columns` parameter is not in use, this step is essentially a no-op, so it can be omitted or included for consistency (recommended).

The `query` and `query_table` functions only support `SELECT` statements (for security reasons), so the dynamic portion of the `ENUM` creation occurs in the function `build_my_enum`.
If this type of usage becomes common, features could be added to DuckDB to enable a `CREATE OR REPLACE` syntax for `ENUM` types, or possibly even temporary enums.
That would reduce this pattern from 3 statements down to 2.
Please let us know!

The `build_my_enum` function uses a combination of `query_table` to pull from multiple input tables, and the `query` function so that double quotes (and correct character escaping) can be completed prior to passing in the list of table names.
It uses a similar pattern to the core `pivot_table` function: build up a SQL query as a string, then call it with `query`.
The SQL string is constructed using list lambda functions and the building block functions for quoting.

### The `pivot_table` function

At its core, the `pivot_table` function determines the SQL required to generate the desired pivot based on which parameters are in use.

Since this SQL statement is a string at the end of the day, we can use a hierarchy of scalar SQL macros rather than a single large macro.
This is a common traditional issue with SQL - it tends to not be very modular or reusable, but we are able to compartmentalize our logic wth DuckDB's syntax.

> Note If a non-optional parameter is not in use, an empty string (`[]`) should be passed in.

* `table_names`: A list of table or view names to aggregate or pivot. Multiple tables are combined with `UNION ALL BY NAME` prior to any other processing.
* `values`: A list of aggregation metrics in the format `['agg_fn_1(col_1)', 'agg_fn_2(col_2)', ...]`.
* `rows`: A list of column names to `SELECT` and `GROUP BY`.
* `columns`: A list of column names to `PIVOT` horizontally into a separate column per value in the original column. If multiple column names are passed in, only unique combinations of data that appear in the dataset are pivoted.
    * Ex: If passing in a `columns` parameter like `['continent', 'country']`, only valid `continent` / `country` pairs will be included.
    * (no `Europe_Canada` column would be generated).
* `filters`: A list of `WHERE` clause expressions to be applied to the raw dataset prior to aggregating in the format `['col_1 = 123', 'col_2 LIKE ''woot%''', ...]`.
    * The `filters` are combined with `AND`.
* `values_axis` (Optional): If multiple `values` are passed in, determine whether to create a separate row or column for each value. Either `rows` or `columns`, defaulting to `columns`.
* `subtotals` (Optional): If enabled, calculate the aggregate metric at multiple levels of detail based on the `rows` parameter. Either 0 or 1, defaulting to 0.
* `grand_totals` (Optional): If enabled, calculate the aggregate metric across all rows in the raw data in addition to at the granularity defined by `rows`. Either 0 or 1, defaulting to 0.

#### No horizontal pivoting (no `columns` in use)

If not using the `columns` parameter, no columns need to be pivoted horizontally.
As a result, a `GROUP BY` statement is used.
If `subtotals` are in use, the `ROLLUP` expression is used to calculate the `values` at the different levels of granularity.
If `grand_totals` are in use, but not `subtotals`, the `GROUPING SETS` expression is used instead of `ROLLUP` to evaluate across all rows.

In this example, we build a summary of the `revenue` and `cost` of each `product_line` and `product`.

```sql
FROM pivot_table(['business_metrics'],
                 ['sum(revenue)', 'sum(cost)'],
                 ['product_line', 'product'],
                 [],
                 [],
                 subtotals := 1,
                 grand_totals := 1,
                 values_axis := 'columns'
                 );
```

|     product_line     |    product    | sum(revenue) | sum("cost") |
|----------------------|---------------|-------------:|------------:|
| Duck Duds            | Duck neckties | 36           | 8           |
| Duck Duds            | Duck suits    | 360          | 80          |
| Duck Duds            | Subtotal      | 396          | 88          |
| Waterfowl watercraft | Duck boats    | 3600         | 800         |
| Waterfowl watercraft | Subtotal      | 3600         | 800         |
| Grand Total          | Grand Total   | 3996         | 888         |

#### Pivot horizontally, one column per metric in `values`

Build up a `PIVOT` statement that will pivot out all valid combinations of raw data values within the `columns` parameter. 
If `subtotals` or `grand_totals` are in use, make multiple copies of the input data, but replace appropriate column names in the `rows` parameter with a string constant.
Pass all expressions in `values` to the `PIVOT` statement's `USING` clause so they each receive their own column.

We enhance our previous example to pivot out a separate column for each `year` / `value` combination:

```sql
DROP TYPE IF EXISTS columns_parameter_enum;

CREATE TYPE columns_parameter_enum AS ENUM (
    FROM build_my_enum(['business_metrics'],
                       ['year'],
                       [])
);

FROM pivot_table(['business_metrics'],
                 ['sum(revenue)', 'sum(cost)'],
                 ['product_line', 'product'],
                 ['year'],
                 [],
                 subtotals := 1,
                 grand_totals := 1,
                 values_axis := 'columns'
                 );
```

|     product_line     |    product    | 2022_sum(revenue) | 2022_sum("cost") | 2023_sum(revenue) | 2023_sum("cost") |
|----------------------|---------------|------------------:|-----------------:|------------------:|-----------------:|
| Duck Duds            | Duck neckties | 10                | 4                | 26                | 4                |
| Duck Duds            | Duck suits    | 100               | 40               | 260               | 40               |
| Duck Duds            | Subtotal      | 110               | 44               | 286               | 44               |
| Waterfowl watercraft | Duck boats    | 1000              | 400              | 2600              | 400              |
| Waterfowl watercraft | Subtotal      | 1000              | 400              | 2600              | 400              |
| Grand Total          | Grand Total   | 1110              | 444              | 2886              | 444              |

#### Pivot horizontally, one row per metric in `values`

Build up a separate `PIVOT` statement for each metric in `values` and combine them with `UNION ALL BY NAME`. 
If `subtotals` or `grand_totals` are in use, make multiple copies of the input data, but replace appropriate column names in the `rows` parameter with a string constant.

To simplify the appearance slightly, we adjust one parameter in our previous query and set `values_axis := 'rows'`:

```sql
DROP TYPE IF EXISTS columns_parameter_enum;

CREATE TYPE columns_parameter_enum AS ENUM (
    FROM build_my_enum(['business_metrics'],
                       ['year'],
                       [])
);

FROM pivot_table(['business_metrics'],
                 ['sum(revenue)', 'sum(cost)'],
                 ['product_line', 'product'],
                 ['year'],
                 [],
                 subtotals := 1,
                 grand_totals := 1,
                 values_axis := 'rows'
                 );
```

|     product_line     |    product    | value_names  | 2022 | 2023 |
|----------------------|---------------|--------------|-----:|-----:|
| Duck Duds            | Duck neckties | sum(cost)    | 4    | 4    |
| Duck Duds            | Duck neckties | sum(revenue) | 10   | 26   |
| Duck Duds            | Duck suits    | sum(cost)    | 40   | 40   |
| Duck Duds            | Duck suits    | sum(revenue) | 100  | 260  |
| Duck Duds            | Subtotal      | sum(cost)    | 44   | 44   |
| Duck Duds            | Subtotal      | sum(revenue) | 110  | 286  |
| Waterfowl watercraft | Duck boats    | sum(cost)    | 400  | 400  |
| Waterfowl watercraft | Duck boats    | sum(revenue) | 1000 | 2600 |
| Waterfowl watercraft | Subtotal      | sum(cost)    | 400  | 400  |
| Waterfowl watercraft | Subtotal      | sum(revenue) | 1000 | 2600 |
| Grand Total          | Grand Total   | sum(cost)    | 444  | 444  |
| Grand Total          | Grand Total   | sum(revenue) | 1110 | 2886 |

## Conclusion

With DuckDB 1.1, sharing your SQL knowledge with the community has never been easier!
DuckDB's community extension repository is truly a package manager for the SQL language.
Macros in DuckDB are now highly reusable (thanks to `query` and `query_table`), and DuckDB's SQL syntax provides plenty of power to accomplish complex tasks.

Please let us know if the `pivot_table` extension is helpful to you - we are open to both contributions and feature requests!
Together we can write the ultimate pivoting capability just once and use it everywhere.

In the future, we have plans to further simplify the creation of SQL extensions.
Of course, we would love your feedback!
[Join us on Discord](https://discord.duckdb.org/) in the `community-extensions` channel.

Happy analyzing!

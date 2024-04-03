---

layout: post
title:  "Even Friendlier SQL with DuckDB"
author: Alex Monahan
excerpt: DuckDB continues to push the boundaries of SQL syntax to both simplify queries and make more advanced analyses possible. Highlights include dynamic column selection, queries that start with the FROM clause, function chaining, and list comprehensions. We boldly go where no SQL engine has gone before!
---

<img src="/images/blog/ai_generated_star_trek_rubber_duck.png"
     alt="Looks like a Duck ready to boldly go where databases have not gone before"
     width=200
/>

Who says that SQL should stay frozen in time, chained to a 1999 version of the specification? As a comparison, do folks remember what JavaScript felt like before Promises? Those didn’t launch until 2012! It’s clear that innovation at the programming syntax layer can have a profoundly positive impact on an entire language ecosystem.

We believe there are many valid reasons for innovation in the SQL language, among them opportunities to simplify basic queries and also to make more dynamic analyses possible. Many of these features arose from community suggestions! Please let us know your SQL pain points on [Discord](https://discord.duckdb.org/) or [GitHub](https://github.com/duckdb/duckdb/discussions) and join us as we change what it feels like to write SQL!

If you have not had a chance to read the first installment in this series, please take a quick look to the prior blog post, [“Friendlier SQL with DuckDB”](/2022/05/04/friendlier-sql).

## The future is now

The first few enhancements in this list were included in the “Ideas for the Future” section of the prior post.

### Reusable column aliases

When working with incremental calculated expressions in a select statement, traditional SQL dialects force you to either write out the full expression for each column or create a common table expression (CTE) around each step of the calculation. Now, any column alias can be reused by subsequent columns within the same select statement. Not only that, but these aliases can be used in the where and order by clauses as well.

#### Old way 1: Repeat yourself

```sql
SELECT 
    'These are the voyages of the starship Enterprise...' AS intro,
    instr('These are the voyages of the starship Enterprise...', 'starship')
        AS starship_loc
    substr('These are the voyages of the starship Enterprise...',
    instr('These are the voyages of the starship Enterprise...', 'starship')
        + len('starship') + 1) AS trimmed_intro;
```

#### Old way 2: All the CTEs

```sql
WITH intro_cte AS (
    SELECT
        'These are the voyages of the starship Enterprise...' AS intro
), starship_loc_cte AS (
    SELECT
        intro,
        instr(intro, 'starship') AS starship_loc
    FROM intro_cte
)
SELECT
    intro,
    starship_loc,
    substr(intro, starship_loc + len('starship') + 1) AS trimmed_intro
FROM starship_loc_cte;
```

#### New way

```sql
SELECT 
     'These are the voyages of the starship Enterprise...' AS intro,
     instr(intro, 'starship') AS starship_loc,
     substr(intro, starship_loc + len('starship') + 1) AS trimmed_intro;
```

<div class="narrow_table"></div>

|                        intro                        | starship_loc | trimmed_intro |
|:---|:---|:---|
| These are the voyages of the starship Enterprise... | 30           | Enterprise... |


### Dynamic column selection

Databases typically prefer strictness in column definitions and flexibility in the number of rows. This can help by enforcing data types and recording column level metadata. However, in data science workflows and elsewhere, it is very common to dynamically generate columns (for example during feature engineering).

No longer do you need to know all of your column names up front! DuckDB can select and even modify columns based on regular expression pattern matching, `EXCLUDE` or `REPLACE` modifiers, and even lambda functions (see the [section on lambda functions below](#list-lambda-functions) for details!). 

Let’s take a look at some facts gathered about the first season of Star Trek. Using DuckDB’s [`httpfs` extension](/docs/extensions/httpfs), we can query a csv dataset directly from GitHub. It has several columns so let’s `DESCRIBE` it.
```sql
INSTALL httpfs;
LOAD httpfs;

CREATE TABLE trek_facts AS
    SELECT *
    FROM 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv';

DESCRIBE trek_facts;
```

<div class="narrow_table"></div>

|               column_name               | column_type | null | key  | default | extra |
|:---|:---|:---|:---|:---|:---|
| season_num                              | BIGINT      | YES  | NULL | NULL    | NULL  |
| episode_num                             | BIGINT      | YES  | NULL | NULL    | NULL  |
| aired_date                              | DATE        | YES  | NULL | NULL    | NULL  |
| cnt_kirk_hookups                        | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_downed_redshirts                    | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_aliens_almost_took_over_planet     | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_aliens_almost_took_over_enterprise | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_vulcan_nerve_pinch                  | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_warp_speed_orders                   | BIGINT      | YES  | NULL | NULL    | NULL  |
| highest_warp_speed_issued               | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_hand_phasers_fired                 | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_ship_phasers_fired                 | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_ship_photon_torpedos_fired         | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_transporter_pax                     | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_damn_it_jim_quote                   | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_im_givin_her_all_shes_got_quote     | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_highly_illogical_quote              | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_enterprise_saved_the_day           | BIGINT      | YES  | NULL | NULL    | NULL  |

#### COLUMNS() with regular expressions

The `COLUMNS` expression can accept a string parameter that is a regular expression and will return all column names that match the pattern. How did warp change over the first season? Let’s examine any column name that contains the word `warp`.

```sql
SELECT
    episode_num,
    COLUMNS('.*warp.*')
FROM trek_facts;
```

<div class="narrow_table"></div>

| episode_num | cnt_warp_speed_orders | highest_warp_speed_issued |
|:---|:---|:---|
| 0           | 1                     | 1                         |
| 1           | 0                     | 0                         |
| 2           | 1                     | 1                         |
| 3           | 1                     | 0                         |
| ...         | ...                   | ...                       |
| 27          | 1                     | 1                         |
| 28          | 0                     | 0                         |
| 29          | 2                     | 8                         |

The `COLUMNS` expression can also be wrapped by other functions to apply those functions to each selected column. Let’s simplify the above query to look at the maximum values across all episodes:

```sql
SELECT
    MAX(COLUMNS('.*warp.*'))
FROM trek_facts;
```

<div class="narrow_table"></div>

| max(trek_facts.cnt_warp_speed_orders) | max(trek_facts.highest_warp_speed_issued) |
|:---|:---|
| 5                                     | 8                                         |

We can also create a `WHERE` clause that applies across multiple columns. All columns must match the filter criteria, which is equivalent to combining them with `AND`. Which episodes had at least 2 warp speed orders and at least a warp speed level of 2?

```sql
SELECT
    episode_num,
    COLUMNS('.*warp.*')
FROM trek_facts
WHERE
    COLUMNS('.*warp.*') >= 2;
    -- cnt_warp_speed_orders >= 2 
    -- AND 
    -- highest_warp_speed_issued >= 2
```

<div class="narrow_table"></div>

| episode_num | cnt_warp_speed_orders | highest_warp_speed_issued |
|:---|:---|:---|
| 14          | 3                     | 7                         |
| 17          | 2                     | 7                         |
| 18          | 2                     | 8                         |
| 29          | 2                     | 8                         |


### COLUMNS() with EXCLUDE and REPLACE

Individual columns can also be either excluded or replaced prior to applying calculations on them. For example, since our dataset only includes season 1, we do not need to find the `MAX` of that column. It would be highly illogical. 

```sql
SELECT
    MAX(COLUMNS(* EXCLUDE season_num))
FROM trek_facts;
```

<div class="narrow_table"></div>

| max(trek_facts.<br>episode_num) | max(trek_facts.<br>aired_date) | max(trek_facts.<br>cnt_kirk_hookups) | ... | max(trek_facts.<br>bool_enterprise_saved_the_day) |
|:---|:---|:---|:---|:---|
| 29                          | 1967-04-13                 | 2                                | ... | 1                                          |

The `REPLACE` syntax is also useful when applied to a dynamic set of columns. In this example, we want to convert the dates into timestamps prior to finding the maximum value in each column. Previously this would have required an entire subquery or CTE to pre-process just that single column!

```sql
SELECT
    MAX(COLUMNS(* REPLACE aired_date::timestamp AS aired_date))
FROM trek_facts;
```

<div class="narrow_table"></div>

| max(trek_facts.<br>season_num) | max(trek_facts.<br>episode_num) | max(aired_date := <br>CAST(aired_date AS TIMESTAMP)) | ... | max(trek_facts.<br>bool_enterprise_saved_the_day) |
|:---|:---|:---|:---|:---|
| 1                          | 29                          | 1967-04-13 00:00:00                              | ... | 1                                                   |

### COLUMNS() with lambda functions

The most flexible way to query a dynamic set of columns is through a [lambda function](/docs/sql/functions/nested#lambda-functions). This allows for any matching criteria to be applied to the names of the columns, not just regular expressions. See more details about lambda functions below. 

For example, if using the `LIKE` syntax is more comfortable, we can select columns matching a `LIKE` pattern rather than with a regular expression.

```sql
SELECT
    episode_num,
    COLUMNS(col -> col LIKE '%warp%')
FROM trek_facts
WHERE
    COLUMNS(col -> col LIKE '%warp%') >= 2;
```

<div class="narrow_table"></div>

| episode_num | cnt_warp_speed_orders | highest_warp_speed_issued |
|:---|:---|:---|
| 14          | 3                     | 7                         |
| 17          | 2                     | 7                         |
| 18          | 2                     | 8                         |
| 29          | 2                     | 8                         |


### Automatic JSON to nested types conversion

The first installment in the series mentioned JSON dot notation references as future work. However, the team has gone even further! Instead of referring to JSON-typed columns using dot notation, JSON can now be [automatically parsed](/2023/03/03/json) into DuckDB’s native types for significantly faster performance, compression, as well as that friendly dot notation!

First, install and load the `httpfs` and `json` extensions if they don't come bundled with the client you are using. Then query a remote JSON file directly as if it were a table!
```sql
INSTALL httpfs;
LOAD httpfs;
INSTALL json;
LOAD json;

SELECT 
     starfleet[10].model AS starship 
FROM 'https://raw.githubusercontent.com/vlad-saling/star-trek-ipsum/master/src/content/content.json';
```

<div class="narrow_table"></div>

|                                                                            starship                                                                            |
|:---|
| USS Farragut - NCC-1647 - Ship on which James Kirk served as a phaser station operator. Attacked by the Dikironium Cloud Creature, killing half the crew. ad.  |

Now for some new SQL capabilities beyond the ideas from the prior post!

## FROM first in SELECT statements

When building a query, the first thing you need to know is where your data is coming `FROM`. Well then why is that the second clause in a `SELECT` statement?? No longer! DuckDB is building SQL as it should have always been – putting the `FROM` clause first! This addresses one of the longest standing complaints about SQL, and the DuckDB team implemented it in 2 days. 

```sql
FROM my_table SELECT my_column;
```

Not only that, the `SELECT` statement can be completely removed and DuckDB will assume all columns should be `SELECT`ed. Taking a look at a table is now as simple as:
```sql
FROM my_table;
-- SELECT * FROM my_table
```

Other statements like `COPY` are simplified as well.
```sql
COPY (FROM trek_facts) TO 'phaser_filled_facts.parquet';
```

This has an additional benefit beyond saving keystrokes and staying in a development flow state: autocomplete will have much more context when you begin to choose columns to query. Give the AI a helping hand!

Note that this syntax is completely optional, so your `SELECT * FROM` keyboard shortcuts are safe, even if they are obsolete... 🙂

## Function chaining

Many SQL blogs advise the use of CTEs instead of subqueries. Among other benefits, they are much more readable. Operations are compartmentalized into discrete chunks and they can be read in order top to bottom instead of forcing the reader to work their way inside out. 

DuckDB enables the same interpretability improvement for every scalar function! Use the dot operator to chain functions together, just like in Python. The prior expression in the chain is used as the first argument to the subsequent function. 

```sql
SELECT 
     ('Make it so')
          .UPPER()
          .string_split(' ')
          .list_aggr('string_agg','.')
          .concat('.') AS im_not_messing_around_number_one;
```

<div class="narrow_table"></div>

| im_not_messing_around_number_one |
|:---|
| MAKE.IT.SO.                      |

Now compare that with the old way...

```sql
SELECT 
     concat(
          list_aggr(
               string_split(
                    UPPER('Make it stop'),
               ' '),
          'string_agg','.'),
     '.') AS oof;
```

<div class="narrow_table"></div>

|      oof      |
|:---|
| MAKE.IT.STOP. |

## Union by name

DuckDB aims to blend the best of databases and dataframes. This new syntax is inspired by the [concat function in Pandas](https://pandas.pydata.org/docs/reference/api/pandas.concat.html). Rather than vertically stacking tables based on column position, columns are matched by name and stacked accordingly. Simply replace `UNION` with `UNION BY NAME` or `UNION ALL` with `UNION ALL BY NAME`. 

For example, we had to add some new alien species proverbs in The Next Generation:
```sql
CREATE TABLE proverbs AS
     SELECT 
          'Revenge is a dish best served cold' AS klingon_proverb 
     UNION ALL BY NAME 
     SELECT 
          'You will be assimilated' AS borg_proverb,
          'If winning is not important, why keep score?' AS klingon_proverb;

FROM proverbs;
```

<div class="narrow_table"></div>

|               klingon_proverb                |      borg_proverb       |
|:---|:---|
| Revenge is a dish best served cold           | NULL                    |
| If winning is not important, why keep score? | You will be assimilated |

This approach has additional benefits. As seen above, not only can tables with different column orders be combined, but so can tables with different numbers of columns entirely. This is helpful as schemas migrate, and is particularly useful for DuckDB’s [multi-file reading capabilities](/docs/data/multiple_files/combining_schemas#union-by-name).

## Insert by name

Another common situation where column order is strict in SQL is when inserting data into a table. Either the columns must match the order exactly, or all of the column names must be repeated in two locations within the query. 

Instead, add the keywords `BY NAME` after the table name when inserting. Any subset of the columns in the table in any order can be inserted.

```sql
INSERT INTO proverbs BY NAME 
     SELECT 'Resistance is futile' AS borg_proverb;

SELECT * FROM proverbs;
```

<div class="narrow_table"></div>

|               klingon_proverb                |      borg_proverb       |
|:---|:---|
| Revenge is a dish best served cold           | NULL                    |
| If winning is not important, why keep score? | You will be assimilated |
| NULL                                         | Resistance is futile    |

## Dynamic PIVOT and UNPIVOT

Historically, databases are not well-suited for pivoting operations. However, DuckDB’s `PIVOT` and `UNPIVOT` clauses can create or stack dynamic column names for a truly flexible pivoting capability! In addition to that flexibility, DuckDB also provides both the SQL standard syntax and a friendlier shorthand. 

For example, let’s take a look at some procurement forecast data just as the Earth-Romulan war was beginning:
```sql
CREATE TABLE purchases (item VARCHAR, year INT, count INT);

INSERT INTO purchases
    VALUES ('phasers', 2155, 1035),
           ('phasers', 2156, 25039),
           ('phasers', 2157, 95000),
           ('photon torpedoes', 2155, 255),
           ('photon torpedoes', 2156, 17899),
           ('photon torpedoes', 2157, 87492);

FROM purchases;
```

<div class="narrow_table"></div>

|       item       | year | count |
|:---|:---|:---|
| phasers          | 2155 | 1035  |
| phasers          | 2156 | 25039 |
| phasers          | 2157 | 95000 |
| photon torpedoes | 2155 | 255   |
| photon torpedoes | 2156 | 17899 |
| photon torpedoes | 2157 | 87492 |

It is easier to compare our phaser needs to our photon torpedo needs if each year’s data is visually close together. Let’s pivot this into a friendlier format! Each year should receive its own column (but each year shouldn’t need to be specified in the query!), we want to sum up the total `count`, and we still want to keep a separate group (row) for each `item`. 

```sql
CREATE TABLE pivoted_purchases AS
     PIVOT purchases 
          ON year 
          USING SUM(count) 
          GROUP BY item;

FROM pivoted_purchases;
```

<div class="narrow_table"></div>

|       item       | 2155 | 2156  | 2157  |
|:---|:---|:---|:---|
| phasers          | 1035 | 25039 | 95000 |
| photon torpedoes | 255  | 17899 | 87492 |

Looks like photon torpedoes went on sale... 

Now imagine the reverse situation. Scotty in engineering has been visually analyzing and manually constructing his purchases forecast. He prefers things pivoted so it’s easier to read. Now you need to fit it back into the database! This war may go on for a bit, so you may need to do this again next year. Let’s write an `UNPIVOT` query to return to the original format that can handle any year. 

The `COLUMNS` expression will use all columns except `item`. After stacking, the column containing the column names from `pivoted_purchases` should be renamed to `year`, and the values within those columns represent the `count`. The result is the same dataset as the original. 

```sql
UNPIVOT pivoted_purchases
     ON COLUMNS(* EXCLUDE item)
     INTO
          NAME year
          VALUE count;
```

<div class="narrow_table"></div>

|       item       | year | count |
|:---|:---|:---|
| phasers          | 2155 | 1035  |
| phasers          | 2156 | 25039 |
| phasers          | 2157 | 95000 |
| photon torpedoes | 2155 | 255   |
| photon torpedoes | 2156 | 17899 |
| photon torpedoes | 2157 | 87492 |

More examples are included as a part of our [DuckDB 0.8.0 announcement post](/2023/05/17/announcing-duckdb-080.html#new-sql-features), and the [`PIVOT`](/docs/sql/statements/pivot) and [`UNPIVOT`](/docs/sql/statements/unpivot) documentation pages highlight more complex queries. 

Stay tuned for a future post to cover what is happening behind the scenes! 

## List lambda functions

List lambdas allow for operations to be applied to each item in a list. These do not need to be pre-defined – they are created on the fly within the query. 

In this example, a lambda function is used in combination with the `list_transform` function to shorten each official ship name. 

```sql
SELECT 
     (['Enterprise NCC-1701', 'Voyager NCC-74656', 'Discovery NCC-1031'])
          .list_transform(x -> x.string_split(' ')[1]) AS short_name;
```

<div class="narrow_table"></div>

|            ship_name             |
|:---|
| [Enterprise, Voyager, Discovery] |

Lambdas can also be used to filter down the items in a list. The lambda returns a list of booleans, which is used by the `list_filter` function to select specific items. The `contains` function is using the [function chaining](#function-chaining) described earlier.

```sql
SELECT 
     (['Enterprise NCC-1701', 'Voyager NCC-74656', 'Discovery NCC-1031'])
          .list_filter(x -> x.contains('1701')) AS the_original;
```

<div class="narrow_table"></div>

|     the_original      |
|:---|
| [Enterprise NCC-1701] |

## List comprehensions

What if there was a simple syntax to both modify and filter a list? DuckDB takes inspiration from Python’s approach to list comprehensions to dramatically simplify the above examples. List comprehensions are syntactic sugar – these queries are rewritten into lambda expressions behind the scenes!

Within brackets, first specify the transformation that is desired, then indicate which list should be iterated over, and finally include the filter criteria. 

```sql
SELECT 
     [x.string_split(' ')[1] 
     FOR x IN ['Enterprise NCC-1701', 'Voyager NCC-74656', 'Discovery NCC-1031'] 
     IF x.contains('1701')] AS ready_to_boldly_go;
```

<div class="narrow_table"></div>

| ready_to_boldly_go |
|:---|
| [Enterprise]       |

## Exploding struct.*

A struct in DuckDB is a set of key/value pairs. Behind the scenes, a struct is stored with a separate column for each key. As a result, it is computationally easy to explode a struct into separate columns, and now it is also syntactically simple as well! This is another example of allowing SQL to handle dynamic column names.

```sql
WITH damage_report AS (
     SELECT {'gold_casualties':5, 'blue_casualties':15, 'red_casualties': 10000} AS casualties
) 
FROM damage_report
SELECT 
     casualties.*;
```

<div class="narrow_table"></div>

| gold_casualties | blue_casualties | red_casualties |
|:---|:---|:---|
| 5               | 15              | 10000          |

## Automatic struct creation

DuckDB exposes an easy way to convert any table into a single-column struct. Instead of `SELECT`ing column names, `SELECT` the table name itself.

```sql
WITH officers AS (
     SELECT 'Captain' AS rank, 'Jean-Luc Picard' AS name 
     UNION ALL 
     SELECT 'Lieutenant Commander', 'Data'
) 
FROM officers 
SELECT officers;
```

<div class="narrow_table"></div>

|                   officers                   |
|:---|
| {'rank': Captain, 'name': Jean-Luc Picard}   |
| {'rank': Lieutenant Commander, 'name': Data} |

## Union data type

DuckDB utilizes strong typing to provide high performance and enforce data quality. However, DuckDB is also as forgiving as possible using approaches like implicit casting to avoid always having to cast between data types. 

Another way DuckDB enables flexibility is the new `UNION` data type. A `UNION` data type allows for a single column to contain multiple types of values. This can be thought of as an “opt-in” to SQLite’s flexible data typing rules (the opposite direction of SQLite’s recently announced [strict tables](https://www.sqlite.org/stricttables.html)).

By default DuckDB will seek the common denominator of data types when combining tables together. The below query results in a `VARCHAR` column:

```sql
SELECT 'The Motion Picture' AS movie UNION ALL 
SELECT 2 UNION ALL 
SELECT 3 UNION ALL 
SELECT 4 UNION ALL 
SELECT 5 UNION ALL 
SELECT 6 UNION ALL 
SELECT 'First Contact';
```

<div class="narrow_table"></div>

|       movie        |
|     varchar        |
|:---|
| The Motion Picture |
| First Contact      |
| 6                  |
| 5                  |
| 4                  |
| 3                  |
| 2                  |

However, if a `UNION` type is used, each individual row retains its original data type. A `UNION` is defined using key-value pairs with the key as a name and the value as the data type. This also allows the specific data types to be pulled out as individual columns:
```sql
CREATE TABLE movies (
     movie UNION(num INT, name VARCHAR)
);
INSERT INTO movies VALUES
     ('The Motion Picture'), (2), (3), (4), (5), (6), ('First Contact');

FROM movies 
SELECT 
     movie,
     union_tag(movie) AS type,
     movie.name,
     movie.num;
```

<div class="narrow_table"></div>

|       movie        | type |        name        | num |
| union(num integer, name varchar) | varchar |        varchar        | int32 |
|:---|:---|:---|:---|
| The Motion Picture | name | The Motion Picture |     |
| 2                  | num  |                    | 2   |
| 3                  | num  |                    | 3   |
| 4                  | num  |                    | 4   |
| 5                  | num  |                    | 5   |
| 6                  | num  |                    | 6   |
| First Contact      | name | First Contact      |     |

## Additional friendly features

Several other friendly features are worth mentioning and some are powerful enough to warrant their own blog posts. 

DuckDB takes a nod from the [`describe` function in Pandas](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html) and implements a `SUMMARIZE` keyword that will calculate a variety of statistics about each column in a dataset for a quick, high-level overview. Simply prepend `SUMMARIZE` to any table or `SELECT` statement. 

Have a look at the [correlated subqueries post](/2023/05/26/correlated-subqueries-in-sql) to see how to use subqueries that refer to each others’ columns. DuckDB’s advanced optimizer improves correlated subquery performance by orders of magnitude, allowing for queries to be expressed as naturally as possible. What was once an anti-pattern for performance reasons can now be used freely!

DuckDB has added more ways to `JOIN` tables together that make expressing common calculations much easier. Some like `LATERAL`, `ASOF`, `SEMI`, and `ANTI` joins are present in other systems, but have high-performance implementations in DuckDB. DuckDB also adds a new `POSITIONAL` join that combines by the row numbers in each table to match the commonly used Pandas capability of joining on row number indexes. See the [`JOIN` documentation](/docs/sql/query_syntax/from) for details, and look out for a blog post describing DuckDB’s state of the art `ASOF` joins!

## Summary and future work

DuckDB aims to be the easiest database to use. Fundamental architectural decisions to be in-process, have zero dependencies, and have strong typing contribute to this goal, but the friendliness of its SQL dialect has a strong impact as well. By extending the industry-standard PostgreSQL dialect, DuckDB aims to provide the simplest way to express the data transformations you need. These changes range from altering the ancient clause order of the `SELECT` statement to begin with `FROM`, allowing a fundamentally new way to use functions with chaining, to advanced nested data type calculations like list comprehensions. Each of these features are available in the 0.8.1 release.

Future work for friendlier SQL includes:
* Lambda functions with more than 1 argument, like `list_zip`
* Underscores as digit separators (Ex: `1_000_000` instead of `1000000`)
* Extension user experience, including autoloading
* Improvements to file globbing
* Your suggestions!

Please let us know what areas of SQL can be improved! We welcome your feedback on [Discord](https://discord.duckdb.org/) or [GitHub](https://github.com/duckdb/duckdb/discussions).

Live long and prosper! 🖖

---
layout: post  
title:  "Friendlier SQL with DuckDB"
author: Alex Monahan
excerpt_separator: <!--more-->
---
<img src="/images/blog/duck_chewbacca.png" alt="Chewbacca_the_duck" title="Chewbacca the duck is pretty friendly" width=200/>

An elegant user experience is a key design goal of DuckDB. This goal guides much of DuckDB's architecture: it is simple to install, seamless to integrate with other data structures like Pandas, Arrow, and R Dataframes, and requires no dependencies. Parallelization occurs automatically, and if a computation exceeds available memory, data is gracefully buffered out to disk. And of course, DuckDB's processing speed makes it easier to get more work accomplished. 

However, SQL is not famous for being user-friendly. DuckDB aims to change that! DuckDB includes both a Relational API for dataframe-style computation, and a highly Postgres-compatible version of SQL. If you prefer dataframe-style computation, we would love your feedback on [our roadmap](https://github.com/duckdb/duckdb/issues/2000). If you are a SQL fan, read on to see how DuckDB is bringing together both innovation and pragmatism to make it easier to write SQL in DuckDB than anywhere else. Please reach out on [GitHub](https://github.com/duckdb/duckdb/discussions) or [Discord](https://discord.gg/vukK4xp7Rd) and let us know what other features would simplify your SQL workflows. Join us as we teach an old dog new tricks!
<!--more-->

### SELECT * EXCLUDE 
A traditional SQL `SELECT` query requires that requested columns be explicitly specified, with one notable exception: the `*` wildcard. `SELECT *` allows SQL to return all relevant columns. This adds tremendous flexibility, especially when building queries on top of one another. However, we are often interested in *almost* all columns. In DuckDB, simply specify which columns to `EXCLUDE`:
```sql
SELECT * EXCLUDE (jar_jar_binks, midichlorians) FROM star_wars
```
Now we can save time repeatedly typing all columns, improve code readability, and retain flexibility as additional columns are added to underlying tables.  

DuckDB's implementation of this concept can even handle exclusions from multiple tables within a single statement:
```sql
SELECT 
    sw.* EXCLUDE (jar_jar_binks, midichlorians),
    ff.* EXCLUDE cancellation
FROM star_wars sw, firefly ff
```

### SELECT * REPLACE
Similarly, we often wish to use all of the columns in a table, aside from a few small adjustments. This would also prevent the use of `*` and require a list of all columns, including those that remain unedited. In DuckDB, easily apply changes to a small number of columns with `REPLACE`:
```sql
SELECT 
    * REPLACE (movie_count+3 as movie_count, show_count*1000 as show_count)
FROM star_wars_owned_by_disney
```
This allows views, CTE's, or sub-queries to be built on one another in a highly concise way, while remaining adaptable to new underlying columns. 

### GROUP BY ALL
A common cause of repetitive and verbose SQL code is the need to specify columns in both the `SELECT` clause and the `GROUP BY` clause. In theory this adds flexibility to SQL, but in practice it rarely adds value. DuckDB now offers the `GROUP BY` we all expected when we first learned SQL - just `GROUP BY ALL` columns in the `SELECT` clause that aren't wrapped in an aggregate function!
```sql
SELECT
    systems,
    planets,
    cities,
    cantinas,
    SUM(scum + villainy) as total_scum_and_villainy
FROM star_wars_locations
GROUP BY ALL
-- GROUP BY systems, planets, cities, cantinas
```

Now changes to a query can be made in only one place instead of two! Plus this prevents many mistakes where columns are removed from a `SELECT` list, but not from the `GROUP BY`, causing duplication.

Not only does this dramatically simplify many queries, it also makes the above `EXCLUDE` and `REPLACE` clauses useful in far more situations. Imagine if we wanted to adjust the above query by no longer considering the level of scum and villainy in each specific cantina:
```sql
SELECT
    * EXCLUDE (cantinas, booths, scum, villainy),
    SUM(scum + villainy) as total_scum_and_villainy
FROM star_wars_locations
GROUP BY ALL
-- GROUP BY systems, planets, cities
```
Now that is some concise and flexible SQL! How many of your `GROUP BY` clauses could be re-written this way?

### ORDER BY ALL
Another common cause for repetition in SQL is the `ORDER BY` clause. DuckDB and other RDBMSs have previously tackled this issue by allowing queries to specify the numbers of columns to `ORDER BY` (For example, `ORDER BY 1, 2, 3`). However, frequently the goal is to order by all columns in the query from left to right, and maintaining that numeric list when adding or subtracting columns can be error prone. In DuckDB, simply `ORDER BY ALL`: 
```sql
SELECT
    age,
    sum(civility) as total_civility
FROM star_wars_universe
GROUP BY ALL
ORDER BY ALL
-- ORDER BY age, total_civility
```
This is particularly useful when building summaries, as many other client tools automatically sort results in this manner. DuckDB also supports `ORDER BY ALL DESC` to sort each column in reverse order, and options to specify `NULLS FIRST` or `NULLS LAST`.

### Column Aliases in WHERE / GROUP BY / HAVING
In many SQL dialects, it is not possible to use an alias defined in a `SELECT` clause anywhere but in the `ORDER BY` clause of that statement. This commonly leads to verbose CTE's or subqueries in order to utilize those aliases. In DuckDB, a non-aggregate alias in the `SELECT` clause can be immediately used in the `WHERE` and `GROUP BY` clauses, and aggregate aliases can be used in the `HAVING` clause, even at the same query depth. No subquery needed!

```sql
SELECT
    only_imperial_storm_troopers_are_so_precise as nope,
    turns_out_a_parsec_is_a_distance as very_speedy,
    SUM(mistakes) as total_oops
FROM oops
WHERE
    nope = 1
GROUP BY
    nope,
    very_speedy
HAVING
    total_oops > 0
```

### Case Insensitivity While Maintaining Case
DuckDB allows queries to be case insensitive, while maintaining the specified case as data flows into and out of the system. This simplifies queries within DuckDB while ensuring compatibility with external libraries.

```sql
CREATE TABLE mandalorian as SELECT 1 as "THIS_IS_THE_WAY";
SELECT this_is_the_way FROM mandalorian;
```  

| THIS_IS_THE_WAY |
|:---|
| 1               |


### Friendly Error Messages
Regardless of expertise, and despite DuckDB's best efforts to understand our intentions, we all make mistakes in our SQL queries. Many RDBMSs leave you trying to use the force to detect an error. In DuckDB, if you make a typo on a column or table name, you will receive a helpful suggestion about the most similar name. Not only that, you will receive an arrow that points directly to the offending location within your query. 

```sql
select * from star_trek;
Error: Catalog Error: Table with name star_trek does not exist!
Did you mean "star_wars"?
LINE 1: select * from star_trek;
                      ^
```
(Don't worry, ducks and duck-themed databases still love some Trek as well).

DuckDB's suggestions are even context specific. Here, we receive a suggestion to use the most similar column from the table we are querying.

```sql
select long_ago from star_wars;
Error: Binder Error: Referenced column "long_ago" not found in FROM clause!
Candidate bindings: "star_wars.long_long_ago"
LINE 1: select long_ago from star_wars;
               ^
```

### String Slicing
Even as SQL fans, we know that SQL can learn a thing or two from newer languages. Instead of using bulky `SUBSTRING` functions, you can slice strings in DuckDB using bracket syntax. As a note, SQL is required to be 1-indexed, so that is a slight difference from other languages (although it keeps DuckDB internally consistent and similar to other DBs). 

```sql
SELECT 'I love you! I know'[:-3] as nearly_soloed;
```  

|  nearly_soloed  |
|:---|
| I love you! I k |

### Simple List and Struct Creation
DuckDB provides nested types to allow more flexible data structures than the purely relational model would allow, while retaining high performance. To make them as easy as possible to use, creating a `LIST` (array) or a `STRUCT` (object) uses simpler syntax than other SQL systems. Data types are automatically inferred.

```sql
SELECT
    ['A-Wing', 'B-Wing', 'X-Wing', 'Y-Wing'] as starfighter_list,
    {name: 'Star Destroyer', common_misconceptions: 'Can''t in fact destroy a star'} as star_destroyer_facts
```

### List Slicing
Bracket syntax may also be used to slice a `LIST`. Again, note that this is 1-indexed for SQL compatibility.
```sql
SELECT 
    starfighter_list[2:2] as dont_forget_the_b_wing 
FROM (SELECT ['A-Wing', 'B-Wing', 'X-Wing', 'Y-Wing'] as starfighter_list);
```  

| dont_forget_the_b_wing |
|:---|
| [B-Wing]               |

### Struct Dot Notation
Use convenient dot notation to access the value of a specific key in a DuckDB `STRUCT` column. If keys contain spaces, double quotes can be used.

```sql
SELECT 
    planet.name,
    planet."Amount of sand" 
FROM (SELECT {name: 'Tatooine', 'Amount of sand': 'High'} as planet)
```

### Trailing Commas
Have you ever removed your final column from a SQL `SELECT` and been met with an error, only to find you needed to remove the trailing comma as well!? Never? Ok, Jedi... On a more serious note, this feature is an example of DuckDB's responsiveness to the community. In under 2 days from seeing this issue in a tweet (not even about DuckDB!), this feature was already built, tested, and merged into the primary branch. You can include trailing commas in many places in your query, and we hope this saves you from the most boring but frustrating of errors! 

```sql
SELECT
    x_wing,
    proton_torpedoes,
    --targeting_computer
FROM luke_whats_wrong
GROUP BY
    x_wing,
    proton_torpedoes,
```

### Function Aliases from Other Databases
For many functions, DuckDB supports multiple names in order to align with other database systems. After all, ducks are pretty versatile - they can fly, swim, and walk! Most commonly, DuckDB supports PostgreSQL function names, but many SQLite names are supported, as well as some from other systems. If you are migrating your workloads to DuckDB and a different function name would be helpful, please reach out - they are very easy to add as long as the behavior is the same! See our [functions documentation](https://duckdb.org/docs/sql/functions/overview) for details.

```sql
SELECT
    'Use the Force, Luke'[:13] as sliced_quote_1,
    substr('I am your father', 1, 4) as sliced_quote_2,
    substring('Obi-Wan Kenobi, you''re my only hope',17,100) as sliced_quote_3
```

### Auto-Increment Duplicate Column Names
As you are building a query that joins similar tables, you'll often encounter duplicate column names. If the query is the final result, DuckDB will simply return the duplicated column names without modifications. However, if the query is used to create a table, or nested in a subquery or Common Table Expression (where duplicate columns are forbidden by other databases!), DuckDB will automatically assign new names to the repeated columns to make query prototyping easier. 

```sql
SELECT
    *
FROM (
    SELECT
        s1.tie_fighter,
        s2.tie_fighter
    FROM squadron_one s1
    JOIN squadron_two s2
        ON 1=1
    ) theyre_coming_in_too_fast
```  

| tie_fighter | tie_fighter:1 |
|:---|:---|
| green_one   | green_two     |

### Implicit Type Casts
DuckDB believes in using specific data types for performance, but attempts to automatically cast between types whenever necessary. For example, when joining between an integer and a varchar, DuckDB will automatically cast them to be the same type and complete the join successfully. A `List` or `IN` expression may also be created with a mixture of types, and they will be automatically cast as well. Also, `INT` and `BIGINT` are interchangeable, and thanks to DuckDB's new storage compression, a `BIGINT` usually doesn't even take up any extra space! Now you can store your data as the optimal data type, but use it easily for the best of both!

```sql
CREATE TABLE sith_count_int as SELECT 2::INT as sith_count;
CREATE TABLE sith_count_varchar as SELECT 2::VARCHAR as sith_count;

SELECT 
    * 
FROM sith_count_int s_int 
JOIN sith_count_varchar s_char 
    on s_int.sith_count = s_char.sith_count;
```  

| sith_count | sith_count |
|:---|:---|
| 2          | 2          |

### Other Friendly Features
There are many other features of DuckDB that make it easier to analyze data with SQL!  
  
DuckDB [makes working with time easier in many ways](https://duckdb.org/2022/01/06/time-zones.html), including by accepting multiple different syntaxes (from other databases) for the [`INTERVAL` data type](https://duckdb.org/docs/sql/data_types/interval) used to specify a length of time.  
  
DuckDB also implements multiple SQL clauses outside of the traditional core clauses including the [`SAMPLE` clause](https://duckdb.org/docs/sql/query_syntax/sample) for quickly selecting a random subset of your data and the [`QUALIFY` clause](https://duckdb.org/docs/sql/query_syntax/qualify) that allows filtering of the results of window functions (much like a `HAVING` clause does for aggregates).  
  
The [`DISTINCT ON` clause](https://duckdb.org/docs/sql/statements/select) allows DuckDB to select unique combinations of a subset of the columns in a `SELECT` clause, while returning the first row of data for columns not checked for uniqueness.


### Ideas for the Future
In addition to what has already been implemented, several other improvements have been suggested. Let us know if one would be particularly useful - we are flexible with our roadmap! If you would like to contribute, we are very open to PRs and you are welcome to reach out on [GitHub](https://github.com/duckdb/duckdb) or [Discord](https://discord.gg/vukK4xp7Rd) ahead of time to talk through a new feature's design. 

 - Choose columns via regex 
    - Decide which columns to select with a pattern rather than specifying columns explicitly
    - Clickhouse supports this with the [`COLUMNS` expression](https://clickhouse.com/docs/en/sql-reference/statements/select/#columns-expression) 
 - Incremental column aliases
    - Refer to previously defined aliases in subsequent calculated columns rather than re-specifying the calculations
-  Dot operators for JSON types
    - The JSON extension is brand new ([see our documentation!](https://duckdb.org/docs/extensions/json)) and already implements friendly `->` and `->>` syntax

Thanks for checking out DuckDB! May the Force be with you...

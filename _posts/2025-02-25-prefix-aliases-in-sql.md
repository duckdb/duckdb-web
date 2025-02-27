---
layout: post
title: "Prefix Aliases in SQL"
author: "Hannes Mühleisen"
excerpt: "You can now put your aliases first in DuckDB's SQL dialect with a colon, e.g., `SELECT a: 42;`"
thumb: "/images/blog/thumbs/prefix-aliases.svg"
image: "/images/blog/thumbs/prefix-aliases.png"
tags: ["using DuckDB"]
---

## Syntax

<p><i>“Perhaps we <a href="https://www.youtube.com/watch?v=TBAf5l1RmcA">should just leave nature alone</a>, to its simple one assed schematics.”</i><br/>
   — Dr. Alphonse Mephesto, South Park Episode #5</p>

There is often more than one way to do things in our beloved SQL. For example, you can define join conditions *implicitly* (and dangerously) in the `WHERE` clause or use the (better) `JOIN ... ON (...)` syntax. Generally, having “more than one way to do things” can be confusing and even outright [dangerous sometimes](https://www.youtube.com/watch?v=noQcWra6sbU).

Having said that we here at DuckDB [pride]({% post_url 2022-05-04-friendlier-sql %}) [ourselves]({% post_url 2023-08-23-even-friendlier-sql %}) [in]({% link docs/stable/sql/dialect/friendly_sql.md %}) *friendlier* SQL. There are just too many people typing this stuff by hand, especially in the more ad-hoc world of analytics.  

If there is a *good* reason to expand the SQL syntax with something useful we are at least considering it. Others seem to be watching closely. For example, our `GROUP BY ALL` syntax has by now been picked up by [almost](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax) [every](https://docs.snowflake.com/en/sql-reference/constructs/group-by#label-group-by-all-columns) [SQL](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-groupby) [system](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql?view=sql-server-ver16#group-by-all-column-expression--n-) out there (and their little brothers).

## Aliases

In SQL, a user can define *aliases* for lots of things like `SELECT` expressions, table names, subqueries, etc. This is sometimes just nice to have readable column names in the result and sometimes required to refer back to a complex expression in for example the `ORDER BY` clause without just repeating it and praying for the optimizer. Aliases are defined *after* the thing they alias using `AS` but actually typing the `AS` term is optional. For example, those two statements are equivalent:

```sql
SELECT 42 AS fortytwo;
SELECT 42 fortytwo;
```

We can see the alias follows the expression (`42`) and the `AS` is optional. Having the alias *behind* the thing it describes is actually somewhat rare in programming, it is much more typical to define the alias first and then provide the expression. For example, in C:

```c
int fortytwo = 42;
```

It seems to be a good idea to first state the alias, after all, this is what we are going to refer to this thing later on. Forcing it the other way around like SQL just increases the mental load. In addition, having the aliases last can make them quite hard to find if there are several complex expressions in a query. For example, here are the first few lines of the infamous TPC-H Query 1:

```sql
SELECT
    l_returnflag,
    l_linestatus,
    sum(l_quantity) sum_qty,
    sum(l_extendedprice) sum_base_price,
    sum(l_extendedprice * (1 - l_discount)) sum_disc_price,
    sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) sum_charge,
    avg(l_quantity) avg_qty,
    avg(l_extendedprice) avg_price,
    avg(l_discount) avg_disc,
    count(*) count_order
    ...
```

It's hard to spot all the aliases here, and this is not even a complex example. What if you could put the aliases first in SQL? Well, wait no more.

## Prefix Aliases in DuckDB

In the latest DuckDB release, [1.2.0]({% post_url 2025-02-05-announcing-duckdb-120 %}), we have quietly shipped yet another useful (we think) [syntax extension](https://github.com/duckdb/duckdb/pull/14436) to allow the alias to come before the thing it names using the colon (`:`) syntax. This turned out to be less difficult than we thought, “all” it took was some modification to the Bison parser we inherited from Postgres ([but are in the process of replacing]({% post_url 2024-11-22-runtime-extensible-parsers %})). Here is the example from before again:

```sql
SELECT fortytwo: 42;
```

Prefix aliases also work for table names, e.g.:

```sql
SELECT *
FROM my_table: some_other_table;
```

Aliases can be quoted if neccessary using *double* quotes:

```sql
SELECT "forty two": 42;
```

Prefix aliases can be used to name just about everything, for example expressions, function calls and subqueries in the `SELECT` clause:

```sql
SELECT 
    e: 1 + 2, 
    f: len('asdf'), 
    s: (SELECT 42);
```

They can also apply to function calls and subqueries in the `FROM clause`, e.g.:

```sql
SELECT *
FROM
    r: range(10),
    v: (VALUES (42)),
    s: (FROM range(10))
```

Note that the `VALUES` clause and the subquery with `FROM` need additional parentheses to work here, this was required to pacify the evil Bison parser generator. Let's look at the Q1 example from earlier, but this time with prefix aliases:

```sql
SELECT
    l_returnflag,
    l_linestatus,
    sum_qty:        sum(l_quantity),
    sum_base_price: sum(l_extendedprice),
    sum_disc_price: sum(l_extendedprice * (1-l_discount)),
    sum_charge:     sum(l_extendedprice * (1-l_discount) * (1+l_tax)),
    avg_qty:        avg(l_quantity),
    avg_price:      avg(l_extendedprice),
    avg_disc:       avg(l_discount),
    count_order:    count(*) 
    ...
```

There is no semantic difference between using `:` or `AS`, they lead to the same query constructs.

## Credits

Credit for this idea goes to Looker veteran [Michael Toy](https://www.linkedin.com/in/michael-toy-27b3407/).
We're grateful for his suggestion.
We also would like to thank the legendary [Lloyd Tabb](https://www.linkedin.com/in/lloydtabb/) for recommending Michael's idea to us.
Also check out Mark Needham's [video on DuckDB's prefix aliases](https://youtu.be/rwIiw7HZa1M?si=yRzsHfpd62d0pp7u&t=215).

---
layout: post
title:  "(Correlated) Subqueries in SQL"
author: Mark Raasveldt
excerpt_separator: <!--more-->
---


Subqueries in SQL are a powerful abstraction that allow simple queries to be used as composable building blocks. They allow you to break down complex problems into smaller parts, and subsequently make it easier to write, understand and maintain large and complex queries.

DuckDB uses a state-of-the-art subquery decorrelation optimizer that allows subqueries to be executed very efficiently. As a result, users can freely use subqueries to create expressive queries without having to worry about manually rewriting subqueries into joins. For more information, skip to the [Performance](#Performance) section.

### Types of Subqueries

SQL subqueries exist in two main forms: subqueries as *expressions* and subqueries as *tables*. Subqueries that are used as expressions can be used in the `SELECT` or `WHERE` clauses. Subqueries that are used as tables can be used in the `FROM` clause. In this blog post we will focus on subqueries used as *expressions*. A future blog post will discuss subqueries as *tables*.

Subqueries as expressions exist in three forms.

* Scalar subqueries
* `EXISTS`
* `IN`/`ANY`/`ALL`

All of the subqueries can be either *correlated* or *uncorrelated*. An uncorrelated subquery is a query that is independent from the outer query. A correlated subquery is a subquery that contains expressions from the outer query. Correlated subqueries can be seen as *parameterized subqueries*.

#### Uncorrelated Scalar Subqueries

Uncorrelated scalar subqueries can only return *a single value*. That constant value is then substituted and used in the query. As an example of why this is useful - imagine that we want to select all of the shortest flights in our dataset. We could run the following query to obtain the shortest flight distance:

```sql
SELECT MIN(distance)
FROM ontime;
```

| min(distance) |
|---------------|
| 31.0          |

We could manually take this distance and use it in the `WHERE` clause to obtain all flights on this route.

```sql
SELECT uniquecarrier, origincityname, destcityname, flightdate
FROM ontime
WHERE distance=31.0;
```

| uniquecarrier | origincityname |  destcityname  | flightdate |
|---------------|----------------|----------------|------------|
| AS            | Petersburg, AK | Wrangell, AK   | 2017-01-15 |
| AS            | Wrangell, AK   | Petersburg, AK | 2017-01-15 |
| AS            | Petersburg, AK | Wrangell, AK   | 2017-01-16 |

However - this requires us to hardcode the constant inside the query. By using the first query as a *subquery* we can compute the minimum distance as part of the query.

```sql
SELECT uniquecarrier, origincityname, destcityname, flightdate
FROM ontime
WHERE distance=(
     SELECT MIN(distance)
     FROM ontime
);
```


#### Correlated Scalar Subqueries

While uncorrelated subqueries are powerful, they come with a hard restriction: only a *single value* can be returned. Often, what we want to do is *parameterize* the query, so that we can return different values per row.

For example, suppose that we want to find all of the shortest flights *for each carrier*. We can find the shortest flight for a *specific carrier* using the following parameterized query:

```sql
PREPARE min_distance_per_carrier AS
SELECT MIN(distance)
FROM ontime
WHERE uniquecarrier=$1;
```

We can execute this prepared statement to obtain the minimum distance for a specific carrier.

```sql
EXECUTE min_distance_per_carrier('UA');
```

| min(distance) |
|---------------|
| 67.0          |

If we want to use this parameterized query as a subquery, we need to use a *correlated subquery*. Correlated subqueries allow us to use parameterized queries as scalar subqueries by referencing columns from *the outer query*. We can obtain the set of shortest flights per carrier using the following query:

```sql
SELECT uniquecarrier, origincityname, destcityname, flightdate, distance
FROM ontime AS ontime_outer
WHERE distance=(
     SELECT MIN(distance)
     FROM ontime
     WHERE uniquecarrier=ontime_outer.uniquecarrier
);
```
| uniquecarrier |    origincityname    |     destcityname     | flightdate | distance |
|---------------|----------------------|----------------------|------------|----------|
| AS            | Wrangell, AK         | Petersburg, AK       | 2017-01-01 | 31.0     |
| NK            | Fort Lauderdale, FL  | Orlando, FL          | 2017-01-01 | 177.0    |
| VX            | Las Vegas, NV        | Los Angeles, CA      | 2017-01-01 | 236.0    |


Notice how the column from the *outer* relation (`ontime_outer`) is used *inside* the query. This is what turns the subquery into a *correlated subquery*. The column from the outer relation (`ontime_outer.uniquecarrier`) is a *parameter* for the subquery. Logically the subquery is executed once for every row that is present in `ontime`, where the value for the column at that row is substituted as a parameter.

In order to make it more clear that the correlated subquery is in essence a *parameterized query*, we can create a scalar macro that contains the query using DuckDB's [macros](/docs/sql/statements/create_macro.html).

```sql
CREATE MACRO min_distance_per_carrier(param) AS (
     SELECT MIN(distance)
     FROM ontime
     WHERE uniquecarrier=param
);
```

We can then use the macro in our original query as if it is a function.

```sql
SELECT uniquecarrier, origincityname, destcityname, flightdate, distance
FROM ontime AS ontime_outer
WHERE distance=min_distance_per_carrier(ontime_outer.uniquecarrier);
```

This gives us the same result as placing the correlated subquery inside of the query, but is cleaner as we can decompose the query into multiple segments more effectively.

#### EXISTS

`EXISTS` can be used to check if a given subquery has any results. This is powerful when used as a correlated subquery. For example, we can use `EXISTS` if we want to obtain the *last flight that has been flown on each route*. 

We can obtain a list of all flights on a given route past a certain date using the following query:

```sql
PREPARE flights_after_date AS
SELECT uniquecarrier, origincityname, destcityname, flightdate, distance
FROM ontime
WHERE origin=$1 AND dest=$2 AND flightdate>$3;
```

```sql
EXECUTE flights_after_date('LAX', 'JFK', DATE '2017-05-01');
```

| uniquecarrier | origincityname  | destcityname | flightdate | distance |
|---------------|-----------------|--------------|------------|----------|
| AA            | Los Angeles, CA | New York, NY | 2017-08-01 | 2475.0   |
| AA            | Los Angeles, CA | New York, NY | 2017-08-02 | 2475.0   |
| AA            | Los Angeles, CA | New York, NY | 2017-08-03 | 2475.0   |

Now in order to obtain the *last flight on a route*, we need to find flights *for which no later flight exists*.

```sql
SELECT uniquecarrier, origincityname, destcityname, flightdate, distance
FROM ontime AS ontime_outer
WHERE NOT EXISTS (
     SELECT uniquecarrier, origincityname, destcityname, flightdate, distance
     FROM ontime
     WHERE origin=ontime_outer.origin AND dest=ontime_outer.dest AND flightdate>ontime_outer.flightdate
);
```

| uniquecarrier |           origincityname           |            destcityname            | flightdate | distance |
|---------------|------------------------------------|------------------------------------|------------|----------|
| AA            | Daytona Beach, FL                  | Charlotte, NC                      | 2017-02-27 | 416.0    |
| EV            | Abilene, TX                        | Dallas/Fort Worth, TX              | 2017-02-15 | 158.0    ||
| EV            | Dallas/Fort Worth, TX              | Durango, CO                        | 2017-02-13 | 674.0    |

#### IN / ANY / ALL

`IN` can be used to check if a *given value* exists within the result returned by the subquery. For example, we can obtain a list of all carriers that have performed more than `250 000` flights in the dataset using the following query:

```sql
SELECT uniquecarrier
FROM ontime
GROUP BY uniquecarrier
HAVING COUNT(*) > 250000;
```

We can then use an `IN` clause to obtain all flights performed by those carriers.

```sql
SELECT *
FROM ontime
WHERE uniquecarrier IN (
     SELECT uniquecarrier
     FROM ontime
     GROUP BY uniquecarrier
     HAVING COUNT(*) > 250000
);
```

A correlated subquery can be useful here if we want to not count the total amount of flights performed by each carrier, but count the total amount of flights *for the given route*. We can select all flights performed by carriers that have performed *at least 1000 flights on a given route* using the following query.

```sql
SELECT *
FROM ontime AS ontime_outer
WHERE uniquecarrier IN (
     SELECT uniquecarrier
     FROM ontime
     WHERE ontime.origin=ontime_outer.origin AND ontime.dest=ontime_outer.dest
     GROUP BY uniquecarrier
     HAVING COUNT(*) > 1000
);
```

`ANY` and `ALL` are generalizations of `IN`. `IN` checks if the value is present in the set returned by the subquery. This is equivalent to `= ANY(...)`. The `ANY` and `ALL` operators can be used to perform other comparison operators (such as `>`, `<`, `<>`). The above query can be rewritten to `ANY` in the following form.

```sql
SELECT *
FROM ontime AS ontime_outer
WHERE uniquecarrier = ANY (
     SELECT uniquecarrier
     FROM ontime
     WHERE ontime.origin=ontime_outer.origin AND ontime.dest=ontime_outer.dest
     GROUP BY uniquecarrier
     HAVING COUNT(*) > 1000
);
```

#### Performance

Logically, correlated subqueries are executed *once per row*. As such, it is natural to think that correlated subqueries are very expensive and should be avoided for performance reasons.

While that is true in many SQL systems, it is not the case in DuckDB. In DuckDB, subqueries are **always** *decorrelated*. DuckDB uses a state-of-the-art subquery decorrelation algorithm as described in the [Unnesting Arbitrary Queries](https://cs.emis.de/LNI/Proceedings/Proceedings241/383.pdf) paper. This allows all subqueries to be decorrelated and executed as a single, much more efficient, query.

If we look at the query plan for the correlated scalar subquery using `EXPLAIN`, we can see that the query has been transformed into a hash aggregate followed by a hash join. This allows the query to be executed very efficiently.

```sql
EXPLAIN SELECT uniquecarrier, origincityname, destcityname, flightdate, distance
FROM ontime AS ontime_outer
WHERE distance=(
     SELECT MIN(distance)
     FROM ontime
     WHERE uniquecarrier=ontime_outer.uniquecarrier
);
```

```
┌───────────────────────────┐
│         HASH_JOIN         │ 
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │ 
│      uniquecarrier =      │ 
│       uniquecarrier       ├──────────────┐
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││       HASH_GROUP_BY       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           ontime          ││       uniquecarrier       │
└───────────────────────────┘│       min(distance)       │
                             └─────────────┬─────────────┘
                             ┌─────────────┴─────────────┐
                             │         SEQ_SCAN          │
                             │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
                             │           ontime          │
                             └───────────────────────────┘
                             
```

We can see the drastic performance difference that subquery decorrelation has when we compare the run-time of this query in DuckDB with the run-time in Postgres and SQLite. When running the above query on the [`ontime` dataset](https://www.transtats.bts.gov/Homepage.asp) for `2017` with roughly `~4 million` rows, we get the following performance results:

| DuckDB | Postgres | SQLite |
|--------|----------|--------|
| 0.06s  | >48 Hours    | >48 Hours  |


As Postgres and SQLite do not de-correlate the subquery, the query is not just *logically*, but *actually* executed once for every row. As the subquery involves a full table scan, this moves the query from linear complexity, O(n), to quadratic complexity, O(n<sup>2</sup>).

In this case, it is possible to manually decorrelate the query and generate the following SQL:

```sql
SELECT ontime.uniquecarrier, origincityname, destcityname, flightdate, distance
FROM ontime
JOIN (
     SELECT uniquecarrier, MIN(distance) AS min_distance
     FROM ontime
     GROUP BY uniquecarrier
) AS subquery 
ON (ontime.uniquecarrier=subquery.uniquecarrier AND distance=min_distance);
```

By performing the de-correlation manually, the performance of SQLite and Postgres improves significantly. However, both systems remain over 30x slower than DuckDB.

| DuckDB | Postgres | SQLite |
|--------|----------|--------|
| 0.06s  | 1.98s    | 2.81s  |

Note that while it is possible to manually decorrelate certain subqueries by rewriting the SQL, it is not always possible to do so. As described in the [Unnesting Arbitrary Queries paper](https://cs.emis.de/LNI/Proceedings/Proceedings241/383.pdf), special join types that are not present in SQL are necessary to decorrelate arbitrary queries.

In DuckDB, these special join types will be automatically generated by the system to decorrelate all subqueries. In fact, DuckDB does not have support for executing subqueries that are not decorrelated. All subqueries will be decorrelated before DuckDB executes them.

#### Conclusion

Subqueries are a very powerful tool that allow you to take arbitrary queries and convert them into ad-hoc functions. When used in combination with DuckDB's powerful subquery decorrelation, they can be executed extremely efficiently, making previously intractable queries not only possible, but fast.


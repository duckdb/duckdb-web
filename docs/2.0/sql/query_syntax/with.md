---
layout: docu
railroad: query_syntax/with.js
redirect_from:
- /docs/sql/query_syntax/with
- /docs/stable/sql/query_syntax/with
- /docs/current/sql/query_syntax/with
- /docs/lts/sql/query_syntax/with
- /docs/preview/sql/query_syntax/with
tested: true
title: WITH Clause
---

The `WITH` clause allows you to specify common table expressions (CTEs).
Regular (non-recursive) common-table-expressions are essentially views that are limited in scope to a particular query.
CTEs can reference each other and can be nested. [Recursive CTEs](#recursive-ctes) can reference themselves.

## Basic CTE Examples

Create a CTE called `cte` and use it in the main query:

```sql
WITH cte AS (SELECT 42 AS x)
SELECT * FROM cte;
```

| x  |
|---:|
| 42 |

Create two CTEs `cte1` and `cte2`, where the second CTE references the first CTE:

```sql
WITH
    cte1 AS (SELECT 42 AS i),
    cte2 AS (SELECT i * 100 AS x FROM cte1)
SELECT * FROM cte2;
```

|  x   |
|-----:|
| 4200 |

You can specify column names for CTEs:

```sql
WITH cte(j) AS (SELECT 42 AS i)
FROM cte;
```

## CTE Materialization

DuckDB handles CTEs as _materialized_ by default, meaning that the CTE is evaluated
once and the result is stored in a temporary table. However, under certain conditions,
DuckDB can _inline_ the CTE into the main query, which means that the CTE is not
materialized and its definition is duplicated in each place it is referenced.
Inlining is done using the following heuristics:
* The CTE is not referenced more than once.
* The CTE does not contain a `VOLATILE` function.
* The CTE is using `AS NOT MATERIALIZED` and does not use `AS MATERIALIZED`.
* The CTE does not perform a grouped aggregation.

Materialization can be explicitly activated by defining the CTE using `AS MATERIALIZED` and disabled by using `AS NOT MATERIALIZED`. Note that inlining is not always possible, even if the heuristics are met. For example, if the CTE contains a `read_csv` function, it cannot be inlined.

Take the following query for example, which invokes the same CTE three times:

```sql
WITH t(x) AS (⟨complex_query⟩)
SELECT *
FROM
    t AS t1,
    t AS t2,
    t AS t3;
```

Inlining duplicates the definition of `t` for each reference which results in the following query:

```sql
SELECT *
FROM
    (⟨complex_query⟩) AS t1(x),
    (⟨complex_query⟩) AS t2(x),
    (⟨complex_query⟩) AS t3(x);
```

If `complex_query` is expensive, materializing it with the `MATERIALIZED` keyword can improve performance. In this case, `complex_query` is evaluated only once.

```sql
WITH t(x) AS MATERIALIZED (⟨complex_query⟩)
SELECT *
FROM
    t AS t1,
    t AS t2,
    t AS t3;
```

If one wants to disable materialization, use `NOT MATERIALIZED`:

```sql
WITH t(x) AS NOT MATERIALIZED (⟨complex_query⟩)
SELECT *
FROM
    t AS t1,
    t AS t2,
    t AS t3;
```

Generally, it is not recommended to use explicit materialization hints, as DuckDB's query optimizer is capable of deciding when to materialize or inline a CTE based on the query structure and the heuristics mentioned above. However, in some cases, it may be beneficial to use `MATERIALIZED` or `NOT MATERIALIZED` to control the behavior explicitly.

## Data-Modifying CTEs

> New Support for data-modifying statements in CTEs was introduced in DuckDB 2.0.

A CTE body can be a data-modifying statement: [`INSERT`]({% link docs/2.0/sql/statements/insert.md %}), [`UPDATE`]({% link docs/2.0/sql/statements/update.md %}), [`DELETE`]({% link docs/2.0/sql/statements/delete.md %}), or [`COPY`]({% link docs/2.0/sql/statements/copy.md %}#copy--to). This lets you chain modifications into a single pipeline. A data-modifying CTE that is followed by other statements should use a [`RETURNING` clause]({% link docs/2.0/sql/statements/insert.md %}#returning-clause) so that its result can be referenced.

Move rows from one table to another in a single statement by combining a `DELETE` and an `INSERT`:

```sql
WITH moved AS MATERIALIZED (
    DELETE FROM staging
    RETURNING *
)
INSERT INTO archive
SELECT * FROM moved;
```

Count the rows affected by an `UPDATE`:

```sql
WITH updated AS (
    UPDATE orders
    SET status = 'shipped'
    WHERE status = 'ready'
    RETURNING *
)
SELECT count(*) AS shipped FROM updated;
```

> Bestpractice Mark a data-modifying CTE as [`MATERIALIZED`](#cte-materialization) when later parts of the query depend on the modification having already run, so that it is not inlined or executed more than once.

## Recursive CTEs

`WITH RECURSIVE` allows the definition of CTEs which can refer to themselves. Note that the query must be formulated in a way that ensures termination, otherwise, it may run into an infinite loop.

### Example: Fibonacci Sequence

`WITH RECURSIVE` can be used to make recursive calculations. For example, here is how `WITH RECURSIVE` could be used to calculate the first ten Fibonacci numbers:

```sql
WITH RECURSIVE FibonacciNumbers (
    RecursionDepth, FibonacciNumber, NextNumber
) AS (
        -- Base case
        SELECT
            0 AS RecursionDepth,
            0 AS FibonacciNumber,
            1 AS NextNumber
        UNION ALL
        -- Recursive step
        SELECT
            fib.RecursionDepth + 1 AS RecursionDepth,
            fib.NextNumber AS FibonacciNumber,
            fib.FibonacciNumber + fib.NextNumber AS NextNumber
        FROM
            FibonacciNumbers fib
        WHERE
            fib.RecursionDepth + 1 < 10
    )
SELECT
    fn.RecursionDepth AS FibonacciNumberIndex,
    fn.FibonacciNumber
FROM
    FibonacciNumbers fn;
```

| FibonacciNumberIndex | FibonacciNumber |
|---------------------:|----------------:|
| 0                    | 0               |
| 1                    | 1               |
| 2                    | 1               |
| 3                    | 2               |
| 4                    | 3               |
| 5                    | 5               |
| 6                    | 8               |
| 7                    | 13              |
| 8                    | 21              |
| 9                    | 34              |

### Example: Tree Traversal

`WITH RECURSIVE` can be used to traverse trees. For example, take a hierarchy of tags:

<img src="/images/examples/with-recursive-tree-example-light.svg" alt="Example graph" style="width: 700px; text-align: center" class="lightmode-img">
<img src="/images/examples/with-recursive-tree-example-dark.svg" alt="Example graph" style="width: 700px; text-align: center" class="darkmode-img">

```sql
CREATE TABLE tag (id INTEGER, name VARCHAR, subclassof INTEGER);
INSERT INTO tag VALUES
    (1, 'U2',     5),
    (2, 'Blur',   5),
    (3, 'Oasis',  5),
    (4, '2Pac',   6),
    (5, 'Rock',   7),
    (6, 'Rap',    7),
    (7, 'Music',  9),
    (8, 'Movies', 9),
    (9, 'Art', NULL);
```

The following query returns the path from the node `Oasis` to the root of the tree (`Art`).

```sql
WITH RECURSIVE tag_hierarchy(id, source, path) AS (
        SELECT id, name, [name] AS path
        FROM tag
        WHERE subclassof IS NULL
    UNION ALL
        SELECT tag.id, tag.name, list_prepend(tag.name, tag_hierarchy.path)
        FROM tag, tag_hierarchy
        WHERE tag.subclassof = tag_hierarchy.id
    )
SELECT path
FROM tag_hierarchy
WHERE source = 'Oasis';
```

|           path            |
|---------------------------|
| [Oasis, Rock, Music, Art] |

### Graph Traversal

The `WITH RECURSIVE` clause can be used to express graph traversal on arbitrary graphs. However, if the graph has cycles, the query must perform cycle detection to prevent infinite loops.
One way to achieve this is to store the path of a traversal in a [list]({% link docs/2.0/sql/data_types/list.md %}) and, before extending the path with a new edge, check whether its endpoint has been visited before (see the example later).

Take the following directed graph from the [LDBC Graphalytics benchmark](https://arxiv.org/pdf/2011.15028.pdf):

<img src="/images/examples/with-recursive-graph-example-light.svg" alt="Example graph" style="width: 700px; text-align: center" class="lightmode-img">
<img src="/images/examples/with-recursive-graph-example-dark.svg" alt="Example graph" style="width: 700px; text-align: center" class="darkmode-img">

```sql
CREATE TABLE edge (node1id INTEGER, node2id INTEGER);
INSERT INTO edge VALUES
    (1, 3), (1, 5), (2, 4), (2, 5), (2, 10), (3, 1),
    (3, 5), (3, 8), (3, 10), (5, 3), (5, 4), (5, 8),
    (6, 3), (6, 4), (7, 4), (8, 1), (9, 4);
```

Note that the graph contains directed cycles, e.g., between nodes 1, 5 and 8.

#### Enumerate All Paths from a Node

The following query returns **all paths** starting in node 1:

```sql
WITH RECURSIVE paths(startNode, endNode, path) AS (
        SELECT -- Define the path as the first edge of the traversal
            node1id AS startNode,
            node2id AS endNode,
            [node1id, node2id] AS path
        FROM edge
        WHERE startNode = 1
        UNION ALL
        SELECT -- Concatenate new edge to the path
            paths.startNode AS startNode,
            node2id AS endNode,
            array_append(path, node2id) AS path
        FROM paths
        JOIN edge ON paths.endNode = node1id
        -- Prevent adding a repeated node to the path.
        -- This ensures that no cycles occur.
        WHERE list_position(paths.path, node2id) IS NULL
    )
SELECT startNode, endNode, path
FROM paths
ORDER BY length(path), path;
```

| startNode | endNode |     path      |
|----------:|--------:|---------------|
| 1         | 3       | [1, 3]        |
| 1         | 5       | [1, 5]        |
| 1         | 5       | [1, 3, 5]     |
| 1         | 8       | [1, 3, 8]     |
| 1         | 10      | [1, 3, 10]    |
| 1         | 3       | [1, 5, 3]     |
| 1         | 4       | [1, 5, 4]     |
| 1         | 8       | [1, 5, 8]     |
| 1         | 4       | [1, 3, 5, 4]  |
| 1         | 8       | [1, 3, 5, 8]  |
| 1         | 8       | [1, 5, 3, 8]  |
| 1         | 10      | [1, 5, 3, 10] |

Note that the result of this query is not restricted to shortest paths, e.g., for node 5, the results include paths `[1, 5]` and `[1, 3, 5]`.

#### Enumerate Unweighted Shortest Paths from a Node

In most cases, enumerating all paths is not practical or feasible. Instead, only the **(unweighted) shortest paths** are of interest. To find these, the second half of the `WITH RECURSIVE` query should be adjusted such that it only includes a node if it has not yet been visited. This is implemented by using a subquery that checks if any of the previous paths includes the node:

```sql
WITH RECURSIVE paths(startNode, endNode, path) AS (
        SELECT -- Define the path as the first edge of the traversal
            node1id AS startNode,
            node2id AS endNode,
            [node1id, node2id] AS path
        FROM edge
        WHERE startNode = 1
        UNION ALL
        SELECT -- Concatenate new edge to the path
            paths.startNode AS startNode,
            node2id AS endNode,
            array_append(path, node2id) AS path
        FROM paths
        JOIN edge ON paths.endNode = node1id
        -- Prevent adding a node that was visited previously by any path.
        -- This ensures that (1) no cycles occur and (2) only nodes that
        -- were not visited by previous (shorter) paths are added to a path.
        WHERE NOT EXISTS (
                FROM paths previous_paths
                WHERE list_contains(previous_paths.path, node2id)
              )
    )
SELECT startNode, endNode, path
FROM paths
ORDER BY length(path), path;
```

| startNode | endNode |    path    |
|----------:|--------:|------------|
| 1         | 3       | [1, 3]     |
| 1         | 5       | [1, 5]     |
| 1         | 8       | [1, 3, 8]  |
| 1         | 10      | [1, 3, 10] |
| 1         | 4       | [1, 5, 4]  |
| 1         | 8       | [1, 5, 8]  |

#### Enumerate Unweighted Shortest Paths between Two Nodes

`WITH RECURSIVE` can also be used to find **all (unweighted) shortest paths between two nodes**. To ensure that the recursive query is stopped as soon as we reach the end node, we use a [window function]({% link docs/2.0/sql/functions/window_functions.md %}) which checks whether the end node is among the newly added nodes.

The following query returns all unweighted shortest paths between nodes 1 (start node) and 8 (end node):

```sql
WITH RECURSIVE paths(startNode, endNode, path, endReached) AS (
   SELECT -- Define the path as the first edge of the traversal
        node1id AS startNode,
        node2id AS endNode,
        [node1id, node2id] AS path,
        (node2id = 8) AS endReached
     FROM edge
     WHERE startNode = 1
   UNION ALL
   SELECT -- Concatenate new edge to the path
        paths.startNode AS startNode,
        node2id AS endNode,
        array_append(path, node2id) AS path,
        max(CASE WHEN node2id = 8 THEN 1 ELSE 0 END)
            OVER (ROWS BETWEEN UNBOUNDED PRECEDING
                           AND UNBOUNDED FOLLOWING) AS endReached
     FROM paths
     JOIN edge ON paths.endNode = node1id
    WHERE NOT EXISTS (
            FROM paths previous_paths
            WHERE list_contains(previous_paths.path, node2id)
          )
      AND paths.endReached = 0
)
SELECT startNode, endNode, path
FROM paths
WHERE endNode = 8
ORDER BY length(path), path;
```

| startNode | endNode |   path    |
|----------:|--------:|-----------|
| 1         | 8       | [1, 3, 8] |
| 1         | 8       | [1, 5, 8] |

### Accessing the Union Table with `recurring`

Within the recursive term of a `WITH RECURSIVE` CTE, the CTE name (e.g., `counter`) refers to the rows produced by the *last iteration*. To access *all rows accumulated so far* (the union table), use the `recurring` schema prefix:

```sql
WITH RECURSIVE counter(i) AS (
    SELECT 1
        UNION ALL
    SELECT i + 1
    FROM counter
    WHERE (SELECT max(i) FROM recurring.counter) < 5
)
SELECT *
FROM counter;
```

| i |
|--:|
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |

Here, `recurring.counter` gives access to all rows accumulated across all previous iterations, while `counter` in the `FROM` clause only contains the rows from the most recent iteration. This is useful when termination conditions or calculations depend on the full accumulated result rather than just the previous iteration.

## Recursive CTEs with `USING KEY`

> Update DuckDB 1.5.0 deprecated recursive `UNION`s in `USING KEY` CTEs because they behaved identically to `UNION ALL`. DuckDB 2.0.0 gives the two keywords distinct meanings and supports both: `UNION ALL` forwards every candidate row to the next iteration, while `UNION` only forwards new or changed keys. See [`UNION` vs. `UNION ALL` in `USING KEY` CTEs](#union-vs-union-all-in-using-key-ctes). The `deprecated_using_key_syntax` setting was removed.

`USING KEY` alters the behavior of a regular recursive CTE.

In each iteration, a regular recursive CTE appends result rows to the union table, which ultimately defines the overall result of the CTE. In contrast, a CTE with `USING KEY` has the ability to update rows that have been placed in the union table in an earlier iteration: if the current iteration produces a row with key `k`, it replaces a row with the same key `k` in the union table (like a dictionary). If no such row exists in the union table yet, the new row is appended to the union table as usual.

This allows a CTE to exercise fine-grained control over the union table contents. Avoiding the append-only behavior can lead to significantly smaller union table sizes. This helps query runtime, memory consumption, and makes it feasible to access the union table while the iteration is still ongoing. In a CTE `WITH RECURSIVE T(...) USING KEY ...`, table `T` denotes the rows added by the last iteration (as is usual for recursive CTEs), while table `recurring.T` denotes the [union table built so far](#accessing-the-union-table-with-recurring). References to `recurring.T` allow for the elegant and idiomatic translation of rather complex algorithms into readable SQL code.

### Example: `USING KEY`

This is a recursive CTE where `USING KEY` has a key column (`a`) and a payload column (`b`).
The payload columns correspond to the columns to be overwritten.
In the first iteration we have two different keys, `1` and `2`.
These two keys will generate two new rows, `(1, 3)` and `(2, 4)`.
In the next iteration we produce a new key, `3`, which generates a new row.
We also generate the row `(2, 3)`, where `2` is a key that already exists from the previous iteration.
This will overwrite the old payload `4` with the new payload `3`.

```sql
WITH RECURSIVE tbl(a, b) USING KEY (a) AS (
    SELECT a, b
    FROM (VALUES (1, 3), (2, 4)) t(a, b)
        UNION ALL
    SELECT a + 1, b
    FROM tbl
    WHERE a < 3
)
SELECT *
FROM tbl;
```

| a | b |
|--:|--:|
| 1 | 3 |
| 2 | 3 |
| 3 | 3 |

### Aggregate Payloads in `USING KEY`

By default, each payload column (i.e., each column not listed in `USING KEY`) uses `last` semantics: a new row for an existing key overwrites the previous payload value. You can also specify an aggregate function for a payload column in the `USING KEY` clause. In this case, all rows produced for a key are combined using the aggregate function. Payload columns without an aggregate keep the default `last` semantics.

For example, the following query computes the average of all values produced for key `1`:

```sql
WITH RECURSIVE tbl(a, b) USING KEY (a, avg(b)) AS (
    SELECT 1, 5
        UNION ALL
    SELECT a, b - 1
    FROM tbl
    WHERE b > 0
)
TABLE tbl;
```

| a |  b  |
|--:|----:|
| 1 | 2.5 |

The following query maintains the maximum of `b`, while `c` uses the default `last` semantics:

```sql
WITH RECURSIVE tbl(a, b, c) USING KEY (a, max(b)) AS (
    SELECT 1, 5, 'x'
        UNION ALL
    SELECT a, b - 1, 'y'
    FROM tbl
    WHERE b > 0
)
TABLE tbl;
```

| a | b | c |
|--:|--:|---|
| 1 | 5 | y |

### `UNION` vs. `UNION ALL` in `USING KEY` CTEs

Both `UNION` and `UNION ALL` update the union table in the same way: all rows produced by an iteration (the candidates) are applied to the union table, i.e., they insert new keys, overwrite payloads or are combined by the payload aggregates. The two forms differ in which rows are passed to the next iteration:

* With `UNION ALL`, every candidate row produced by the recursive term is forwarded to the next iteration, even if it did not change the union table.
* With `UNION`, only rows for keys that are new or whose (finalized) payload changed are forwarded to the next iteration. Therefore, the recursion stops once the union table stops changing.

For example, the following query computes single-source shortest paths in a weighted graph that contains a cycle. Using `min(dist)` as the payload aggregate, the union table keeps the shortest distance found so far for each node. With `UNION`, the recursion terminates once no shorter distances are found. With `UNION ALL`, the query would not terminate, as candidates would continue to be forwarded around the cycle.

```sql
CREATE TABLE weighted_edges (src INTEGER, dst INTEGER, weight INTEGER);
INSERT INTO weighted_edges VALUES
    (1, 2, 4), (1, 3, 1), (3, 2, 1), (2, 4, 1), (3, 4, 5), (4, 1, 1);
```

```sql
WITH RECURSIVE shortest_paths(node, dist) USING KEY (node, min(dist)) AS (
    SELECT 1, 0
        UNION
    SELECT e.dst, sp.dist + e.weight
    FROM shortest_paths AS sp
    JOIN weighted_edges AS e ON e.src = sp.node
)
SELECT *
FROM shortest_paths
ORDER BY node;
```

| node | dist |
|-----:|-----:|
| 1    | 0    |
| 2    | 2    |
| 3    | 1    |
| 4    | 3    |

For more details on the semantics and the implementation, see the [“How DuckDB Runs Recursive CTEs Faster” blog post]({% post_url 2026-08-25-how-duckdb-runs-recursive-ctes-faster %}).

## Using `VALUES`

You can use the `VALUES` clause for the initial (anchor) part of the CTE:

```sql
WITH RECURSIVE tbl(a, b) USING KEY (a) AS (
    VALUES (1, 3), (2, 4)
        UNION ALL
    SELECT a + 1, b
    FROM tbl
    WHERE a < 3
)
SELECT *
FROM tbl;
```

### Example: `USING KEY` References Union Table

As well as using the union table as a dictionary, we can now reference it in queries. This allows you to use results from not just the previous iteration, but also earlier ones. This new feature makes certain algorithms easier to implement.

One example is the connected components algorithm. For each node, the algorithm determines the node with the lowest ID to which it is connected. To achieve this, we use the entries in the union table to track the lowest ID found for a node. If a new incoming row contains a lower ID, we update this value.

<img src="/images/examples/using-key-graph-example-light.svg" alt="Example graph" style="width: 700px; text-align: center" class="lightmode-img">
<img src="/images/examples/using-key-graph-example-dark.svg" alt="Example graph" style="width: 700px; text-align: center" class="darkmode-img">

```sql
CREATE TABLE nodes (id INTEGER);
INSERT INTO nodes VALUES (1), (2), (3), (4), (5), (6), (7), (8);
CREATE TABLE edges (node1id INTEGER, node2id INTEGER);
INSERT INTO edges VALUES
    (1, 3), (2, 3), (3, 7), (7, 8), (5, 4), (6, 4);
```

```sql
WITH RECURSIVE connected_components(id, comp) USING KEY (id) AS (
    SELECT n.id, n.id AS comp
    FROM nodes AS n
        UNION ALL (
    SELECT DISTINCT ON (previous_iter.id) previous_iter.id, initial_iter.comp
    FROM 
        recurring.connected_components AS previous_iter,
        connected_components AS initial_iter,
        edges AS e
    WHERE ((e.node1id, e.node2id) = (previous_iter.id, initial_iter.id)
       OR (e.node2id, e.node1id) = (previous_iter.id, initial_iter.id))
      AND initial_iter.comp < previous_iter.comp
    ORDER BY initial_iter.id ASC, previous_iter.comp ASC)
)
TABLE connected_components
ORDER BY id;
```

| id | comp |
|---:|-----:|
| 1  | 1    |
| 2  | 1    |
| 3  | 1    |
| 4  | 4    |
| 5  | 4    |
| 6  | 4    |
| 7  | 1    |
| 8  | 1    |

## Limitations

DuckDB does not support mutually recursive CTEs. See the [related issue and discussion in the DuckDB repository](https://github.com/duckdb/duckdb/issues/14716#issuecomment-2467952456).

## Syntax

<div id="rrdiagram"></div>

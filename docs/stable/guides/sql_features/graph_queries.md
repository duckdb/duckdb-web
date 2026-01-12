---
layout: docu
title: Graph Queries
---

DuckDB supports graph queries via the [DuckPGQ community extension](https://duckpgq.org), which implements the SQL/PGQ syntax from the SQL:2023 standard.

Graph queries allow you to find patterns and paths in connected data, such as social networks, financial transactions, or knowledge graphs, using a visual, intuitive syntax.

> Warning DuckPGQ is a community extension and is still under active development. Some features may be incomplete. See the [DuckPGQ website](https://duckpgq.org) for the latest status.

## Installing DuckPGQ

```sql
INSTALL duckpgq FROM community;
LOAD duckpgq;
```

## Creating a Property Graph

A property graph consists of vertices (nodes) and edges (relationships). You create one as a layer on top of existing tables:

```sql
CREATE TABLE Person (id BIGINT, name VARCHAR);
CREATE TABLE Knows (person1_id BIGINT, person2_id BIGINT, since DATE);

INSERT INTO Person VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO Knows VALUES (1, 2, '2020-01-01'), (2, 3, '2021-06-15');

CREATE PROPERTY GRAPH social_network
VERTEX TABLES (
    Person
)
EDGE TABLES (
    Knows
        SOURCE KEY (person1_id) REFERENCES Person (id)
        DESTINATION KEY (person2_id) REFERENCES Person (id)
);
```

## Pattern Matching

Use the `GRAPH_TABLE` function with `MATCH` to find patterns. The syntax uses `()` for nodes and `[]` for edges:

```sql
FROM GRAPH_TABLE (social_network
    MATCH (a:Person)-[k:Knows]->(b:Person)
    COLUMNS (a.name AS person1, b.name AS person2, k.since)
);
```

| person1 | person2 | since      |
|---------|---------|------------|
| Alice   | Bob     | 2020-01-01 |
| Bob     | Charlie | 2021-06-15 |

## Path Finding

Find paths of variable length using quantifiers like `{1,5}` (1 to 5 hops) or `+` (one or more):

```sql
FROM GRAPH_TABLE (social_network
    MATCH p = ANY SHORTEST (a:Person)-[k:Knows]->{1,3}(b:Person)
    WHERE a.name = 'Alice' AND b.name = 'Charlie'
    COLUMNS (a.name AS start_person, b.name AS end_person, path_length(p) AS hops)
);
```

| start_person | end_person | hops |
|--------------|------------|------|
| Alice        | Charlie    | 2    |

## Graph Algorithms

> Warning Graph algorithm functions require DuckDB v1.4.3 or later due to a [known issue](https://github.com/cwida/duckpgq-extension/issues/283). Earlier versions will return a `csr_cte does not exist` error.

DuckPGQ includes built-in graph algorithms:

| Function | Description |
|----------|-------------|
| `pagerank(graph, vertex_label, edge_label)` | Computes PageRank centrality scores |
| `local_clustering_coefficient(graph, vertex_label, edge_label)` | Measures how connected a node's neighbors are |
| `weakly_connected_component(graph, vertex_label, edge_label)` | Identifies connected components |

Example:

```sql
FROM pagerank(social_network, Person, Knows);
```

## Use Case: Financial Fraud Detection

Graph queries excel at finding suspicious patterns in financial data. See the ["Uncovering Financial Crime with DuckDB and Graph Queries" blog post]({% post_url 2025-10-22-duckdb-graph-queries-duckpgq %}) for a detailed example of detecting money laundering patterns.

## Cleanup

To remove a property graph:

```sql
DROP PROPERTY GRAPH social_network;
```

## Further Reading

* [DuckPGQ Documentation](https://duckpgq.org)
* [DuckPGQ Community Extension]({% link community_extensions/extensions/duckpgq.md %})
* ["Uncovering Financial Crime with DuckDB and Graph Queries" blog post]({% post_url 2025-10-22-duckdb-graph-queries-duckpgq %})

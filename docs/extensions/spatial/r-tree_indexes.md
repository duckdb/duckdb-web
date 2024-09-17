---
layout: docu
title: RTree Indexes
---

As of DuckDB v1.1.0 the `spatial` extension provides basic support for spatial indexing through the R-Tree extension index type.

## Why should I use an R-Tree index?

When working with geospatial datasets, it is very common that you want to filter rows based on their spatial relationship with a specific region of interest. Unfortunately, even though DuckDB's vectorized execution engine is pretty fast, this sort of operation does not scale very well to large datasets as it always requires a full table scan to check every row in the table. However, by indexing a table with an R-Tree, it is possible to accelerate these types of queries significantly. 

## How do R-Tree indexes work?

An R-Tree is a balanced tree data structure that stores the approximate _minimum bounding rectangle_ of each geometry (and the internal ID of the corresponding row) in the leaf nodes, and the bounding rectangle enclosing all of the child nodes in each internal node. 

> The _minimum bounding rectangle_ (MBR) of a geometry is the smallest rectangle that completely encloses the geometry. Usually when we talk about the bounding rectangle of a geometry (or the bounding "box" in the context of 2D geometry), we mean the minimum bounding rectangle. Additionally, we tend to assume that bounding boxes/rectangles are _axis-aligned_ i.e., the rectangle is __not__ rotated - the sides are always parallel to the coordinate axes. The MBR of a point is the point itself.

By traversing the R-Tree from top to bottom, it is possible to very quickly search a R-Tree-indexed table for only those rows where the indexed geometry column intersect a specific region of interest, as you can skip searching entire sub-trees if the bounding rectangles of their parent nodes don't intersect the query region at all. Once the leaf nodes are reached, only the specific rows whose geometries intersect the query region have to be fetched from disk, and the often much more expensive exact spatial predicate check (and any other filters) only have to be executed for these rows.

## What are the limitations of R-Tree indexes in DuckDB?

Before you get started using the R-Tree index, there are some limitations to be aware of:

- The R-Tree index is only supported for the `GEOMETRY` data type.
- The R-Tree index will only be used to perform "index scans" when the table is filtered (using a `WHERE` clause) with one of the following spatial predicate functions (as they all imply intersection): `ST_Equals`, `ST_Intersects`, `ST_Touches`, `ST_Crosses`, `ST_Within`, `ST_Contains`, `ST_Overlaps`, `ST_Covers`, `ST_CoveredBy`, `ST_ContainsProperly`.
- One of the arguments to the spatial predicate function must be a "constant" (i.e. a expression whose result is known at query planning time). This is because the query planner needs to know the bounding box of the query region _before_ the query itself is executed in order to use the R-Tree index scan. 

In the future we want to enable R-Tree indexes to be used to accelerate additional predicate functions and more complex queries such a spatial joins.

## How do I use R-Tree indexes in DuckDB

To create an R-Tree index, simply use the `CREATE INDEX` statement with the `USING RTREE` clause, passing the geometry column to index within the parentheses. For example:

```sql
-- Create a table with a geometry column
CREATE TABLE my_tbl (geom GEOMETRY);

-- Create an R-Tree index on the geometry column
CREATE INDEX my_idx ON my_table USING RTREE (geom);
```

You can also pass in additional options when creating an R-Tree index using the `WITH` clause to control the behavior of the R-Tree index. For example, to specify the maximum number of entries per node in the R-Tree, you can use the `max_node_capacity` option:

```sql
CREATE INDEX my_idx ON my_table USING RTREE (geom) WITH (max_node_capacity = 16);
```

The impact tweaking these options will have on performance is highly dependent on the system setup DuckDB is running on, the spatial distribution of the dataset, and the query patterns of your specific workload. The defaults should be good enough, but you if you want to experiment with different parameters, see the the [full list of options here](#options).

## Example

Here is an example that shows how to create an R-Tree index on a geometry column and where we can see that the `RTREE_INDEX_SCAN` operator is used when the table is filtered with a spatial predicate:

```sql

INSTALL spatial;
LOAD spatial;

-- Create a table with 10_000_000 random points
CREATE TABLE t1 AS SELECT point::GEOMETRY as geom
FROM st_generatepoints({min_x: 0, min_y: 0, max_x: 100, max_y: 100}::BOX_2D, 10_000, 1337);

-- Create an index on the table.
CREATE INDEX my_idx ON t1 USING RTREE (geom);

-- Perform a query with a "spatial predicate" on the indexed geometry column
-- Note how the second argument in this case, the ST_MakeEnvelope call is a "constant"
SELECT count(*) FROM t1 WHERE ST_Within(geom, ST_MakeEnvelope(45, 45, 65, 65));
----
390
```

We can check for ourselves that an R-Tree index scan is used by using the `EXPLAIN` statement:

```sql
EXPLAIN SELECT count(*) FROM t1 WHERE ST_Within(geom, ST_MakeEnvelope(45, 45, 65, 65));
----
┌───────────────────────────┐
│    UNGROUPED_AGGREGATE    │
│    ────────────────────   │
│        Aggregates:        │
│        count_star()       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│           FILTER          │
│    ────────────────────   │
│ ST_Within(geom, '...')    │ 
│                           │
│         ~2000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│     RTREE_INDEX_SCAN      │
│    ────────────────────   │
│   t1 (RTREE INDEX SCAN :  │
│           my_idx)         │
│                           │
│     Projections: geom     │
│                           │
│        ~10000 Rows        │
└───────────────────────────┘
```

## Performance considerations

### Bulk loading & Maintenance
Creating R-Trees on top of an already populated table is much faster than first creating the index and then inserting the data. This is because the R-Tree will have to periodically rebalance itself and perform a somewhat costly splitting operation when a node reaches max capacity after an insert, potentially causing additional splits to cascade up the tree. However, when the R-Tree index is created on an already populated table, a special bottom up "bulk loading algorithm" (Sort-Tile-Recursive) is used, which divides all entries into an already balanced tree as the total number of required nodes can be computed from the begining. 

Additionally, using the bulk loading algorithm tends to create a R-Tree with a better structure (less overlap between bounding boxes), which usually leads to better query performance. If you find that the performance of querying the R-Tree starts to deteriorate after a large number of of updates or deletions, dropping and re-creating the index might produce a higher quality R-Tree.

### Memory usage
Like DuckDB's built in ART-index, all the associated buffers containing the R-Tree will be lazily loaded from disk (when running DuckDB in disk-backed mode), but they are currently never unloaded unless the index is dropped. This means that if you end up scanning the entire index, the entire index will be loaded into memory and stay there for the duration of the database connection. However, all memory used by the R-Tree index (even during bulk-loading) is tracked by DuckDB, and will count towards the memory limit set by the `memory_limit` configuration parameter.

### Tuning
Depending on you specific workload, you might want to experiment with the `max_node_capacity` and `min_node_capacity` options to change the structure of the R-Tree and how it responds to insertions and deletions, see the [full list of options here](#options). In general, a tree with a higher total number of nodes (i.e. a lower `max_node_capacity`) _may_ result in a more granular structure that enables more aggressive pruning of sub-trees during query execution, but it will also require more memory to store the tree itself and be more punishing when querying larger regions as more internal nodes will have to be traversed.

## Options

The following options can be passed to the `WITH` clause when creating an R-Tree index: (e.g. `CREATE INDEX my_idx ON my_table USING RTREE (geom) WITH (<option> = <value>);`)

| Option               | Description                                                                                   | Default |
|----------------------|-----------------------------------------------------------------------------------------------|---------|
| `max_node_capacity` | The maximum number of entries per node in the R-Tree.                                         | `128`      |
| `min_node_capacity` | The minimum number of entries per node in the R-Tree.*                                         | `0.4 * max_node_capacity` |

*Should a node fall under the minimum number of entries after a deletion, the node will be dissolved and all the entries reinserted from the top of the tree. This is a common operation in R-Tree implementations to prevent the tree from becoming too unbalanced.



## R-Tree Table Functions

The `rtree_index_dump(VARCHAR)` table function can be used to return all the nodes within an R-Tree index which might come on handy when debugging, profiling or otherwise just inspecting the structure of the index. The function takes the name of the R-Tree index as an argument and returns a table with the following columns:

| Column Name | Type | Description |
|-------------|------|-------------|
| `level`     | `INTEGER` | The level of the node in the R-Tree. The root node has level 0. |
| `bounds`    | `BOX_2DF` | The bounding box of the node. |
| `row_id`    | `ROW_TYPE` | If this is a leaf node, the `rowid` of the row in the table, otherwise `NULL`. |


Example:

```sql
-- Create a table with 64 random points
CREATE TABLE t1 AS SELECT point::GEOMETRY as geom
FROM st_generatepoints({min_x: 0, min_y: 0, max_x: 100, max_y: 100}::BOX_2D, 64, 1337);

-- Create an R-Tree index on the geometry column (with a low max_node_capacity for demonstration purposes)
CREATE INDEX my_idx ON t1 USING RTREE (geom) WITH (max_node_capacity = 4);

-- Inspect the R-Tree index! Notice how the area of the bounding boxes of the branch nodes 
-- decreases as we go deeper into the tree.
SELECT 
  level, 
  bounds::GEOMETRY as geom, 
  CASE WHEN row_id IS NULL THEN st_area(geom) ELSE NULL END as area, 
  row_id, 
  CASE WHEN row_id IS NULL THEN 'branch' ELSE 'leaf' END as kind 
FROM rtree_index_dump('my_idx') 
ORDER BY area DESC;
----
┌───────┬──────────────────────────────┬────────────────────┬────────┬─────────┐
│ level │             geom             │        area        │ row_id │  kind   │
│ int32 │           geometry           │       double       │ int64  │ varchar │
├───────┼──────────────────────────────┼────────────────────┼────────┼─────────┤
│     0 │ POLYGON ((2.17285037040710…  │  3286.396482226409 │        │ branch  │
│     0 │ POLYGON ((6.00962591171264…  │  3193.725100864862 │        │ branch  │
│     0 │ POLYGON ((0.74995160102844…  │  3099.921458393704 │        │ branch  │
│     0 │ POLYGON ((14.6168870925903…  │ 2322.2760491675654 │        │ branch  │
│     1 │ POLYGON ((2.17285037040710…  │  604.1520104388514 │        │ branch  │
│     1 │ POLYGON ((26.6022186279296…  │  569.1665467030252 │        │ branch  │
│     1 │ POLYGON ((35.7942314147949…  │ 435.24662436250037 │        │ branch  │
│     1 │ POLYGON ((62.2643051147460…  │ 396.39027683023596 │        │ branch  │
│     1 │ POLYGON ((59.5225715637207…  │ 386.09153403820187 │        │ branch  │
│     1 │ POLYGON ((82.3060836791992…  │ 369.15115640929434 │        │ branch  │
│     · │              ·               │          ·         │      · │  ·      │
│     · │              ·               │          ·         │      · │  ·      │
│     · │              ·               │          ·         │      · │  ·      │
│     2 │ POLYGON ((20.5411434173584…  │                    │     35 │ leaf    │
│     2 │ POLYGON ((14.6168870925903…  │                    │     36 │ leaf    │
│     2 │ POLYGON ((43.7271652221679…  │                    │     39 │ leaf    │
│     2 │ POLYGON ((53.4629211425781…  │                    │     44 │ leaf    │
│     2 │ POLYGON ((26.6022186279296…  │                    │     62 │ leaf    │
│     2 │ POLYGON ((53.1732063293457…  │                    │     63 │ leaf    │
│     2 │ POLYGON ((78.1427154541015…  │                    │     10 │ leaf    │
│     2 │ POLYGON ((75.1728591918945…  │                    │     15 │ leaf    │
│     2 │ POLYGON ((62.2643051147460…  │                    │     42 │ leaf    │
│     2 │ POLYGON ((80.5032577514648…  │                    │     49 │ leaf    │
├───────┴──────────────────────────────┴────────────────────┴────────┴─────────┤
│ 84 rows (20 shown)                                                 5 columns │
└──────────────────────────────────────────────────────────────────────────────┘
```


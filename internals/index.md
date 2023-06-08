---
layout: docu
title: DuckDB Internals
selected: Internals
---
On this page is a brief description of the internals of the DuckDB engine.

## Parser
The parser converts a query string into the following tokens:

* [SQLStatement](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/parser/sql_statement.hpp)
* [QueryNode](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/parser/query_node.hpp)
* [TableRef](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/parser/tableref.hpp)
* [ParsedExpression](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/parser/parsed_expression.hpp)

The parser is not aware of the catalog or any other aspect of the database. It will not throw errors if tables do not exist, and will not resolve **any** types of columns yet. It only transforms a query string into a set of tokens as specified.

### ParsedExpression
The ParsedExpression represents an expression within a SQL statement. This can be e.g. a reference to a column, an addition operator or a constant value. The type of the ParsedExpression indicates what it represents, e.g. a comparison is represented as a [ComparisonExpression](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/parser/expression/comparison_expression.hpp).

ParsedExpressions do **not** have types, except for nodes with explicit types such as `CAST` statements. The types for expressions are resolved in the Binder, not in the Parser.

### TableRef
The TableRef represents any table source. This can be a reference to a base table, but it can also be a join, a table-producing function or a subquery.

### QueryNode
The QueryNode represents either (1) a `SELECT` statement, or (2) a set operation (i.e. `UNION`, `INTERSECT` or `DIFFERENCE`).

### SQL Statement
The SQLStatement represents a complete SQL statement. The type of the SQL Statement represents what kind of statement it is (e.g. StatementType::`SELECT` represents a `SELECT` statement). A single SQL string can be transformed into multiple SQL statements in case the original query string contains multiple queries.

# Binder
The binder converts all nodes into their **bound** equivalents. In the binder phase:
* The tables and columns are resolved using the catalog
* Types are resolved
* Aggregate/window functions are extracted

The following conversions happen:
* SQLStatement -> [BoundStatement](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/planner/bound_statement.hpp)
* QueryNode -> [BoundQueryNode](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/planner/bound_query_node.hpp)
* TableRef -> [BoundTableRef](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/planner/bound_tableref.hpp)
* ParsedExpression -> [Expression](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/planner/expression.hpp)

# Logical Planner
The logical planner creates [LogicalOperator](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/planner/logical_operator.hpp) nodes from the bound statements. In this phase, the actual logical query tree is created.

# Optimizer
After the logical planner has created the logical query tree, the optimizers are run over that query tree to create an optimized query plan. The following query optimizers are run:

* **Expression Rewriter**: Simplifies expressions, performs constant folding
* **Filter Pushdown**: Pushes filters down into the query plan and duplicates filters over equivalency sets. Also prunes subtrees that are guaranteed to be empty (because of filters that statically evaluate to false).
* **Join Order Optimizer**: Reorders joins using dynamic programming. Specifically, the `DPcpp` algorithm from the paper [Dynamic Programming Strikes Back](https://15721.courses.cs.cmu.edu/spring2017/papers/14-optimizer1/p539-moerkotte.pdf) is used.
* **Common Sub Expressions**: Extracts common subexpressions from projection and filter nodes to prevent unnecessary duplicate execution.
* **In Clause Rewriter**: Rewrites large static IN clauses to a MARK join or INNER join.

# Column Binding Resolver
The column binding resolver converts logical [BoundColumnRefExpresion](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/planner/expression/bound_columnref_expression.hpp) nodes that refer to a column of a specific table into [BoundReferenceExpression](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/planner/expression/bound_reference_expression.hpp) nodes that refer to a specific index into the DataChunks that are passed around in the execution engine.

# Physical Plan Generator
The physical plan generator converts the resulting logical operator tree into a [PhysicalOperator](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/execution/physical_operator.hpp) tree.

# Execution
In the execution phase, the physical operators are executed to produce the query result. The execution model is a vectorized volcano model, where [DataChunks](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/common/types/data_chunk.hpp) are pulled from the root node of the physical operator tree. Each PhysicalOperator itself defines how it grants its result. A [PhysicalTableScan](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/execution/operator/scan/physical_table_scan.hpp) node will pull the chunk from the base tables on disk, whereas a [PhysicalHashJoin](https://github.com/duckdb/duckdb/blob/master/src/include/duckdb/execution/operator/join/physical_hash_join.hpp) will perform a hash join between the output obtained from its child nodes.

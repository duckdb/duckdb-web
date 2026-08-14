---
layout: post
title: "Design and Implementation of DuckDB Internals"
author: "Torsten Grust (University of Tübingen)"
tags: ["Talk"]
thirdparty: true
highlighted: true
category: community
excerpt: ""
pill: "Lecture Notes"
redirect_from:
- /didi
---

This is a DuckDB-based course explaining the Design and Implementation of Database System Internals (“DiDi”).
The slides and auxiliary material are available in the [GitHub repository](https://github.com/DBatUTuebingen/DiDi).

## Overview

This lecture material has been developed by [Torsten Grust](https://db.cs.uni-tuebingen.de/grust/)
to support a 15-week course for undergraduate students of
the [Database Research Group](https://db.cs.uni-tuebingen.de) at
University of Tübingen (Germany).

## A Tour Through DuckDB's Internals

The course treads on a path through selected internals of the
[DuckDB](https://duckdb.org/) relational database system.  15 weeks
do not suffice to exhaustively discuss all interesting bits and pieces of the
DuckDB kernel. As of March 2026, the chapter layout reads as follows:

1. [Welcome & Setup](https://blobs.duckdb.org/slides/DiDi-01.pdf)
2. [The Query Performance Spectrum](https://blobs.duckdb.org/slides/DiDi-02.pdf)
3. [Managing Memory + Grouped Aggregation](https://blobs.duckdb.org/slides/DiDi-03.pdf)
4. [Sorting Large Tables](https://blobs.duckdb.org/slides/DiDi-04.pdf)
5. [The ART of Indexing](https://blobs.duckdb.org/slides/DiDi-05.pdf)
6. [Query Execution Plans and Pipelining](https://blobs.duckdb.org/slides/DiDi-06.pdf)
7. [Vectorized Query Execution](https://blobs.duckdb.org/slides/DiDi-07.pdf)
8. [Query Rewriting and Optimization](https://blobs.duckdb.org/slides/DiDi-08.pdf)

(You can also download the [DiDi slides concatenated into a single deck](https://blobs.duckdb.org/slides/DiDi.pdf))

You will need basic SQL skills to follow the course's red thread and
auxiliary material.  There are few queries that go beyond the core
`SELECT`-`FROM`-`WHERE`-`GROUP BY`-`HAVING` block, however.  Should
you require an introduction to the tabular data model and its
query language SQL, you may find the companion course
[*Tabular Database Systems*]({% link _library/2026-03-19-tabular-database-systems.md %}) helpful.

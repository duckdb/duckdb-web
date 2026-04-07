---
layout: post
title: "Design and Implementation of DuckDB Internals"
author: "Torsten Grust (University of Tübingen)"
tags: ["Talk"]
thirdparty: true
highlighted: true
excerpt: ""
pill: "Lecture Notes"
---

A DuckDB-based course on the Design and Implementation of Database System Internals.

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

1. Welcome & Setup
2. The Query Performance Spectrum
3. Managing Memory + Grouped Aggregation
4. Sorting Large Tables
5. The ART of Indexing
6. Query Execution Plans and Pipelining
7. Vectorized Query Execution
8. Query Rewriting and Optimization

You will need basic SQL skills to follow the course's red thread and
auxiliary material.  There are few queries that go beyond the core
`SELECT`-`FROM`-`WHERE`-`GROUP BY`-`HAVING` block, however.  Should
you require an introduction to the tabular data model and its
query language SQL, you may find the companion course
[*Tabular Database Systems*]({% link _library/2026-03-19-tabular-database-systems.md %}) helpful.

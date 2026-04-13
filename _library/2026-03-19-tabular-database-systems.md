---
layout: post
title: "Tabular Database Systems"
author: "Torsten Grust (University of Tübingen)"
tags: ["Talk"]
thirdparty: true
highlighted: true
excerpt: ""
pill: "Lecture Notes"
---

A DuckDB-based course on the fundamentals of relational database management systems and SQL.

The slides and auxiliary material are available in the [GitHub repository](https://github.com/DBatUTuebingen/TaDa).

## Overview

This lecture material has been developed by [Torsten Grust](https://db.cs.uni-tuebingen.de/grust/)
to support a 15-week course (coined *TaDa*) for undergraduate students of
the [Database Research Group](https://db.cs.uni-tuebingen.de) at
University of Tübingen (Germany).  You are welcome to use this
material in any way you may see fit: skim it, study it, send suggestions
or corrections, or tear it apart to build your own lecture material
based on it.  I would be delighted to hear from you in any case:

## A DuckDB-Based Introduction to Tabular Data and SQL

As a member of the decades-old family of relational database
management systems, [DuckDB](https://duckdb.org/) is an expert in
processing tabular data (or: tables, relations).   DuckDB is a
capable and very efficient
SQL database system that can
[crunch billions of rows on commodity laptops](https://blobs.duckdb.org/merch/duckdb-2024-big-data-on-your-laptop-poster.pdf).
Its SQL dialect is versatile, complete, and [remarkably *friendly*](https://duckdb.org/docs/current/sql/dialect/friendly_sql).
[DuckDB is a breeze to install](https://duckdb.org/install/) ~~and maintain~~,
open for tinkering and inspection, has developed an open and supportive community
since its inception in 2019,
and thus makes for an ideal vehicle for an introduction
into the world of contemporary tabular database system technology.

15 weeks hardly suffice to exhaustively cover a field that has developed
since the early 1970s, but I still hope that the topics covered in *TaDa*
will pave a path from which you can easily branch off to get lost in the depths
of [Ted Codd's](https://en.wikipedia.org/wiki/Edgar_F._Codd) jungle.
A future *TaDa* may see chapters added, merged, or removed but as of
March 2026, the chapter layout reads as follows:

1. Tabular Data and Database Systems
2. Tabular Data in CSV Files
3. Reading Data at the Speed of ~~Light~~Memory
4. Columnar Table Storage
5. Database-External Data in Parquet Files
6. The Structured Query Language (SQL)
7. More SQL (Subqueries + Embedded SQL)
8. SQL: Grouping + Aggregation and Functional Dependencies

We do not assume any prior SQL skills.  Chapters 03 and 07 will have you read
and modify short pieces of C, Python, or awk code.  There will be only
fleeting glimpses at the internals of DuckDB.  If the innards of The
Duck catch your interest, you may find the companion course
[*Design and Implementation of DuckDB Internals*]({% link _library/2026-03-19-design-and-implementation-of-duckdb-internals.md %}) on selected internals
of the DuckDB kernel helpful.

---
layout: default
title: Create Table
selected: Documentation/SQL/Create Table
expanded: SQL
railroad: createtable.js
---
# Create Table Statement
CREATE TABLE - this statement creates an empty table in the catalog.

### Examples
```sql
-- create a table with two integer columns (i and j)
CREATE TABLE t1(i INTEGER, j INTEGER);
-- create a table with a primary key
CREATE TABLE t1(id INTEGER PRIMARY KEY, j VARCHAR);
-- create a table with various different types
CREATE TABLE t1(i INTEGER NOT NULL, decimalnr DOUBLE, date DATE UNIQUE, time TIMESTAMP);
```

### Syntax
<div id="rrdiagram"></div>

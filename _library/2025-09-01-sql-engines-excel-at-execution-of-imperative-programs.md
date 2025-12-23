---
layout: post
title: "SQL Engines Excel at the Execution of Imperative Programs"
author: "Tim Fischer, Denis Hirn, Torsten Grust"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "VLDB 2025"
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol17/p4696-fischer.pdf)

Venue: VLDB 2025

## Abstract

SQL query engines can act as efficient runtime environments for the execution of imperative programs over database-resident tabular data. To make this point, we lay out the details of a compilation strategy that maps the basic blocks of arbitrarily branching and looping control flow graphs into plain—possibly recursive—SQL:1999 common table expressions. The compiler does not stumble when faced with imperative programs of several hundred lines and emits SQL code that can execute such programs over entire batches of input arguments. These batches create opportunities for parallel program evaluation which contemporary query decorrelation techniques exploit automatically. SQL engines that already support UDFs may find the present program execution approach to outperform their native implementation—SQL engines without such support may gain UDF capabilities without the need to build a dedicated interpreter.

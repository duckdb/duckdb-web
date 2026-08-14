---
layout: post
title: "Don't Hold My Data Hostage – A Case for Client Protocol Redesign"
author: "Mark Raasveldt, Hannes Mühleisen"
tags: ["Paper"]
thirdparty: false
excerpt: ""
pill: "VLDB 2017"
---

|-------|-------|
| **Paper** | [Don't Hold My Data Hostage – A Case for Client Protocol Redesign (PDF)](https://www.vldb.org/pvldb/vol10/p1022-muehleisen.pdf) |
| **Venue** | VLDB 2017 |

## Abstract

Transferring a large amount of data from a database to a client program is a surprisingly expensive operation. The time this requires can easily dominate the query execution time for large result sets. This represents a significant hurdle for external data analysis, for example when using statistical software. In this paper, we explore and analyse the result set serialization design space. We present experimental results from a large chunk of the database market and show the inefficiencies of current approaches. We then propose a columnar serialization method that improves transmission performance by an order of magnitude.

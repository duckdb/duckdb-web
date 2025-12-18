---
layout: post
title: "DuckPGQ: Bringing SQL/PGQ to DuckDB"
author: "Daniel ten Wolde, Gábor Szárnyas, Peter Boncz"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol16/p4034-wolde.pdf)

Venue: VLDB 2023

## Abstract

We demonstrate the most important new feature of SQL:2023, namely SQL/PGQ, which eases querying graphs using SQL by introducing new syntax for pattern matching and (shortest) path-finding. We show how support for SQL/PGQ can be integrated into an RDBMS, specifically in the DuckDB system, using an extension module called DuckPGQ. As such, we also demonstrate the use of the DuckDB extensibility mechanism, which allows us to add new functions, data types, operators, optimizer rules, storage systems, and even parsers to DuckDB. We also describe the new data structures and algorithms that the DuckPGQ module is based on, and how they are injected into SQL plans. While the demonstrated DuckPGQ extension module is lean and efficient, we sketch a roadmap to (i) improve its performance through new algorithms (factorized and WCOJ) and better parallelism and (ii) extend its functionality to scenarios beyond SQL, e.g., building and analyzing Graph Neural Networks.

## Implementation

`DuckPGQ` has been implemented as a community extension.
For details on how to use the extension, please refer to the [documentation]({% link community_extensions/extensions/duckpgq.md %}).

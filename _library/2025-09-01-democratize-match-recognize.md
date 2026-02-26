---
layout: post
title: "Democratize MATCH_RECOGNIZE!"
author: "Louisa Lambrecht, Tim Findling, Samuel Heid, Marcel Knüdeler, Torsten Grust"
thumb: "/images/library/thumbs/vldb.svg"
image: "/images/library/thumbs/vldb.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "VLDB 2025"
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol18/p5251-lambrecht.pdf)

Venue: VLDB 2025

## Abstract

_Row pattern matching_ in terms of the `MATCH_RECOGNIZE` clause is a powerful and relatively recent feature in SQL that allows users to define regular patterns over ordered rows in a table. As of today, few database systems offer support for match recognize, making it unaccessible to a wide range of users. We demonstrate the implementation of a transpiler that translates match recognize into a plain SQL query executable by any database system that supports window functions and recursive common table expressions—no changes to the underlying database systems are required. We evaluate the performance of this approach on the running example to show that the transpiler generates code competitive with contemporary database systems that implement row pattern matching natively. The on-site demonstration is based on DuckDB.

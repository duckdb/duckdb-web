---
layout: post
title: "Building Tetris in a SQL Query!"
author: "Nuno Faria"
tags: ["Talk"]
thirdparty: true
excerpt: ""
pill: "PGConf.EU 2025"
---

[Slides (PDF)](https://nuno-faria.github.io/papers/tetris-sql.pdf)

|-------|-------|
| **Date** | {{ page.date | date: "%Y-%m-%d" }} |
| **Event** | [PGConf.EU 2025](https://2025.pgconf.eu/) |
| **Speaker** | [Nuno Faria (INESC TEC / University of Minho)](https://nuno-faria.github.io/) |

## Abstract

While SQL is a powerful declarative language to query and modify data, it is not designed for general programming tasks. However, since the introduction of recursive Common Table Expressions (CTEs) in SQL:1999, SQL became a Turing complete language. Informally, this means that, in theory, we can implement "any" algorithm in it.

This talk presents a complete implementation of Tetris in a single SQL query, by taking advantage of recursive Common Table Expressions and DuckDB's `USING KEY` feature.

## Code

[GitHub repository](https://github.com/nuno-faria/tetris-sql)

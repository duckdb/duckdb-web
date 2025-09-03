---
layout: post
title: "DuckDB-Wasm: Fast Analytical Processing for the Web"
author: "André Kohn, Dominik Moritz, Mark Raasveldt, Hannes Mühleisen, Thomas Neumann"
thumb: "/images/science/thumbs/vldb-2022.svg"
image: "/images/science/thumbs/vldb-2022.png"
excerpt: ""
tags: ["Paper"]
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol15/p3574-kohn.pdf)

Venue: VLDB 2022

## Abstract

We introduce DuckDB-Wasm, a WebAssembly version of the database system DuckDB, to provide fast analytical processing for the Web. DuckDB-Wasm evaluates SQL queries asynchronously in web workers, supports efficient user-defined functions written in JavaScript, and features a browser-agnostic filesystem that reads local and remote data in pages. DuckDB-Wasm outperforms previous data processing libraries for the Web in the TPC-H benchmark at multiple scale factors. We demonstrate the capabilities of an analytical database in the browser using an interactive SQL shell.

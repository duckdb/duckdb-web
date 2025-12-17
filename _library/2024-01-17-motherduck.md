---
layout: post
title: "MotherDuck: DuckDB in the Cloud and in the Client"
author: "RJ Atwal, Peter Boncz, Ryan Boyd, Antony Courtney, Till Döhmen, Florian Gerlinghoff, Jeff Huang, Joseph Hwang, Raphael Hyde, Elena Felder, Jacob Lacouture, Yves LeMaout, Boaz Leskes, Yao Liu, Alex Monahan, Dan Perkins, Tino Tereshko, Jordan Tigani, Nick Ursa, Stephanie Wang, Yannick Welsch"
thumb: "/images/library/thumbs/cidr-2024.svg"
image: "/images/library/thumbs/cidr-2024.png"
tags: ["Paper"]
thirdparty: true
---

[Paper (PDF)](https://www.cidrdb.org/cidr2024/papers/p46-atwal.pdf)

Venue: CIDR 2024

## Abstract

We describe and demo MotherDuck: a new service that connects DuckDB to the cloud. MotherDuck provides the concept of _hybrid query processing:_ the ability to execute queries partly on the client and partly in the cloud. We cover the motivation for MotherDuck and some of its use cases; and outline its system architecture, which heavily uses the extension mechanisms of DuckDB. MotherDuck allows existing DuckDB users who use a laptop, like data scientists, to start using cloud computing without changing their queries: this can provide better performance as well as scalability to larger datasets. It also provides them the ability to share DuckDB databases with others through the cloud for collaboration. Hybrid query processing opens the door to new data-intensive applications, such as low-latency analytical web apps, with DuckDB-wasm as the client running inside a browser. It also leads on to research questions, some of which we describe in the paper.

## Implementation

[MotherDuck](https://motherduck.com/) is a full-fledged enterprise-ready cloud database.

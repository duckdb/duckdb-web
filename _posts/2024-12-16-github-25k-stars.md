---
layout: post
title: "25 000 Stars on GitHub"
author: The DuckDB team
thumb: "/images/blog/thumbs/github-25k-stars.svg"
image: "/images/blog/thumbs/github-25k-stars.png"
tags: ["release"]
excerpt: "We have recently reached 25 000 stars on GitHub. We would like to use this occasion to stop and reflect about DuckDB's recent year and our future plans."
---

Our [GitHub repository](https://github.com/duckdb/duckdb) has just passed 25,000 stars. This is great news and since it is also the end of the year it is a good moment to reflect on DuckDB’s trajectory. There has been a lot of new and exciting adoption of DuckDB across the industry.

We would like to highlight two main events that have happened this year:

* We [released DuckDB 1.0.0]({% post_url 2024-06-03-announcing-duckdb-100 %}). This version introduced a stable storage format which guarantees [backwards compatibility and limited forward compatibility]({% link docs/stable/internals/storage.md %}#compatibility).
* We started the [DuckDB Community Extensions project]({% post_url 2024-07-05-community-extensions %}). Community extensions allow developers to contribute packages to DuckDB and users to easily install these extensions using the simple command `INSTALL xyz FROM community`.

Besides the GitHub stars we have also observed a lot of growth in various metrics.

* Each month, our website handles over 1.5 million unique visitors. In addition, we see over 300 TB in traffic from ca. 30 million extension downloads. Thanks again to Cloudflare for [sponsoring the project]({% link foundation/index.html %}#technical-sponsors) with free content delivery services!
* In one year, we rose in the [DB Engines ranking](https://db-engines.com/en/ranking) from position 91 to 55 on the general board and from position 47 to 33 in the [relational board](https://db-engines.com/en/ranking/relational+dbms), which makes DuckDB the fastest growing relational system in the top-50.
* We count [7.5M+ monthly downloads in PyPI](https://pypistats.org/packages/duckdb).
* Maven Central downloads for the JDBC driver have also shot up, we now see over 500k+ downloads per month.

We should note that we’re not glorifying those numbers and they are not a target per se for our much-beloved optimization in accordance with [Goodhart’s law](https://en.wikipedia.org/wiki/Goodhart%27s_law). Still, they are just motivating to see grow.

As an aside, we have recently opened a [Bluesky account](https://bsky.app/profile/duckdb.org) and are seeing great discussions happening over there. The account has already exceeded 4 thousand followers!

Following our ancient two-year tradition, we hosted two DuckCon events, one in [Amsterdam]({% link _events/2023-10-06-duckcon4.md %}) and another in [Seattle]({% link _events/2024-08-15-duckcon5.md %}). We also organized the first [DuckDB Amsterdam Meetup]({% link _events/2024-10-17-duckdb-amsterdam-meetup-1.md %}).

Early next year, we are going to host [DuckCon in Amsterdam]({% link _events/2025-01-31-duckcon6.md %}), which is going to be the first event that we live stream in order to be more accessible to the growing DuckDB users in, e.g., Asia.
But for now, let’s sit around the syntax tree and be merry thinking about what’s to come.

<div align="center">
    <img src="/images/blog/duckdb-syntax-tree.jpg"
    alt="Christmas tree with SQL syntax decorations"
    width="800"
    /></div>

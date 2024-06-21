---
layout: post
title: "20 000 Stars on GitHub"
author: "The DuckDB Team"
thumb: "/images/blog/thumbs/240622.svg"
excerpt: ""
---

DuckDB reached 20&nbsp;000 stars today on [GitHub](https://github.com/duckdb/duckdb).
We would like to thank our amazing community of users and [contributors](https://github.com/duckdb/duckdb/graphs/contributors).

To this day, we continue to be amazed by the adoption of DuckDB.
We hit the previous milestone, [10&nbsp;000 stars]({% post_url 2023-05-12-github-10k-stars %}) just a little over a year ago.
Since then, the growth of stars has been slowly increasing, until the [release of version 1.0.0 in early June]({% post_url 2024-06-03-announcing-duckdb-100 %}) gave the boost that propelled the star count to 20&nbsp;000.

<div align="center">
    <img src="/images/blog/github-20k-stars-duckdb.png" alt="Star History of DuckDB" width="700"/>
    <br/>
    (image source: <a href="https://star-history.com/">star-history.com</a>)
</div>

## What Else Happened in June?

The last few weeks since the release were quite eventful:

1. MotherDuck, a DuckDB-based cloud warehouse, just [reached General Availability](https://motherduck.com/blog/announcing-motherduck-general-availability-data-warehousing-with-duckdb/) last week.
    Congratulations to the team on the successful release!

2. We added support to DuckDB for [Delta Lake](https://delta.io/), an open-source lakehouse framework.
    This feature was described in Sam Ansmink's [blog post]({% post_url 2024-06-10-delta %}) and Hannes Mühleisen's [keynote segment at the DATA+AI summit](https://www.youtube.com/watch?v=wuP6iEYH11E).

    With extensions for both [Delta Lake]({% link docs/extensions/delta.md %}) and [Iceberg]({% link docs/extensions/iceberg.md %}),
    DuckDB can now read the two most popular data lake formats.

3. We ran a poster campaign for DuckDB in Amsterdam:

    <div align="center">
        <img src="/images/blog/duckdb-poster-campaign-amsterdam.jpg" alt="Big Data on your Laptop Poster in Amsterdam" width="700"/>
        <br/>
    </div>

4. We sponsored the [Hack4Her event](https://networkinstitute.org/2024/06/18/hack4her-2024-a-celebration-of-women-in-tech-and-innovation/), a female-focused student hackathon in the Netherlands. During the DuckDB Challenge of the event, teams built a community-driven app providing safe walking routes in Amsterdam using DuckDB's data processing capabilities.

    <div align="center">
        <img src="/images/blog/hack4her-duckdb-amsterdam.jpg" alt="Hack4Her Event" width="700"/>
        <br/>
    </div>

## Looking Ahead

There are several interesting events lined up for the summer.

First, two books about DuckDB are expected to be released:

* [**Getting Started with DuckDB**](https://www.packtpub.com/product/getting-started-with-duckdb/9781803241005), authored by Simon Aubury and Ned Letcher, and published by Packt Publishing
* [**DuckDB in Action**](https://www.manning.com/books/duckdb-in-action), authored by Mark Needham, Michael Hunger and Michael Simons, and published by Manning Publications

Second, we are holding our next user community meeting, [DuckCon #5]({% post_url 2024-08-15-duckcon5 %}) in Seattle on August 15 with the regular "State of the Duck" update as well as three regular talks and several lightning talks.

<div align="center"><a href="{% post_url 2024-08-15-duckcon5 %}"><img src="/images/duckcon5-splashscreen.svg"
     alt="DuckCon #5 Splashscreen"
     width="680"
     /></a></div>

Third, we will improve DuckDB's extension ecosystem and streamline the publication process for community extensions.

Finally, we have a series of blog posts lined up for publication.
These will discuss DuckDB's performance over time, the results of the user survey we conducted during the spring, DuckDB's storage format, and many more.
Stay tuned!

We are looking forward to next part of our journey and, of course, the next 10&nbsp;000 stars on GitHub.

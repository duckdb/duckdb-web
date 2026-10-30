---
layout: post
title: "From Forty Minutes to Five: How SproutMe Tests Its Data Pipeline with DuckDB"
authors:
  - Archit Dukhande
  - Geertjan Wielenga
  - Tim Cox
thumb: "/images/blog/thumbs/user-archit-dukhande.svg"
image: "/images/blog/thumbs/user-archit-dukhande.png"
excerpt: "At the early-stage marketing startup [SproutMe](https://www.linkedin.com/in/archit-dukhande/), data engineer Archit Dukhande added DuckDB to the local development and CI workflow behind a data-heavy AI product. BigQuery remains the production warehouse, but running the team's end-to-end pipeline locally on DuckDB cut a daily test run from roughly forty minutes to a few, letting a small team iterate quickly without risking regressions for its pilot users."
tag: using-duckdb
---

> This post describes how SproutMe uses DuckDB in its development and continuous integration workflow. DuckDB is not part of the production product. SproutMe's production data warehouse is Google BigQuery.

## Why Iteration Speed Matters at SproutMe

[SproutMe](https://www.linkedin.com/in/archit-dukhande/) is an advertising-technology startup, about a year old, building an AI workspace for small businesses and marketing agencies. The idea is to bring Google Ads, Meta Ads, and Google Analytics 4 into a single environment that combines analytics, reports, and recommendations, so that even a one-person marketing team can manage campaigns across platforms from one place. A Shopify integration is in progress, and the platform already serves more than 20 pilot accounts.

Archit Dukhande is the data engineer who built SproutMe's data platform from scratch. For a team this size, the speed of the development loop is a business concern, not a convenience. **“Because we are a startup, we have to work very fast,”** he says. In practice that means shipping two to three pull requests a day while making sure nothing breaks for the businesses already relying on the product. **“We don't want the businesses to face problems when we push it,”** Archit explains, so every change is run end to end locally and in CI before it reaches the main branch.

The problem was that these local and CI runs were slow. The pipeline processes a lot of data: when a new customer joins, SproutMe pulls roughly 365 days of history across its ad and analytics sources, which adds up to millions of rows to load and transform. Testing a change against data at that scale on BigQuery was taking long enough to interrupt the team's daily rhythm.

## Where DuckDB Fits

Archit first heard about DuckDB through posts on LinkedIn describing how fast it was. With the development loop slowing the team down, he decided to try it on a few small runs, and from there it worked its way into the everyday workflow. SproutMe now uses DuckDB for two things: local end-to-end testing and CI integration tests.

The pipeline looks like this:

1. [Dagster](https://dagster.io/) orchestrates extraction from Google Ads, Meta Ads, and GA4.
2. The extracted data lands in DuckDB, which acts as the analytical warehouse on the engineer's local machine.
3. [dbt](https://www.getdbt.com/) runs the transformations on DuckDB, following a medallion architecture: bronze for raw data, silver for cleaned and standardized data, and gold for the user-facing models.
4. The same logic runs locally and in CI before any change is deployed.

The transformation stage is where DuckDB earns its place. **“This is where we are saving a lot of time, the transformation part,”** Archit says, with the extraction step benefiting too, since Dagster writes straight into DuckDB. The important point is scope: **“It is part of the local development pipeline.”** Production still runs on BigQuery.

## The Numbers

SproutMe chose BigQuery early because the team was already comfortable with Google's infrastructure, and a full end-to-end run there can take one to two hours. That is fine for production, but far too slow for a team pushing several changes a day and waiting on local and CI feedback each time.

Running the same daily pipeline locally on DuckDB changed the shape of the workday. In SproutMe's own measurements, a daily end-to-end run that took around 30 to 40 minutes on BigQuery dropped to **“around four to five minutes”** on DuckDB, a reduction of more than 80 percent in elapsed time. The comparison is specific to SproutMe's development and testing workflow rather than a general claim that one system is faster than the other, and SproutMe is preparing a detailed benchmark with the workload, data volumes, and configuration so that others can judge it for themselves.

For Archit, the practical effect is faster debugging. Instead of spending hours reproducing an issue, he can identify a bug in a few minutes. **“First one is the development speed. It is super fast,”** he says, naming it the first of DuckDB's advantages. The second is ease of use on local machines, including for the AI coding assistants the team relies on, which can inspect errors and help debug them directly. The third is compatibility: the same setup runs locally and in CI without changes.

## What Comes Next

SproutMe only started using DuckDB a month or two ago, and the results so far have made the team curious about going further. Archit is open to using DuckDB in the production product if additional testing and benchmarking justify it, though he is careful to note that migrating a production workload that already serves pilot accounts is a separate decision that needs its own evaluation. For now, the story is about a faster, safer development loop, not a change to the production warehouse.

## The Takeaway

SproutMe's experience is a reminder that DuckDB can earn a role inside an existing Cloud data architecture without replacing anything in production. By making local development and CI runs fast enough to keep up with a startup's pace, it shortens feedback loops and lowers the risk of shipping a regression, all while BigQuery continues to serve the live product.

We would like to thank Archit for the conversation. If you are using DuckDB and would like to share your story, drop us a line at [quack@duckdb.org](mailto:quack@duckdb.org).

---
layout: post
title: "How SproutMe Cut Integration Test Time by 92.9% with DuckDB"
authors:
  - Archit Dukhande
  - Geertjan Wielenga
  - Tim Cox
thumb: "/images/blog/thumbs/sproutme.svg"
image: "/images/blog/thumbs/sproutme.png"
excerpt: "At [SproutMe](https://sproutme.ai/), a fast-moving, early-stage AI marketing startup, data engineer [Archit Dukhande](https://www.linkedin.com/in/archit-dukhande/) added DuckDB to their local development and CI workflow for a data-heavy AI product. Running the integration tests on DuckDB cut the step per merge by 92.9 percent, from 10.65 minutes to 0.76 minutes, so the team can ship several changes a day without putting users at risk."
tag: using-duckdb
---

## Why Iteration Speed Matters at SproutMe

[SproutMe](https://sproutme.ai/) is an AI workspace that gives marketers and agencies the playbooks large advertisers run in-house: competitive analysis, account audits, cross-channel optimization and more. AI agents do most of the work, leaving marketers free to focus on long-term strategy. SproutMe was founded by [Pulkit Khurana](https://pulkitkhurana.com/), who spent 13 years at Google, most recently as Engineering Director for Google Ads.

[Archit Dukhande](https://www.linkedin.com/in/archit-dukhande/) built SproutMe’s data platform from scratch. For a company moving this fast, development speed directly affects the business. **“Because we are a startup, we have to work very fast,”** he says. In practice, that means shipping two to three pull requests a day without breaking anything for the businesses already using the product. **“We don’t want the businesses to face problems when we push it,”** Archit explains, so every change runs end to end, both locally and in CI, before it reaches the main branch.

Local and CI runs were slow. The pipeline handles a lot of data. When a new customer joins, SproutMe pulls about 365 days of history across its ad and analytics sources, which means millions of rows to load and transform. On BigQuery, testing a change at that scale took long enough to disrupt the team’s daily rhythm.

## Where DuckDB Fits

Archit first heard about DuckDB in LinkedIn posts about its speed. He decided to try it on a few small runs, and it soon became part of the daily workflow. SproutMe now uses DuckDB for local end-to-end testing and CI integration tests.

The pipeline looks like this:

1. [Dagster](https://dagster.io/) orchestrates extraction from Google Ads, Meta Ads, and GA4.
2. The extracted data lands in DuckDB, which acts as the analytical warehouse on the engineer’s local machine.
3. [dbt](https://www.getdbt.com/) runs the transformations on DuckDB, following a medallion architecture: bronze for raw data, silver for cleaned and standardized data, and gold for the user-facing models.
4. The same logic runs locally and in CI before any change is deployed.

The transformation stage is where DuckDB saves the most time. **“This is where we are saving a lot of time, the transformation part,”** Archit says. Extraction benefits as well, because Dagster writes directly into DuckDB. The scope matters, though: **“It is part of the local development pipeline.”** Production still runs on BigQuery.

## The Numbers

SproutMe chose BigQuery early because the team was already familiar with Google’s infrastructure. A full end-to-end run there can take one to two hours. That works for production, but it is too slow for a team pushing several changes a day and waiting on feedback from local and CI runs each time.

Running the same pipeline on DuckDB shortens the wait between changes. In SproutMe’s measurements, the same dbt project, command, and real data ran on both engines. The integration test step, which runs on every merge, fell from a median of 10.65 minutes (639.0 seconds) to **0.76 minutes (45.6 seconds)**. That is a 92.9 percent reduction across 88 CI/CD runs. The dbt runs also got faster. On local test accounts, a full backfill dropped from 180.2 seconds to 104.6 seconds, and a daily incremental build dropped from 300.3 seconds to 120.7 seconds. DuckDB times are medians of five runs. The table below lists all timings in seconds.

<div class="center_aligned_header_table"></div>

| What we measured | BigQuery | DuckDB | Time saved |
|---|---:|---:|---:|
| Integration test step, per merge | 639.0 s | 45.6 s | 92.9% |
| Full dbt backfill | 180.2 s | 104.6 s | 42.0% |
| Daily incremental dbt build | 300.3 s | 120.7 s | 59.8% |
| Backfill and daily build together | 480.5 s | 225.3 s | 53.1% |

These results apply to SproutMe’s development and testing workflow. They do not show that one engine is faster in general.

For Archit, the main gain is faster debugging. Instead of spending hours reproducing an issue, he can find a bug in minutes. **“First one is the development speed. It is super fast,”** he says, calling it the first of DuckDB’s advantages. The second is how easily it runs on local machines, including with the AI coding assistants the team uses, which can inspect errors and help debug them directly. The third is compatibility: the same setup runs locally and in CI without changes.

## What Comes Next

SproutMe has used DuckDB for only a month or two, but the results have made the team curious about going further. Archit is open to using DuckDB in production if more testing and benchmarking support it. He also points out that moving a production workload that serves live customers needs its own evaluation. For now, the change is limited to development, and the production warehouse stays the same.

## The Takeaway

SproutMe shows that DuckDB can fit into an existing Cloud data architecture without replacing anything in production. The integration tests now finish in under a minute, which keeps pace with the team. Feedback arrives sooner, which lowers the risk of shipping a regression, and BigQuery keeps serving the live product.

We would like to thank Archit for the conversation. If you use DuckDB and want to share your story, email [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).

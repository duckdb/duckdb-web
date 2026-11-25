---
layout: post
title: "DuckDB User Group Workshop on AI-Powered Review Analysis with Hugging Face"
authors:
  - Geertjan Wielenga
thumb: /images/blog/thumbs/duckdb-hugging-face-workshop.svg
image: /images/blog/thumbs/duckdb-hugging-face-workshop.png
excerpt: "On 11 November 2026, the DuckDB User Group held its first workshop in Amsterdam, together with Hugging Face. Pratik Patel from Hugging Face led the session."
tag: using-duckdb
---

![Workshop room with attendees at laptops]({% link images/blog/duckdb-user-group-workshop-amsterdam.png %})

In one afternoon, attendees built a pipeline that finds the products with falling ratings in 2.1 million Amazon reviews and explains why. DuckDB did the filtering and an LLM summarized the complaints. At the end, each attendee had a Hugging Face Space that they can call as an API.

## What We Built

The data was the appliances part of the Amazon Reviews 2023 dataset. That is 2.1 million reviews and about 1.2 GB of raw JSON lines. Nobody downloaded it over the venue Wi-Fi. Attendees built and tested everything on their laptops with a 22 MB sample. Then the same two files ran on Hugging Face against the full data.

The afternoon had five modules.

1. **Build locally.** An ingest script converted the sample from JSON lines into two Parquet tables, one for reviews and one for products. It runs in seconds, so attendees could change a column and run it again.

2. **Find the trouble.** A file of DuckDB queries, run with `duckdb < sql/analysis.sql`, showed the rating distribution, followed one product month by month, ranked products by how much their rating fell in the last six months, and selected the most helpful recent 1 and 2 star reviews for one product.

3. **Run it on the full data.** The same ingest script ran as a Hugging Face Job on all 2.1 million reviews. The job read the data inside the Hugging Face network and wrote the Parquet files to a Storage Bucket. The hardware costs $0.01 an hour, and the job ran during the coffee break.

4. **Build the workflow.** Gradio's `gr.Workflow` showed five Python functions as nodes on a canvas. Attendees connected them and ran them one by one.

5. **Ship it.** `gradio deploy` put the app on a Hugging Face Space with the bucket mounted at `/data`. Each node in the workflow is also an API endpoint that you can call with `gradio_client`.

The rating distribution explains why the ranking query is needed. Most reviews give 5 stars and there is a smaller peak at 1 star, so a plain average does not show change well. The ranking query compares each product's recent average with its earlier average. A simplified version looks like this.

```sql
WITH split AS (
    SELECT
        parent_asin,
        rating,
        reviewed_at >= (SELECT max(reviewed_at) FROM 'clean/reviews.parquet')
                       - INTERVAL 6 MONTH AS is_recent
    FROM 'clean/reviews.parquet'
    WHERE verified_purchase
)
SELECT
    parent_asin,
    avg(rating) FILTER (WHERE NOT is_recent) AS before_avg,
    avg(rating) FILTER (WHERE is_recent)     AS recent_avg,
    recent_avg - before_avg                  AS change
FROM split
GROUP BY parent_asin
HAVING count(*) FILTER (WHERE is_recent)     >= 20
   AND count(*) FILTER (WHERE NOT is_recent) >= 50
ORDER BY change
LIMIT 10;
```

A product needs at least 20 recent and 50 earlier verified reviews to be ranked. Attendees changed these two thresholds to see how the list changed.

## SQL First, Then the LLM

DuckDB selects the product with the largest drop in rating and the 40 most helpful recent complaints about it. Only those 40 reviews go to the LLM, which groups them into themes with counts and quotes and lists safety issues first. The Space runs the result, reads its data from a Storage Bucket and makes every step available as an API.

The model does not have to decide which reviews are relevant, because the SQL already did that. This keeps the number of LLM calls small. The pipeline uses six columns: `parent_asin`, `rating`, `text`, `reviewed_at`, `helpful_vote` and `verified_purchase`. If you load other customer feedback into these columns, the SQL and the workflow run without changes.

## Who Attended

The workshop brought together software engineers, data engineers, platform engineers, researchers, and product managers from various organizations across Europe. The workshop did not require ML experience — attendees needed to know SQL and be able to read basic Python.

The workshop received an average rating of 4.65 out of 5. Attendees highlighted what worked well: the exercises with real data, the DuckDB and Hugging Face content, the preparation of the speaker and host, the organization and the food.

## Thanks and Where Next?

Thank you to [Pratik Patel](https://www.linkedin.com/in/prpatel/) and Hugging Face for preparing and leading the workshop, and to everyone who attended.

**This was the first workshop run by the DuckDB User Group, and we want to run more of them. Join the [DuckDB User Group on Meetup](https://www.meetup.com/duckdb/) to stay updated on future workshops and meetups. If your company or community wants to co-organize a DuckDB User Group workshop or meetup, send us a request at [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com). Tell us where you are, what topic you have in mind and what you can offer or need to make it happen, such as a venue, a speaker or catering.**

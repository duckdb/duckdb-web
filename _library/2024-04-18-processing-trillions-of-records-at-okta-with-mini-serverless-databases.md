---
layout: post
title: "Processing Trillions of Records at Okta with Mini Serverless Databases"
author: Jake Thomas
tags: ["Talk"]
thirdparty: true
excerpt: ""
pill: "Data Council 2024"
---

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/TrmJilG4GXk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

|-------|-------|
| **Event** | [Data Council 2024](https://www.datacouncil.ai/bay-2024) |
| **Speaker** | Jake Thomas (Manager, Data Foundations, Okta) |
| **YouTube** | [Processing Trillions of Records at Okta with Mini Serverless Databases](https://www.youtube.com/watch?v=TrmJilG4GXk) |

## Abstract

While building Okta's next-gen security data platform, the pipelines required the total cost of ownership of batch ETL, the latency of streaming, the flexibility of SQL, the durability of S3, the ease and enormous scalability of serverless, and a minimal footprint for constrained environments. To satisfy these requirements, Okta turned to serverless DuckDB for all data preprocessing, normalization, and operational metadata harvesting. Over six months, Okta's defensive cyber operations team processed 7.5 trillion records across 130 million files using thousands of concurrent DuckDB instances, handling data spikes from 1.5 TB to 50 TB per day without infrastructure changes.

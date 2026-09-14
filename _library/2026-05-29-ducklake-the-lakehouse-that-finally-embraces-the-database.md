---
layout: post
title: "DuckLake: The Lakehouse That Finally Embraces the Database"
author: "Graziano Montanaro"
tags: ["Talk"]
category: community
excerpt: ""
pill: "PyCon Italia 2026"
---

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/SJ9VqyQMTw8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

|-------|-------|
| **Event** | [PyCon Italia 2026](https://2026.pycon.it/) |
| **Speaker** | Graziano Montanaro |
| **YouTube** | [DuckLake: The Lakehouse That Finally Embraces the Database](https://www.youtube.com/watch?v=SJ9VqyQMTw8) |

## Abstract

DuckLake challenges the dominance of Iceberg and Delta Lake by managing table metadata in a simple database instead of a complex file system, coupling the low-cost storage of object storage like S3 with the transactional guarantees of a standard SQL database. The talk covers DuckLake's design as well as its trade-offs, including the single-writer bottleneck for high-concurrency write scenarios, scale limits where distributed catalogs become necessary, and ecosystem maturity compared to established formats like Delta Lake and Iceberg.

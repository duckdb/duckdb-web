---
layout: post
title: "Running TPC-H SF300 on a Raspberry Pi"
author: Gábor Szárnyas
thumb: "/images/blog/thumbs/raspberry-pi.svg"
image: "/images/blog/thumbs/raspberry-pi.png"
excerpt: DuckDB can run all TPC-H SF300 queries on a Raspberry Pi board.
tags: ["benchmark"]
--- 

## Introduction

The Raspberry Pi is a great initiative to provide around affordable but easy-to-program microcomputer boards.
The initial models in 2012 had a CPU with a single core running at 0.7 GHz, 256 MB RAM and an SD card slot, making it a good educational platform.
Over time the Raspberry Pi Foundation introduced more and more powerful models that found many interesting use cases among hobbyists, who formed a thriving online community.

The latest model, the Raspberry Pi 5 model has a 2.4 GHz quad-core CPU and – with extra connectors – can make use of an NVMe SSD for storage.
Last week, the [Raspberry Pi 5 got another upgrade](https://www.raspberrypi.com/news/16gb-raspberry-pi-5-on-sale-now-at-120/):
it can now be kitted out with 16 GB of RAM.
To put this into context, this is equivalent to the amount of memory found in the median gaming machine as reported by the [2024 December Steam survey](https://store.steampowered.com/hwsurvey/Steam-Hardware-Software-Survey-Welcome-to-Steam).

## Setup

The DuckDB teams likes to experiment with DuckDB in [unusual]({% post_url 2021-10-29-duckdb-wasm %}) [setups]({% post_url 2024-12-06-duckdb-tpch-sf100-on-mobile %}), so we were eager to get our hands on a new Raspberry Pi 5.
So we ordered the following components for our setup:

| Component | Price (USD) |
|-----------|------------:|
| [Raspberry Pi 5 with 16 GB RAM](https://www.raspberrypi.com/products/raspberry-pi-5/) | 120.00 |
| [Raspberry Pi 27 W USB-C power supply](https://www.raspberrypi.com/products/27w-power-supply/) | 13.60 |
| [Raspberry Pi microSD card (128 GB)](https://www.raspberrypi.com/products/sd-cards/) | 33.40 |
| [Samsung 980 NVMe SSD (1 TB)](https://www.amazon.com/Technology-Intelligent-Turbowrite-MZ-V8V1T0B-AM/dp/B08V83JZH4) | 84.00 |
| [Argon ONE V3 Case](https://argon40.com/products/argon-one-v3-case-for-raspberry-pi-5) | 30.00 |
| **Total** | **$281.00** |

> Disclaimer: We purchased all the hardware for our experiments. This is not a sponsored post.

We installed the heat sinks, assembled the house, popped in the SSD, and connected the cables to the house. Here is a photo of our machine:

<div align="center">
    <img src="/images/blog/raspberry-pi-5-duckdb.jpg"
    alt="Raspberry 5 in an Argon ONE v3 case"
    width="600px"
    /></div>

## Experiments

So what can this little box do? We used the well-known [TPC-H workload](https://www.tpc.org/tpch/) to find out.

We compiled DuckDB version [`0024e5d4be`](https://github.com/duckdb/duckdb/commit/0024e5d4be) using the [Raspberry Pi build intructions in the documentation]({% link docs/dev/building/raspberry_pi.md %}).
To make the experiments easier to run, we also included the [TPC-H extension]({% link docs/extensions/tpch.md %}) in the build:

```batch
GEN=ninja CORE_EXTENSIONS="tpch" make
```

We then downloaded the TPC-H scale factor 100 and scale factor 300 databases from DuckDB's public data repository:

```batch
wget https://blobs.duckdb.org/data/tpch-sf100.db
wget https://blobs.duckdb.org/data/tpch-sf300.db
```

We used two different storage options.
We first stored the databases on the 128 GB microSD card, as the microSD card is the only storage that most Raspberry Pi setups have.
This card works fine for serving the operating system and programs.
It can also store DuckDB databases but it's rather slow for processing large amounts of data.
Therefore, for our second attempt, we used a 1 TB NVMe SSD, connected to the board via the Argon ONE case, and formatted to use the `ext4` file system.

We set the `SF` and `STORAGE` environment variables and ran DuckDB with the `tpch-power-test.sql` script:

<details markdown='1'>
<summary markdown='span'>
`tpch-power-test.sql`
</summary>
<pre>
PRAGMA version;
SET enable_progress_bar = false;
LOAD tpch;
.timer on
PRAGMA tpch(1);
PRAGMA tpch(2);
PRAGMA tpch(3);
PRAGMA tpch(4);
PRAGMA tpch(5);
PRAGMA tpch(6);
PRAGMA tpch(7);
PRAGMA tpch(8);
PRAGMA tpch(9);
PRAGMA tpch(10);
PRAGMA tpch(11);
PRAGMA tpch(12);
PRAGMA tpch(13);
PRAGMA tpch(14);
PRAGMA tpch(15);
PRAGMA tpch(16);
PRAGMA tpch(17);
PRAGMA tpch(18);
PRAGMA tpch(19);
PRAGMA tpch(20);
PRAGMA tpch(21);
PRAGMA tpch(22);
</pre>
</details>

```batch
duckdb tpch-sf${SF}.db -c '.read power.sql'
    | tee tpch-${SF}-${STORAGE}.log
```

| Scale factor | Storage | Geometric mean runtime | Total runtime |
|-------------:|---------|-----------------------:|--------------:|
| 100          | microSD |                 23.8 s |       769.9 s |
| 100          | NVMe    |                 11.7 s |       372.3 s |
| 300          | microSD |                171.9 s |     4,866.5 s |
| 300          | NVMe    |                 55.2 s |     1,561.8 s |

If you look at [historical TPC-H results from 20 years ago](https://www.tpc.org/tpch/results/tpch_results5.asp?version=2), you can find systems had a geometric mean query runtime of more than 60 seconds for their power test.
And, with the license and maintenance costs factored in, they cost more than 1,000× as much as our setup with Raspberry Pi 5.
The innovation in hardware and software over the last 20 years resulted in this remarkable price-performance ratio increase.

If you are interested in the detailed query runtimes, you can find the table behind the following line:

<details markdown='1'>
<summary markdown='span'>
<i>Detailed query runtimes (in seconds)</i>
</summary>
<table>
    <tr><th>Query</th><th>SF100 / microSD</th><th>SF100 / NVMe</th><th>SF300 / microSD</th><th>SF300 / NVMe</th></tr>
    <tr><td>Q1</td><td align="right">81.1</td><td align="right">15.6</td><td align="right">242.0</td><td align="right">12.34</td></tr>
    <tr><td>Q2</td><td align="right">7.9</td><td align="right">2.4</td><td align="right">27.8</td><td align="right">12.34</td></tr>
    <tr><td>Q3</td><td align="right">31.5</td><td align="right">11.8</td><td align="right">218.9</td><td align="right">12.34</td></tr>
    <tr><td>Q4</td><td align="right">40.2</td><td align="right">11.4</td><td align="right">157.5</td><td align="right">12.34</td></tr>
    <tr><td>Q5</td><td align="right">32.2</td><td align="right">12.3</td><td align="right">215.9</td><td align="right">12.34</td></tr>
    <tr><td>Q6</td><td align="right">1.6</td><td align="right">1.4</td><td align="right">155.9</td><td align="right">12.34</td></tr>
    <tr><td>Q7</td><td align="right">12.1</td><td align="right">12.3</td><td align="right">255.2</td><td align="right">12.34</td></tr>
    <tr><td>Q8</td><td align="right">25.0</td><td align="right">19.2</td><td align="right">298.0</td><td align="right">12.34</td></tr>
    <tr><td>Q9</td><td align="right">74.0</td><td align="right">50.1</td><td align="right">337.2</td><td align="right">12.34</td></tr>
    <tr><td>Q10</td><td align="right">54.7</td><td align="right">24.3</td><td align="right">234.9</td><td align="right">12.34</td></tr>
    <tr><td>Q11</td><td align="right">7.8</td><td align="right">2.3</td><td align="right">34.0</td><td align="right">12.34</td></tr>
    <tr><td>Q12</td><td align="right">43.1</td><td align="right">13.6</td><td align="right">202.9</td><td align="right">12.34</td></tr>
    <tr><td>Q13</td><td align="right">59.2</td><td align="right">51.7</td><td align="right">207.4</td><td align="right">12.34</td></tr>
    <tr><td>Q14</td><td align="right">33.0</td><td align="right">9.7</td><td align="right">269.7</td><td align="right">12.34</td></tr>
    <tr><td>Q15</td><td align="right">11.1</td><td align="right">7.1</td><td align="right">157.2</td><td align="right">12.34</td></tr>
    <tr><td>Q16</td><td align="right">8.7</td><td align="right">8.7</td><td align="right">33.4</td><td align="right">12.34</td></tr>
    <tr><td>Q17</td><td align="right">8.3</td><td align="right">7.6</td><td align="right">249.4</td><td align="right">12.34</td></tr>
    <tr><td>Q18</td><td align="right">73.9</td><td align="right">40.9</td><td align="right">374.7</td><td align="right">12.34</td></tr>
    <tr><td>Q19</td><td align="right">66.0</td><td align="right">17.8</td><td align="right">317.9</td><td align="right">12.34</td></tr>
    <tr><td>Q20</td><td align="right">22.4</td><td align="right">8.4</td><td align="right">273.1</td><td align="right">12.34</td></tr>
    <tr><td>Q21</td><td align="right">66.9</td><td align="right">35.2</td><td align="right">569.5</td><td align="right">12.34</td></tr>
    <tr><td>Q22</td><td align="right">9.2</td><td align="right">8.4</td><td align="right">34.1</td><td align="right">12.34</td></tr>
</table>
</details>

> Disclaimer: The results presented here are not official TPC-H results and only include the TPC-H power test.

That's it for today. If you have deployed DuckDB in an interesting setup, please let us now!

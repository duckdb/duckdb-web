---
layout: post
title: "Big Data on the Move: DuckDB on the Framework Laptop 13"
author: Gábor Szárnyas
thumb: "/images/blog/thumbs/framework-laptop-13.png"
image: "/images/blog/thumbs/framework-laptop-13.svg"
excerpt: "We put DuckDB through its paces on a 12-core ultrabook with 128 GB RAM, running TPC-H queries up to SF10,000."
tags: ["benchmark"]
---

## Background

When DuckDB's design was first sketched out in 2018, a key insight was that laptops had gotten powerful enough to handle most analytical workloads that data scientists can throw at them.
This made implementing a new analytical database as a single-node system that can run everywhere – including laptops – a feasible proposition: enter DuckDB.

In 2020, the release of Apple Silicon gave DuckDB-on-a-laptop setups a big performance boost. Today, modern MacBooks have CPUs with a dozen plus cores along with lots of memory and fast disks – all of which DuckDB is very eager to make use of. However, this comes at a steep price: here in the Netherlands, speccing up a MacBook Pro with 128 GB of RAM and 8 TB of disk will set you back more than 8,500 euros.

Meanwhile, there have been significant leaps in x86 land too. AMD's [Ryzen AI 300](https://en.wikipedia.org/wiki/List_of_AMD_Ryzen_processors#Strix_Point_mobile) ultrathin mobile processors, released in 2024, pack up to 12 cores and 24 threads. DuckDB is [just as happy]({% link why_duckdb.md %}#portable) to run on the x86_64 architecture as it is on arm64 processors, so we were eager to find out how DuckDB performs on the new AMDs.

## Setup

To run this experiment, we purchased the 13" modular laptop by [Framework](https://frame.work/gb/en) and kitted it out with 128 GB of RAM and 8 TB of disk – all for [just under 3,000 euros](#cost-breakdown).

We installed [Omarchy 2.0](https://omarchy.org/), an Arch Linux-based distribution with a vibrant community and first-class support for Framework laptops. Assembling the laptop and installing Omarchy took less than an hour in total. Installing the DuckDB command line client only took seconds using the installer script:

```batch
curl https://install.duckdb.org | sh
```

We changed the theme to _[Osaka Jade](https://github.com/Justikun/omarchy-osaka-jade-theme)_ for a more Matrix-like look and got to work:

<img src="/images/blog/framework-13-duckdb.jpg"
     alt="DuckDB running on the Framework Laptop 13&quot;"
     width="800"
     />

## Experiments

To see how this laptop performs, we ran a few benchmarks focusing on loading and query processing times.

### CSV Loading

To measure CSV loading performance, we used one of our favorite datasets: the [Dutch railway services]({% link docs/stable/guides/snippets/dutch_railway_datasets.md %}). We picked the [full dataset spanning the last 80 months](https://blobs.duckdb.org/nl-railway/railway-services-80-months.zip) (between Jan 2019 and Aug 2025).
We can fetch and decompress the file as follows:

```batch
wget https://blobs.duckdb.org/nl-railway/railway-services-80-months.zip
unzip railway-services-80-months.zip
```

The resulting directory is approximately 20 GB. Let's see how quickly DuckDB can load the files:

```batch
duckdb
```

```sql
.timer on
CREATE TABLE services AS FROM 'services/services-*.csv.gz';
-- Run Time (s): real 10.219 user 217.596664 sys 7.348692
```

It turns out that DuckDB can load 20 GB of CSV files into memory in just 10.2 seconds, at 1.96 GB/s!

### TPC-H Benchmarks

To see query performance, we used TPC-H.
We have already run TPC-H queries in all
[sorts]({% post_url 2021-10-29-duckdb-wasm %})
[of]({% post_url 2024-12-06-duckdb-tpch-sf100-on-mobile %})
[environments]({% post_url 2025-01-17-raspberryi-pi-tpch %})
and were curious: how far can DuckDB scale on this laptop?

#### Data Generation

Of course, we first needed some big TPC-H datasets, and we needed to generate them locally – downloading them could take days.
Luckily, we could use the [tpchgen-rs](https://github.com/clflushopt/tpchgen-rs/) tool, a pure Rust implementation of the TPC-H generator that can produce large-scale datasets on the laptop in just a few hours. We generated the data as Parquet files and loaded them into DuckDB.

> Omarchy comes with the [btrfs](https://en.wikipedia.org/wiki/Btrfs) file system by default. We created a directory for the generated data and disabled copy-on-write (see the [configuration details](#file-system-configuration)).

#### SF3,000

We first ran all 22 TPC-H queries on the SF3,000 the dataset, which corresponds to 3,000 GB of CSV files.
The total runtime of the queries was 47.5 minutes with a geometric mean query runtime of 86.5 seconds.

During the experiments, we noticed that the laptop bottom cover heated up [above 45 degrees Celsius](https://www.notebookcheck.net/Framework-Laptop-13-5-Ryzen-AI-9-review-Skip-the-Intel-version-for-better-performance.997363.0.html): while the keyboard was still usable, you definitely won't want to keep this machine on your lap while running data crunching workloads.
Obviously, the excess heat also results in some thermal throttling that causes the CPU to be downclocked, making the queries slower.
We are no stranger to such issues: last year, we [dipped an iPhone 16 in dry ice to improve its cooling]({% post_url 2024-12-06-duckdb-tpch-sf100-on-mobile %}#a-song-of-dry-ice-and-fire), but this seemed impractical with the laptop, so we resorted to more practical measures.

For our “cool run”, we simply inserted 5-minute sleeping periods between queries to allow the laptop to cool down. This worked very well: the total runtime of the queries (with the cooling periods excluded) went down to 30.8 minutes and the geometric mean runtime reduced to 58.2 seconds – a 32% speedup!

> Most interactive data science workloads have the query execution interspersed with the time spent on coding and analysis – which allows such a cooling period for the laptop.

#### SF3,000 on Battery

So far, we ran our experiments with the laptop plugged into the charger. But laptops are portable devices after all, so we were curious – can we run the queries on the SF3,000 dataset while on the move?

It turns out that we can! Running all TPC-H queries on the SF3,000 dataset took 46.9 minutes (with a geomean runtime of 83.7 seconds) and it drained a fully charged battery to about 30%.
That said, if you analyze terabyte-sized datasets on your laptop, you may still want to carry a [power bank](https://www.anker.com/products/a1340-250w-power-bank) just to be on the safe side.

#### TPC-H SF10,000

Finally, it was time for our ultimate challenge – can this laptop handle the SF10,000 dataset?
To decide, we:

* generated the data – _about 4 TB in Parquet files,_
* loaded it into DuckDB – _about 2.7 TB in DuckDB's format,_
* cleaned up the Parquet files – _knowing that the extra space will come in handy,_
* ran the queries – _and witnessed DuckDB spilling 3.6 TB on the disk for some queries,_

but ultimately saw it finishing without an issue!

**The run took a total of 4.2 hours with a geometric mean query runtime of 6.6 minutes.**

Unsurprisingly, some thermal throttling also occurred here, so we repeated the experiment with cooling periods. We found that this brings down the total query runtime to 3.8 hours with a geomean runtime of 5.7 minutes (14% speedup). This means that the differences are smaller than for the SF3,000 dataset, which actually makes perfect sense: given the longer query runtimes, the cooling periods no longer have that much of an effect.

## Conclusion

In short, we found that you can build a laptop for less than 3,000 euros that can load CSV files at almost 2 GB / second, run the full range of TPC-H queries on SF3,000 while on battery, and complete all queries on the SF10,000 dataset.

While ours is not an official TPC-H run, it's worth mentioning that among the current ranking of [audited SF10,000 TPC-H implementations](https://www.tpc.org/tpch/results/tpch_perf_results5.asp?resulttype=all&version=3), the cost of the cheapest setup capable of doing TPC-H SF10,000 is well over 1 million euros or 1.2 million U.S. dollars – our setup costs less than 0.3% of that and will do the job for 99% of data science workloads.

Just don't forget to pause every now and then to allow the laptop to cool down a bit.

## Appendix

### Cost Breakdown

Here's the cost breakdown of the laptop using retail prices in euros (including the 21% Dutch VAT). The items were purchased in August 2025.

| Item                                                         |   Cost (EUR) |
| ------------------------------------------------------------ | -----------: |
| [Framework Laptop 13 DIY Edition w/ AMD Ryzen AI 9 HX 370 CPU](https://frame.work/laptop13) |     1,785.00 |
| Framework Laptop 13 Bezel – Translucent Green                |        55.00 |
| Keyboard – US English                                        |       109.00 |
| Power Adapter – 60W – EU                                     |        49.00 |
| HDMI (3rd Gen) Expansion Card                                |        20.00 |
| USB-A Expansion Card                                         |        10.00 |
| USB-C Expansion Card – Translucent Green (2 pcs)             |        20.00 |
| [WD_BLACK SN850X NVMe SSD 8TB](https://www.amazon.nl/dp/B0D9WT512W?th=1)                                 |       582.69 |
| [Crucial DDR5 RAM 128GB Kit](https://www.amazon.nl/dp/B0DSQMKYLN)                                   |       327.87 |
| **Total (euros, VAT included)**                              | **2,974.87** |

Note that Framework currently only sells 96 GB memory kits but both the motherboard and the CPU can handle 128 GB (2 × 64 GB) kits.

### File System Configuration

In our initial experiments, we experienced intermittent checksum errors from the btrfs file system in [dmesg](https://man.archlinux.org/man/dmesg.1.en), manifesting as `BTRFS warning (device dm-0): csum failed ...` messages and crashes. We ran extensive disk and memory tests, which indicated no issues, and also attempted to reproduce the error on an AWS EC2 cloud instance with btrfs but we could not observe the issue there. If you have an insight into this error or have a reproducer, please [let us know](https://github.com/duckdb/duckdb/issues/new) and we'd be happy to send you some [DuckDB merch](https://shop.duckdb.org/)!

Because DuckDB's storage already uses checksums, we can [disable copy-on-write along with checksums](https://wiki.archlinux.org/title/Btrfs#Disabling_CoW) for the experiments using the NOCOW attribute without risking data corruption:

```batch
sudo chattr +C duckdb-tpch-experiment
lsattr -d duckdb-tpch-experiment
```

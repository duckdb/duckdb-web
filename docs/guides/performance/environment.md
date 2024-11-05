---
layout: docu
title: Environment
---

The environment where DuckDB is run has an obvious impact on performance. This page focuses on the effects of the hardware configuration and the operating system used.

## Hardware Configuration

### CPU and Memory

As a rule of thumb, DuckDB requires a **minimum** of 125 MB of memory per thread.
For example, if you use 8 threads, you need at least 1 GB of memory.
For ideal performance, aggregation-heavy workloads require approx. 5 GB memory per thread and join-heavy workloads require approximately 10 GB memory per thread.

> Bestpractice Aim for 5-10 GB memory per thread.

> Tip If you have a limited amount of memory, try to [limit the number of threads]({% link docs/configuration/pragmas.md %}#threads), e.g., by issuing `SET threads = 4;`.

### Disk

DuckDB is capable of operating both as an in-memory and as a disk-based database system. In both cases, it can spill to disk to process larger-than-memory workloads (a.k.a. out-of-core processing) for which a fast disk is highly beneficial. However, if the workload fits in memory, the disk speed only has a limited effect on performance.

### Local Disk

DuckDB's disk-based mode is designed to work best with SSD and NVMe disks. While HDDs are supported, they will result in low performance, especially for write operations.

### Network-Attached Disks

**Cloud disks.** DuckDB runs well on network-backed cloud disks such as [AWS EBS](https://aws.amazon.com/ebs/) for both read-only and read-write workloads.

**Network-attached storage.**
Network-attached storage can serve DuckdB for read-only workloads.
However, _it is not recommended to run DuckDB in read-write mode on network-attached storage (NAS)._
These setups include [NFS](https://en.wikipedia.org/wiki/Network_File_System),
network drives such as [SMB](https://en.wikipedia.org/wiki/Server_Message_Block) and
[Samba](https://en.wikipedia.org/wiki/Samba_(software)).
Based on user reports, running read-write workloads on network-attached storage can result in slow and unpredictable performance,
as well as spurious errors cased by the underlying file system.

> Warning Avoid running DuckDB in read-write mode on network-attached storage.

> Bestpractice Fast disks are important if your workload is larger than memory and/or fast data loading is important. Only use network-backed disks if they are reliable (e.g., cloud disks) and guarantee high IO.

## Operating System

We recommend using the latest stable version of operating systems: macOS, Windows, and Linux are all well-tested and DuckDB can run on them with high performance. Among Linux distributions, we recommended using Ubuntu Linux LTS due to its stability and the fact that most of DuckDB’s Linux test suite jobs run on Ubuntu workers.

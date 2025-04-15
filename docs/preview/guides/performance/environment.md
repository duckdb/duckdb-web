---
layout: docu
title: Environment
---

The environment where DuckDB is run has an obvious impact on performance. This page focuses on the effects of the hardware configuration and the operating system used.

## Hardware Configuration

### CPU

DuckDB works efficiently on both AMD64 (x86_64) and ARM64 (AArch64) CPU architectures.

### Memory

> Bestpractice Aim for 1-4 GB memory per thread.

#### Minimum Required Memory

As a rule of thumb, DuckDB requires a _minimum_ of 125 MB of memory per thread.
For example, if you use 8 threads, you need at least 1 GB of memory.
If you are working in a memory-constrained environment, consider [limiting the number of threads]({% link docs/preview/configuration/pragmas.md %}#threads), e.g., by issuing:

```sql
SET threads = 4;
```

#### Memory for Ideal Performance

The amount of memory required for ideal performance depends on several factors, including the data set size and the queries to execute.
Maybe surprisingly, the _queries_ have a larger effect on the memory requirement.
Workloads containing large joins over many-to-many tables yield large intermediate datasets and thus require more memory for their evaluation to fully fit into the memory.
As an approximation, aggregation-heavy workloads require 1-2 GB memory per thread and join-heavy workloads require 3-4 GB memory per thread.

#### Larger-than-Memory Workloads

DuckDB can process larger-than-memory workloads by spilling to disk.
This is possible thanks to _out-of-core_ support for grouping, joining, sorting and windowing operators.
Note that larger-than-memory workloads can be processed both in persistent mode and in in-memory mode as DuckDB still spills to disk in both modes.

### Local Disk

**Disk type.**
DuckDB's disk-based mode is designed to work best with SSD and NVMe disks. While HDDs are supported, they will result in low performance, especially for write operations.

**Disk-based vs. in-memory storage.**
Counter-intuitively, using a disk-based DuckDB instance can be faster than an in-memory instance due to compression.
Read more in the [“How to Tune Workloads” page]({% link docs/preview/guides/performance/how_to_tune_workloads.md %}#persistent-vs-in-memory-tables).

**File systems.**
On Linux, we recommend using the ext4 or xfs file systems.
On Windows, we recommend using NTFS and avoiding FAT32.

> Note that DuckDB databases have built-in checksums, so integrity checks from the file system are not required to prevent data corruption.

### Network-Attached Disks

**Cloud disks.** DuckDB runs well on network-backed cloud disks such as [AWS EBS](https://aws.amazon.com/ebs/) for both read-only and read-write workloads.

**Network-attached storage.**
Network-attached storage can serve DuckDB for read-only workloads.
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

## Memory Allocator

If you have a many-core CPU running on a system where DuckDB ships with [`jemalloc`]({% link docs/preview/extensions/jemalloc.md %}) as the default memory allocator, consider [enabling the allocator's background threads]({% link docs/preview/extensions/jemalloc.md %}#background-threads).
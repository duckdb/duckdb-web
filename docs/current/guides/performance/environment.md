---
layout: docu
redirect_from:
- /docs/guides/performance/environment
- /docs/preview/guides/performance/environment
- /docs/stable/guides/performance/environment
title: Environment
---

The environment where DuckDB is run has an obvious impact on performance. This page focuses on the effects of the hardware configuration and the operating system used.

## Hardware Configuration

### CPU

DuckDB's officially supported architectures are AMD64 (x86_64) and ARM64 (AArch64) CPU architectures. DuckDB works efficiently on both of these architectures.

> DuckDB can be compiled to other architecture such as [LoongArch]({% link _everywhere/morefine-m700s.md %}) and [RISC-V]({% link docs/current/dev/building/unofficial_and_unsupported_platforms.md %}#risc-v-architectures). However, there are no performance guarantees for these platforms.

### Memory

> Bestpractice Aim for 1-4 GB memory per thread.

#### Minimum Required Memory

As a rule of thumb, DuckDB requires a _minimum_ of 125 MB of memory per thread.
For example, if you use 8 threads, you need at least 1 GB of memory.
If you are working in a memory-constrained environment, consider [limiting the number of threads]({% link docs/current/configuration/pragmas.md %}#threads), e.g., by issuing:

```sql
SET threads = 4;
```

#### Memory for Ideal Performance

The amount of memory required for ideal performance depends on several factors, including the dataset size and the queries to execute.
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
Read more in the [“How to Tune Workloads” page]({% link docs/current/guides/performance/how_to_tune_workloads.md %}#persistent-vs-in-memory-tables).

**File systems.**
On Linux, [DuckDB performs best with the XFS file system](https://www.phoronix.com/review/linux-70-filesystems/4) but it also performs reasonably well with other file systems such as ext4.
On Windows, we recommend using NTFS and avoiding FAT32.

> Note that DuckDB databases have built-in checksums, so integrity checks from the file system are not required to prevent data corruption.

### Network-Attached Disks

Special care needs to be taken when using network-attached disks:

* If you are writing to disk, it is important that the disks is reliable. As a general rule of thumb, this is true for locally attached disks, and block storage in the cloud.
* If your workload is larger than memory and/or fast data loading is important, you need fast disks, preferrably SSD or NVMe with a fast connection.

With these in mind, here are two common architectures and the related considerations when you are using DuckDB's [native database format]({% link docs/lts/internals/storage.md %}):

**Clock storage in the colud.** DuckDB runs well on network-backed cloud disks such as [AWS EBS](https://aws.amazon.com/ebs/) for both read-only and read-write workloads.

**Network-attached storage.**
Network-attached storage can serve DuckDB for read-only workloads.
However, _it is recommended to avoid using DuckDB's native database format in read-write mode on network-attached storage (NAS)._
These setups include [NFS](https://en.wikipedia.org/wiki/Network_File_System),
network drives such as [SMB](https://en.wikipedia.org/wiki/Server_Message_Block) and
[Samba](https://en.wikipedia.org/wiki/Samba_(software)).
Based on user reports, running read-write workloads on network-attached storage can result in slow and unpredictable performance,
as well as spurious errors caused by the underlying file system.
Instead of using DuckDB's native database format, consider using the [DuckLake lakehouse format](https://ducklake.select/).

## Operating System

We recommend using the latest stable version of operating systems: macOS, Windows, and Linux are all well-tested and DuckDB can run on them with high performance.

### Linux

DuckDB runs on all mainstream Linux distributions released in the last ≈5 years.
If you don't have a particular preference, we recommend using Ubuntu Linux LTS due to its stability and the fact that most of DuckDB’s Linux test suite jobs run on Ubuntu workers.

#### glibc vs. musl libc

DuckDB can be built with both [glibc](https://www.gnu.org/software/libc/) (default) and [musl libc](https://www.musl-libc.org/) (see the [build guide]({% link docs/current/dev/building/linux.md %})).
However, note that DuckDB binaries built with musl libc have lower performance.
In practice, this can lead to a slowdown of more than 5× on compute-intensive workloads.
Therefore, it's recommended to use a Linux distribution with glibc for performance-oriented workloads when running DuckDB.

## Memory Allocator

If you have a many-core CPU running on a system where DuckDB ships with [`jemalloc`]({% link docs/current/core_extensions/jemalloc.md %}) as the default memory allocator, consider [enabling the allocator's background threads]({% link docs/current/core_extensions/jemalloc.md %}#background-threads).

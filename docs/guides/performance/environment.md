---
layout: docu
title: Environment
---

The environment where DuckDB is run has an obvious impact on performance. This page focuses on the effects of the hardware configuration and the operating system used.

## Hardware Configuration

### CPU and Memory

As a rule of thumb, aggregation-heavy workloads require approx. 5 GB memory per CPU core and join-heavy workloads require approximately 10 GB memory per core for best performance.
In AWS EC2, the former are available as general-purpose instances (e.g., [M7g](https://aws.amazon.com/ec2/instance-types/m7g/))
and the latter as memory-optimized instances (e.g., [R7g](https://aws.amazon.com/ec2/instance-types/r7g/)).

_**Best Practice:**_ Aim for 5-10 GB memory per CPU core.

### Disk

DuckDB is capable of operating both as an in-memory and as a disk-based database system. In the latter case, it can spill to disk to process larger-than-memory workloads (a.k.a. out-of-core processing). In these cases, a fast disk is highly beneficial. However, if the workload fits in memory, the disk speed only has a limited effect on performance.

In general, network disks – e.g., [NFS](https://en.wikipedia.org/wiki/Network_File_System), network drives on Windows, and network-backed cloud disks (such as [AWS EBS](https://aws.amazon.com/ebs/)) – will result in slower DuckDB workloads than using local disks. However, different network disks can have vastly varying IO performance, ranging from very slow to almost as fast as local. Therefore, for optimal performance, only use network disks that can provide high IO performance.

_**Best Practice:**_ Fast disks are important if your workload is larger than memory and/or fast data loading is important. Only use network-backed disks if they guarantee high IO.

## Operating System

We recommend using the latest stable version of operating systems: macOS, Windows, and Linux are all well-tested and DuckDB can run on them with high performance. Among Linux distributions, we recommended using Ubuntu Linux LTS due to its stability and the fact that most of DuckDB’s Linux test suite jobs run on Ubuntu workers.

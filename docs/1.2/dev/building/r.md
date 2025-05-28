---
layout: docu
title: R
---

This page contains instructions for building the R client library.

## The Build Only Uses a Single Thread

**Problem:**
By default, R compiles packages using a single thread, which causes the build to be slow.

**Solution:**
To parallelize the compilation, create or edit the `~/.R/Makevars` file, and add a line like the following:

```ini
MAKEFLAGS = -j8
```

The above will parallelize the compilation using 8 threads. On Linux/macOS, you can add the following to use all of the machine's threads:

```ini
MAKEFLAGS = -j$(nproc)
```

However, note that, the more threads that are used, the higher the RAM consumption. If the system runs out of RAM while compiling, then the R session will crash.
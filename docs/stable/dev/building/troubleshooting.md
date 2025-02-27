---
layout: docu
redirect_from:
- /docs/dev/building/troubleshooting
title: Troubleshooting
---

This page contains solutions to common problems reported by users. If you have platform-specific issues, make sure you also consult the troubleshooting guide for your platform such as the one for [Linux builds]({% link docs/stable/dev/building/linux.md %}#troubleshooting).

## The Build Runs Out of Memory

**Problem:**
Ninja parallelizes the build, which can cause out-of-memory issues on systems with limited resources.
These issues have also been reported to occur on Alpine Linux, especially on machines with limited resources.

**Solution:**
Avoid using Ninja by setting the Makefile generator to empty via `GEN=`:

```batch
GEN= make
```

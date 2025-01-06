---
layout: docu
title: Raspberry Pi
---

DuckDB can be built for Raspberry Pi.

On 32-bit Raspberry Pi boards, you need to add the [`-latomic` link flag](https://github.com/duckdb/duckdb/issues/13855#issuecomment-2341539339).
As extensions are not distributed for this platform, it's recommended to also include them in the build.
For example:

```batch
mkdir build
cd build
cmake .. \
    -DCORE_EXTENSIONS="httpfs;json;parquet" \
    -DDUCKDB_EXTRA_LINK_FLAGS="-latomic"
make -j4
```

---
layout: docu
redirect_from:
- /docs/dev/building/raspberry_pi
title: Raspberry Pi
---

DuckDB is not officially distributed for the Raspberry Pi OS (previously called Raspbian).
You can build it following the instructions on this page.

## Raspberry Pi (64-bit)

First, install the required build packages:

```bash
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build
```

Then, clone and build it as follows:

```bash
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja BUILD_EXTENSIONS="icu;json" make
```

Finally, run it:

```bash
build/release/duckdb
```

## Raspberry Pi (32-bit)

On 32-bit Raspberry Pi boards, you need to add the [`-latomic` link flag](https://github.com/duckdb/duckdb/issues/13855#issuecomment-2341539339).
As extensions are not distributed for this platform, it's recommended to also include them in the build.
For example:

```bash
mkdir build
cd build
cmake .. \
    -DBUILD_EXTENSIONS="httpfs;json;parquet" \
    -DDUCKDB_EXTRA_LINK_FLAGS="-latomic"
make -j4
```

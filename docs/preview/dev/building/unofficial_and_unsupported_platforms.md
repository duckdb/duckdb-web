---
layout: docu
title: Unofficial and Unsupported Platforms
---

> Warning The platforms listed on this page are not officially supported.
> The build instructions are provided on a best-effort basis.
> Community contributions are very welcome.

DuckDB is built and distributed for several platforms with [different levels of support]({% link docs/preview/dev/building/overview.md %}).
DuckDB _can be built_ for other platforms with varying levels of success.
This page provides an overview of these with the intent to clarify which platforms can be expected to work.

## 32-bit Architectures

[32-bit architectures](https://en.wikipedia.org/wiki/32-bit_computing) are officially not supported but it is possible to build DuckDB manually for some of these platforms.
For example, see the build instructions for [32-bit Raspberry Pi boards]({% link docs/preview/dev/building/raspberry_pi.md %}#raspberry-pi-32-bit).

Note that 32-bit platforms are limited to using 4 GiB RAM due to the amount of addressable memory.

## Big-Endian Architectures

[Big-endian architectures](https://en.wikipedia.org/wiki/Endianness) (such as PowerPC) are [not supported](https://duckdblabs.com/community_support_policy#architectures) by DuckDB.
While DuckDB can likely be built on such architectures,
the resulting binary may exhibit [correctness](https://github.com/duckdb/duckdb/issues/5548) [errors](https://github.com/duckdb/duckdb/issues/9714) on certain operations.
Therefore, its use is not recommended.

## RISC-V Architectures

The user [“LivingLinux” on Bluesky](https://bsky.app/profile/livinglinux.bsky.social) managed to [build DuckDB](https://bsky.app/profile/livinglinux.bsky.social/post/3lak5q7mmg42j) for a [RISC-V](https://en.wikipedia.org/wiki/RISC-V) profile and [published a video about it](https://www.youtube.com/watch?v=G6uVDH3kvNQ). The instructions to build DuckDB, including the `fts` extension, are the following:

```bash
GEN=ninja \
    CC='gcc-14 -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    CXX='g++-14 -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    BUILD_EXTENSIONS='fts' \
    make
```

For those who do not have a RISC-V chip development environment, you can cross-compile DuckDB using the latest [g++-riscv64-linux-gnu](https://github.com/riscv-collab/riscv-gnu-toolchain) :

```bash
GEN=ninja \
    CC='riscv64-linux-gnu-gcc -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    CXX='riscv64-linux-gnu-g++ -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    make
```

For more reference information on DuckDB RISC-V cross-compiling, see the [mocusez/duckdb-riscv-ci](https://github.com/mocusez/duckdb-riscv-ci) and [DuckDB Pull Request #16549](https://github.com/duckdb/duckdb/pull/16549)

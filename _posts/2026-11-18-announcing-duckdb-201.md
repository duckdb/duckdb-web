---
layout: post
title: "Announcing DuckDB 2.0.1 LTS"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/duckdb-release-2-0-1.svg"
image: "/images/blog/thumbs/duckdb-release-2-0-1.png"
excerpt: "TODO"
tag: release
---

TODO: Gather major fixes in DuckDB core, primary clients, and extensions.

TODO: announce new core extensions

## DuckDB 1.4 Reached EOL

TODO: announce this

## Conclusion

We are grateful to the following people, whose reports helped us make DuckDB more robust when reading malformed or corrupted data:

* [@TristanInSec](https://github.com/TristanInSec) for reporting out-of-bounds reads and a string-length buffer sizing overflow in `DICT_FSST` decompression, and for reporting missing validation of Arrow string offsets.
* [@zerovulnlabs](https://github.com/zerovulnlabs) for reporting missing page-size validation when reading uncompressed Parquet V2 pages.

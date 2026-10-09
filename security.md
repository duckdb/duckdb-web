---
layout: default
title: Security
body_class: history blog_typography
max_page_width: medium
toc: true
redirect_from:
- /cve
- /cves
---

<div class="wrap pagetitle">
  <div class="pagetitle-heading" role="heading" aria-level="1">Security</div>
</div>

This page describes DuckDB's security model, how to report a potential vulnerability, and the CVEs that have been filed against DuckDB. For a detailed discussion of DuckDB's security-related settings, see the ["Securing DuckDB"](https://duckdb.org/docs/stable/operations_manual/securing_duckdb/overview) page.

## Security Model

DuckDB is an embedded engine: it runs inside the host process, with the privileges of that process. It has no internal privilege boundary and no notion of an untrusted user inside the engine. The embedding application controls which SQL is executed and which files are opened, and that is the security boundary. DuckDB assumes both inputs are trusted.

* **SQL is executable code**, comparable to Bash or Python. A query can read and write local files, open network connections, install and load extensions, and consume unbounded CPU, memory, and disk. Executing untrusted SQL is unsafe by design, and a query that does any of the above is not a vulnerability. To run untrusted SQL, sandbox at the operating-system level (for example a container, a virtual machine, or [DuckDB-Wasm](https://duckdb.org/docs/stable/clients/wasm/overview)).
* **Data files** (Parquet, CSV, JSON, Arrow, Avro, Iceberg and Delta metadata, and DuckDB database files) are assumed to come from a trusted writer. A crafted or corrupted file may crash the process or allocate unbounded memory. These are fixed as bugs, but are not treated as vulnerabilities. Opening a database file with `ATTACH` is closer to loading a shared library than to opening a document. Do not open data files from untrusted parties.
* **Extensions** execute native code in the host process. A deliberately loaded malicious extension is not a vulnerability, but loading an extension that was not requested, or loading unsigned code while signature checking is enabled, is.

The values *inside* a well-formed file are a separate case and are in scope: column values are frequently attacker controlled, so memory corruption or unexpected file or network access caused by the values in a file, rather than by its structure, is a vulnerability. Bypasses of `enable_external_access`, `allowed_directories`, `disabled_filesystems`, `lock_configuration`, the extension settings, or the CLI safe mode are also in scope. For the complete, authoritative version of this model, see the [`SECURITY.md`](https://github.com/duckdb/duckdb/blob/main/SECURITY.md) policy in the DuckDB repository.

## Reporting a Vulnerability

Please review the [security model](#security-model) first, as many reports fall outside it. To report a potential security issue, use GitHub's [security reporting tool](https://github.com/duckdb/duckdb/security/advisories/new). Our team will investigate and respond. If the report is determined to be an actual security issue, we will request a CVE. We prefer to disclose an issue once a DuckDB release containing the fix has been published. See the [release calendar]({% link release_calendar.md %}) for planned release dates.

For the list of currently supported versions, see the [release calendar]({% link release_calendar.md %}) or DuckDB's [`endoflife.date`](https://endoflife.date/duckdb) page.

## CVEs

The following CVEs have been filed against DuckDB. For each one, we document either the version in which it was fixed or, where a CVE falls outside the [security model](#security-model), the reason it is disputed.

<div class="monospace_table"></div>

| CVE | Status | Description |
|-----|--------|-------------|
| [CVE-2024-22682](https://github.com/advisories/GHSA-fq57-m32w-cmv5) | Disputed | Reports a crash triggered by opening a crafted input file. Opening a data file from an untrusted party is outside DuckDB's [security model](#security-model): a crafted or corrupted file may crash the process, and we fix such crashes as bugs rather than treating them as vulnerabilities. |

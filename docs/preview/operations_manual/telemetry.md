---
layout: docu
title: Telemetry
---

## HTTP user-agent

Core DuckDB sets the default user agent as follows:

```
duckdb/v1.4.4(osx_arm64) cli 6ddac802ff
```

which indicates version, architecture, client, buildref in the agent string. The user-agent string can also be modified via the `custom_user_agent` setting, see [Configuration](https://duckdb.org/docs/stable/configuration/overview).

In addition, some extensions set their own user agents; notable examples here include:

## Extensions

### Azure

Azure uses the Azure SDK which sets its own user agents. For identity and storage calls you may see respectively strings like these:

- AZURE-ID: `azsdk-cpp-identity/1.11.0 (Darwin 25.2.0 arm64 Darwin Kernel Version 25.2.0: Tue Nov 18 21:07:05 PST 2025; root:xnu-12377.61.12~1/RELEASE_ARM64_T6020 Cpp/201402)`
- AZURE-BLOB/ADLS: `azsdk-cpp-storage-blobs/12.15.0 (Darwin 25.2.0 arm64 Darwin Kernel Version 25.2.0: Tue Nov 18 21:07:05 PST 2025; root:xnu-12377.61.12~1/RELEASE_ARM64_T6020 Cpp/201402)`

### Delta (and Unity Catalog)

The Delta extension employs calls from DuckDB core, tagged as the duckdb default above, and also has calls originating from the Delta Kernel, which may look like:

- `object_store/0.12.5`

Unity Catalog calls also use a mix of duckdb default user-agents, and the Delta style agent above.

### HTTPFS - HTTPS/S3

Calls via HTTPFS the extension use the duckdb default strings noted above.

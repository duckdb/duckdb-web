---
layout: docu
redirect_from:
- /docs/preview/operations_manual/user_agents
- /docs/stable/operations_manual/user_agents
title: HTTP User-Agent
---

## HTTP User-Agent

Core DuckDB sets the default user-agent as follows:

```text
duckdb/v1.4.4(osx_arm64) cli 6ddac802ff
```

which indicates version, architecture, client, buildref in the agent string. The user-agent string can also be modified via the `custom_user_agent` setting, see [Configuration]({% link docs/current/configuration/overview.md %}). The currently generated user-agent string can be seen via `PRAGMA user_agent;`, see [Configuration/Pragmas]({% link docs/current/configuration/pragmas.md %}#user-agent).

In addition, some extensions set their own user agents; notable examples here include the following.

## Extensions

### Azure

Azure uses the Azure SDK which sets its own user agents. For identity and storage calls you may see respectively strings like these:

- via Azure Identity: `azsdk-cpp-identity/1.11.0 (Darwin 25.2.0 arm64 Darwin Kernel Version 25.2.0: Tue Nov 18 21:07:05 PST 2025; root:xnu-12377.61.12~1/RELEASE_ARM64_T6020 Cpp/201402)`
- via Azure Blob/ADLSv2: `azsdk-cpp-storage-blobs/12.15.0 (Darwin 25.2.0 arm64 Darwin Kernel Version 25.2.0: Tue Nov 18 21:07:05 PST 2025; root:xnu-12377.61.12~1/RELEASE_ARM64_T6020 Cpp/201402)`

### Delta (and Unity Catalog)

The Delta extension employs calls from DuckDB core, tagged as the DuckDB default above, and also has calls originating from the Delta Kernel, which may look like:

- `object_store/0.12.5`

Unity Catalog calls also use a mix of DuckDB default user-agents, and the Delta style agent above.

### HTTPFS - HTTPS/S3

Calls via HTTPFS the extension use the DuckDB default strings noted above.

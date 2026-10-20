---
layout: docu
redirect_from:
- /docs/stable/guides/troubleshooting/command_line
- /docs/current/guides/troubleshooting/command_line
- /docs/lts/guides/troubleshooting/command_line
- /docs/preview/guides/troubleshooting/command_line
title: Command Line
---

## Unexpected Markdown Output When Piping

If the output of the [command line client]({% link docs/2.0/clients/cli/overview.md %}) is piped to another process and an AI agent environment variable (such as `AI_AGENT`) is set, the CLI switches to [agent mode]({% link docs/2.0/clients/cli/agent_mode.md %}) and prints compact Markdown tables instead of the usual duckbox tables:

```bash
echo "SELECT 42 AS x;" | duckdb | cat
```

```text
| x:INTEGER |
|---|
| 42 |
```

To turn off agent mode, use the `-no-agent` [command line argument]({% link docs/2.0/clients/cli/arguments.md %}) or set the `DUCKDB_AGENT_MODE` environment variable to `0`:

```bash
echo "SELECT 42 AS x;" | duckdb -no-agent | cat
```

```text
┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

Passing an explicit [output mode]({% link docs/2.0/clients/cli/output_formats.md %}) flag, such as `-csv` or `-json`, also disables agent mode.

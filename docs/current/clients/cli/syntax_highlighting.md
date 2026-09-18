---
layout: docu
redirect_from:
- /docs/api/cli/syntax_highlighting
- /docs/clients/cli/syntax_highlighting
- /docs/preview/clients/cli/syntax_highlighting
- /docs/stable/clients/cli/syntax_highlighting
title: Syntax Highlighting
---

> Syntax highlighting in the CLI is currently only available for macOS and Linux.

SQL queries that are written in the shell are automatically highlighted using syntax highlighting.

![Image showing syntax highlighting in the shell](/images/syntax_highlighting_screenshot.png)

There are several components of a query that are highlighted in different colors. The colors can be configured using the `.highlight_colors` [dot command]({% link docs/current/clients/cli/dot_commands.md %}):
Syntax highlighting can also be disabled entirely using the `.highlight off` command.

Below is a list of query components that can be configured.
|          Type           |       Component         | Default color |
|-------------------------|-------------------------|---------------|
| Keywords                | `keyword`               | `green`       |
| Numeric constants       | `numeric_constant`      | `yellow`      |
| String constants        | `string_constant`       | `yellow`      |
| Comments                | `comment`               | `gray`        |
| Errors                  | `error`                 | `red`         |
| Continuation            | `continuation`          | `gray`        |
| Continuation (Selected) | `continuation_selected` | `green`       |

Colors are specified by name. The following basic colors are supported by all terminals:

`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `brightgray`, `gray`, `brightred`, `brightgreen`, `brightyellow`, `brightblue`, `brightmagenta`, `brightcyan`, `white`

In addition, 8-bit colors can be used. Run `.display_colors` to list all available color names, see [8-Bit Colors]({% link docs/current/clients/cli/friendly_cli.md %}#8-bit-colors).

The optional intensity can be `standard`, `bold`, `underline` or `bold_underline`.

For example, here is an alternative set of syntax highlighting colors:

```text
.highlight_colors keyword brightred bold
.highlight_colors numeric_constant white
.highlight_colors string_constant white
.highlight_colors comment cyan
.highlight_colors error yellow
.highlight_colors continuation blue
.highlight_colors continuation_selected brightblue
```

If you wish to start up the CLI with a different set of colors every time, you can place these commands in the `~/.duckdbrc` file that is loaded on start-up of the CLI.

## Error Highlighting

The shell has support for highlighting certain errors. In particular, mismatched brackets and unclosed quotes are highlighted in red (or another color if specified). This highlighting is automatically disabled for large queries. In addition, it can be disabled manually using the `.render_errors off` command.

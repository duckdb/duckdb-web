---
layout: docu
title: Syntax Highlighting
---

> Syntax highlighting in the CLI is currently only available for macOS and Linux.

SQL queries that are written in the shell are automatically highlighted using syntax highlighting.

![Image showing syntax highlighting in the shell](/images/syntax_highlighting_screenshot.png)

There are several components of a query that are highlighted in different colors. The colors can be configured using [dot commands](dot_commands).
Syntax highlighting can also be disabled entirely using the `.highlight off` command.

Below is a list of components that can be configured.

|          Type           |  Command  | Default Color |
|-------------------------|-----------|---------------|
| Keywords                | .keyword  | green         |
| Constants & Literals    | .constant | yellow        |
| Comments                | .comment  | brightblack   |
| Errors                  | .error    | red           |
| Continuation            | .cont     | brightblack   |
| Continuation (Selected) | .cont_sel | green         |

The components can be configured using either a supported color name (e.g. `.keyword red`), or by directly providing a terminal code to use for rendering (e.g. `.keywordcode \033[31m`). Below is a list of supported color names and their corresponding terminal codes.

|     Color     | Terminal Code |
|---------------|---------------|
| red           | `\033[31m`    |
| green         | `\033[32m`    |
| yellow        | `\033[33m`    |
| blue          | `\033[34m`    |
| magenta       | `\033[35m`    |
| cyan          | `\033[36m`    |
| white         | `\033[37m`    |
| brightblack   | `\033[90m`    |
| brightred     | `\033[91m`    |
| brightgreen   | `\033[92m`    |
| brightyellow  | `\033[93m`    |
| brightblue    | `\033[94m`    |
| brightmagenta | `\033[95m`    |
| brightcyan    | `\033[96m`    |
| brightwhite   | `\033[97m`    |

For example, here is an alternative set of syntax highlighting colors:

```text
.keyword brightred
.constant brightwhite
.comment cyan
.error yellow
.cont blue
.cont_sel brightblue
```

If you wish to start up the CLI with a different set of colors every time, you can place these commands in the `~/.duckdbrc` file that is loaded on start-up of the CLI.

## Error Highlighting

The shell has support for highlighting certain errors. In particular, mismatched brackets and unclosed quotes are highlighted in red (or another color if specified). This highlighting is automatically disabled for large queries. In addition, it can be disabled manually using the `.render_errors off` command.

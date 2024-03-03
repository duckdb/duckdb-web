---
layout: docu
title: Editing
---

> The linenoise-based CLI editor is currently only available for macOS and Linux.

DuckDB's CLI uses a line-editing library based on [linenoise](https://github.com/antirez/linenoise), which has short-cuts that are based on [Emacs mode of readline](https://readline.kablamo.org/emacs.html). Below is a list of available commands.

## Moving

<div class="narrow_table"></div>

|      Key      |                                 Action                                 |
|---------------|------------------------------------------------------------------------|
| Left          | Move back a character                                                  |
| Right         | Move forward a character                                               |
| Up            | Move up a line. When on the first line, move to previous history entry |
| Down          | Move down a line. When on last line, move to next history entry        |
| Home          | Move to beginning of buffer                                            |
| End           | Move to end of buffer                                                  |
| Ctrl+Left     | Move back a word                                                       |
| Ctrl+Right    | Move forward a word                                                    |
| Ctrl+A        | Move to beginning of buffer                                            |
| Ctrl+B        | Move back a character                                                  |
| Ctrl+E        | Move to end of buffer                                                  |
| Ctrl+F        | Move forward a character                                               |
| Alt+Left      | Move back a word                                                       |
| Alt+Right     | Move forward a word                                                    |

## History

<div class="narrow_table"></div>

| Key    | Action                         |
|--------|--------------------------------|
| Ctrl+P | Move to previous history entry |
| Ctrl+N | Move to next history entry     |
| Ctrl+R | Search the history             |
| Ctrl+S | Search the history             |
| Alt+<  | Move to first history entry    |
| Alt+>  | Move to last history entry     |
| Alt+N  | Search the history             |
| Alt+P  | Search the history             |

## Changing Text

<div class="narrow_table"></div>

| Key           | Action                                                   |
|---------------|----------------------------------------------------------|
| Backspace     | Delete previous character                                |
| Delete        | Delete next character                                    |
| Ctrl+D        | Delete next character. When buffer is empty, end editing |
| Ctrl+H        | Delete previous character                                |
| Ctrl+K        | Delete everything after the cursor                       |
| Ctrl+T        | Swap current and next character                          |
| Ctrl+U        | Delete all text                                          |
| Ctrl+W        | Delete previous word                                     |
| Alt+C         | Convert next word to titlecase                           |
| Alt+D         | Delete next word                                         |
| Alt+L         | Convert next word to lowercase                           |
| Alt+R         | Delete all text                                          |
| Alt+T         | Swap current and next word                               |
| Alt+U         | Convert next word to uppercase                           |
| Alt+Backspace | Delete previous word                                     |
| Alt+\         | Delete spaces around cursor                              |

## Completing

<div class="narrow_table"></div>

|    Key    |                          Action                        |
|-----------|--------------------------------------------------------|
| Tab       | Autocomplete. When autocompleting, cycle to next entry |
| Shift+Tab | When autocompleting, cycle to previous entry           |
| ESC+ESC   | When autocompleting, revert autocompletion             |

## Miscellaneous

<div class="narrow_table"></div>

|  Key   |                           Action                                                   |
|--------|------------------------------------------------------------------------------------|
| Enter  | Execute query. If query is not complete, insert a newline at the end of the buffer |
| Ctrl+J | Execute query. If query is not complete, insert a newline at the end of the buffer |
| Ctrl+C | Cancel editing of current query                                                    |
| Ctrl+G | Cancel editing of current query                                                    |
| Ctrl+L | Clear screen                                                                       |
| Ctrl+O | Cancel editing of current query                                                    |
| Ctrl+X | Insert a newline after the cursor                                                  |
| Ctrl+Z | Suspend CLI and return to shell, use `fg` to re-open                               |

## Using Read-Line

If you prefer, you can use [`rlwrap`](https://github.com/hanslub42/rlwrap) to use read-line directly with the shell. Then, use Shift+Enter to insert a newline and Enter to execute the query:

```bash
rlwrap --substitute-prompt="D " duckdb -batch
```

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the source for [duckdb.org](https://duckdb.org) — a Jekyll 4.4.1 static site hosting the DuckDB documentation, blog, and marketing pages.

## Setup

```bash
# Ruby dependencies
bundle install

# Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development Commands

```bash
# Serve locally (latest stable only, faster — recommended for most editing)
scripts/serve-latest.sh

# Serve full site including all archived versions
scripts/serve.sh

# Run linters (markdownlint, vale, black)
scripts/lint.sh

# Auto-fix lint issues
scripts/lint.sh -f
```

Visit `http://localhost:4000/docs/` (use HTTP, not HTTPS).

## Architecture

### Site Generator
Jekyll with Kramdown/GFM markdown. Navigation menus are driven by JSON data files, not auto-discovered from files.

### Documentation Versioning
- `docs/stable/` — current stable release (target for most PRs)
- `docs/preview/` — nightly/dev release
- `docs/1.3/`, `docs/1.2/`, etc. — archived versions (rarely edited)

The `_config_exclude_archive.yml` config is used by `serve-latest.sh` to skip archived versions for faster local builds.

### Adding a New Doc Page
1. Create a Markdown file using `snake_case` naming in `docs/stable/`
2. Add an entry to `_data/menu_docs_stable.json` for sidebar navigation
3. For a new guide, also add a link in `docs/stable/guides/overview.md`

### Generated Pages
Many pages under `docs/stable/sql/functions/` are auto-generated. Check `scripts/generate_all_docs.sh` before editing — do not edit generated content directly. Source data lives in the [`duckdb/duckdb`](https://github.com/duckdb/duckdb) repository.

### Front Matter
Every doc page uses Jekyll front matter:
```yaml
---
layout: docu
title: Page Title
---
```

### Internal Links
Always use Jekyll link tags (not relative paths):
```markdown
{% link docs/stable/sql/statements/select.md %}
```
Link tags cause build failures if the target doesn't exist, catching broken links at build time.

## Style Guide

### Markdown
- No hard line breaks; do not use `<br/>` or double trailing spaces
- Unordered lists use `*` (not `-`); 4-space indentation for nesting
- Use `"` `"` and `'` `'` for smart quotes
- Page title goes in front matter `title:` only — do not repeat as an `h1` in the body
- Body headers: `##`, `###`, `####` only
- Header capitalization: [Chicago Manual of Style](https://capitalizemytitle.com/style/Chicago/)
- Spelling: American English, no Oxford comma

### Code Block Language Tags

| Tag | Renders as |
|-----|-----------|
| `sql` | SQL, no prompt |
| `plsql` | SQL with `D` prompt |
| `batch` | Shell with `$` prompt |
| `bash` | Shell, no prompt |
| `text` | Plain output |
| `console` | Error messages |

### SQL Style
- Uppercase keywords: `SELECT`, `FROM`, `WHERE`
- Lowercase function names: `cos()`, `date_part()`
- `snake_case` for table/column names
- 4-space indentation, trailing semicolons, commas at end of line
- Placeholders use `⟨angle brackets⟩` (not `<>`, `[]`, or `{}`)
- Do not include the `D ` prompt in SQL examples

### Callout Boxes
Blockquotes render as colored callout boxes. Types: `Note` (default), `Warning`, `Tip`, `Bestpractice`, `Deprecated`.

### Tables
- Prepend `<div class="monospace_table"></div>` for code-heavy output tables
- Prepend `<div class="center_aligned_header_table"></div>` for centered headers

---
layout: docu
title: Harlequin SQL IDE
selected: Harlequin SQL IDE
---

[Harlequin](https://github.com/tconbeer/harlequin) is an open-source, terminal-based SQL IDE for DuckDB. You can install it using `pip` and run it anywhere you can run the DuckDB CLI.

![The Harlequin IDE](/images/guides/harlequin.png)

### Installing Harlequin

After installing Python 3.8 or above, install Harlequin using `pip` or `pipx` with:

```bash
pip install harlequin
```

### Using Harlequin

From any shell, to open a DuckDB database file:

```bash
harlequin "path/to/duck.db"
```

To open an in-memory DuckDB session, run Harlequin with no arguments:

```bash
harlequin
```

#### Viewing the Schema of your Database

When Harlequin is open, you can view the schema of your DuckDB database in the left sidebar. You can use your mouse or the arrow keys + enter to navigate the tree. The tree shows schemas, tables/views and their types, and columns and their types.

#### Editing a Query

The main query editor is a full-featured text editor, with features including syntax highlighting, auto-formatting with ``ctrl + ` ``, text selection, copy/paste, and more.

You can save the query currently in the editor with `ctrl + s`. You can open a query in any text or .sql file with `ctrl + o`.

#### Running a Query and Viewing Results

To run a query, press `ctrl + enter`. Up to 50k records will be loaded into the results pane below the query editor. When the focus is on the data pane, you can use your arrow keys or mouse to select different cells.

#### Exiting Harlequin

Press `ctrl + q` to quit and return to your shell.

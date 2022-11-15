---
layout: docu
title: Tad - A Tabular Data Viewer
selected: Tad - A Tabular Data Viewer
---

# How to use Tad to view tabular data files and DuckDb databases

[Tad](https://www.tadviewer.com) is a fast, free cross-platform tabular data viewer application powered by DuckDb.  There are [pre-built binary installers](https://github.com/antonycourtney/tad/releases/latest) available for Mac, Windows and Linux, and full
source code is available on [github](https://github.com/antonycourtney/tad).

Tad is a low friction way to explore tabular data files (CSV and Parquet) as well as 
SQLite and DuckDb database files. A dirty little secret of the data world is that workflows often involve using commercial spreadsheet apps like Excel to take a quick peek at the contents of a tabular data file (like a CSV) before analysis work begins. Tad provides a pleasant (and free) alternative to this, and (thanks to DuckDb!) is much faster than Excel at opening CSV files. How much faster?  On a 2019 MacBook Pro, opening MetObjects.csv, a 230 MB CSV with 450k rows takes around 33 seconds to open with the latest version of Excel. This same file opens in under 5 seconds in Tad.  

Unlike commercial spreadsheet applications, Tad also natively supports Parquet files. Since DuckDb operates on Parquet files in place without an extra import step, the speed for opening Parquet files is pretty mind-blowing.  Here is Tad browsing a directory of multi-million-row Parquet files from the TPC-H-SF10 benchmark data set:

![Tad-parquet](/images/guides/tad-parquet-browsing.gif)

# Data Exploration with Tad

For data exploration, the core of Tad is a hierarchical pivot table that allows you to specify a combination of pivot, filter, aggregate, sort, column selection, column ordering and basic column formatting operations directly in the UI. Tad delegates
to a SQL database (DuckDb!) for storage and analytics, and generates SQL queries to perform all analytic operations specified in the UI.  Here is a quick view of using Tad to pivot and sort a tabular data file:

![tad-metobjects-pivoted](/images/guides/tad-pivot-table.png)

# Launching Tad

There are three ways to launch Tad:
  1. **Application Icon**: You can double click on the Tad application icon to open Tad.  Use <strong>File...Open</strong> and the standard file open dialog to open a tabular data file in any of the supported file formats.
  2. **Context Menu or Drag and Drop**: The installation process registers Tad as a viewer for the supported file format extensions. On any <code>.csv</code> or <code> parquet</code>file in the Finder (macOS) or Explorer (Windows), use <strong>Open With...</strong> and select <strong>Tad</strong> to open the file in Tad.
  3. **Command Line**: Once Tad is installed and available on your PATH, simply type:
```
$ tad somefile.csv
```
to launch Tad to explore the file. You can also open <code>.tad</code> files (previously saved Tad view configurations) and all the other supported file types via the command line.

# Browsing Database Files

Of particular interest to DuckDb users, Tad can serve as a lightweight browser for DuckDb and SQLite database files.  Just run:
```sh
$ tad myDatabase.duckdb
```
from the command line to get a browsable view of the tables in a DuckDb database file.
This also works for sqlite databases (files with a `.sqlite` extension).

# Peeking Under The Bonnet

If for some reason you want to see the gnarly details of the SQL queries that Tad is constructing and executing, you can use the <code>-f</code> option on the command line to keep Tad in the foreground and <code>--show-queries</code> to get Tad to print the generated SQL queries like so:
```
$ tad -f --show-queries somefile.csv
```
Not for the faint-hearted.

# Downloading and Installing Tad

You can download pre-built installers for Mac, Linux and Windows from the [Tad github releases page](https://github.com/antonycourtney/tad/releases/latest).

# Help / Bug Reports / Feedback

Please send any questions, feedback, bug reports, and feature requests to
[tad-feedback@tadviewer.com](mailto:tad-feedback@tadviewer.com). 

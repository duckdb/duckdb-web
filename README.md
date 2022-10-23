# DuckDB Website

<div align="center">
  <img src="./images/duckdb_logo_dl.svg" height="50">
</div>
<p>&nbsp;</p>

This repository hosts the source code for the [DuckDB Website](www.duckdb.org). Please file any  questions or issues relating to the website or documentation here.

The main DuckDB repository is hosted [here](https://github.com/duckdb/duckdb).

## Building

The site is built using [Jekyll](https://jekyllrb.com/). To build the site locally, install ruby, and run `bundler` to install the dependencies. If you are on Windows, you must then run these two commands:

```sh
gem uninstall eventmachine
gem install eventmachine --platform ruby
```

You might have to install `webrick` to get `jekyll serve` to work, you can do so by running `gem install webrick`.
Finally, navigate to the directory where you have cloned duckdb-web and run `bundler exec jekyll serve`. The website can then be browsed by going to `localhost:4000` in your browser.

## Generating code docs

Much of the documentation in this repository is automatically generated from the duckdb source code, or compiled binaries. The scripts that do this work are called from [`scripts/generate_all_docs.sh`](scripts/generate_all_docs.sh)

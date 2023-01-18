# DuckDB Website

<div align="center">
  <img src="./images/duckdb_logo_dl.svg" height="50">
</div>
<p>&nbsp;</p>

This repository hosts the source code for the [DuckDB Website](https://duckdb.org). Please file any  questions or issues relating to the website or documentation here.

The main DuckDB repository is hosted [here](https://github.com/duckdb/duckdb).

## Adding a new page

First, thank you for your contribution!

Each new page requires at least 2 edits:
* The creation of a new markdown page with the documentation. Please follow the format of another .md file in the docs folder.
* Add a link to the new page within _data/menu_docs_current.json. This populates the dropdown menus.

The addition of a new guide requires one additional edit:
* Add a link to the new page within the Guides landing page: docs/guides/index.md

Each new page must also be added to the Search feature. Either manually edit the file _data/search_data.json or:
* Install Python
* Clone this repo and navigate to it
* Create a new Python virtual environment
* pip install -r requirements.txt
* python scripts/generate_search.py

**Please test your changes using the steps listed in the Building section below.**

**When creating a PR, please check the box to "Allow edits from maintainers".**

Please enclose code in blocks that are tagged with the appropriate language. (Ex: \`\`\`sql CODE HERE \`\`\`). 

All examples should be self contained and reproducible if possible, meaning that any example tables are created as a part of the documentation.

Feedback is welcome on these contribution steps as well!

## Building

The site is built using [Jekyll](https://jekyllrb.com/). To build the site locally, install ruby, and run `bundler` to install the dependencies. If you are on Windows, you must then run these two commands:

```sh
gem uninstall eventmachine
gem install eventmachine --platform ruby
```

You might have to install `webrick` to get `jekyll serve` to work, you can do so by running `gem install webrick`.
Finally, navigate to the directory where you have cloned duckdb-web and run `bundler exec jekyll serve`. The website can then be browsed by going to `localhost:4000` in your browser.

## Generating code docs

Much of the documentation in this repository is automatically generated from the duckdb source code, or compiled binaries. The scripts that do this work are called from [`scripts/generate_all_docs.sh`](scripts/generate_all_docs.sh).

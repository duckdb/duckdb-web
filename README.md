# DuckDB Website

<div align="center">
  <img src="./images/duckdb_logo_dl.svg" height="50">
</div>
<p>&nbsp;</p>

This repository hosts the source code for the [DuckDB Website](www.duckdb.org). Please file any  questions or issues relating to the website or documentation here.

The main DuckDB repository is hosted [here](https://github.com/duckdb/duckdb).


## Building
<<<<<<< HEAD
The site is built using [Jekyll](https://jekyllrb.com/). To build the site locally, install the minima theme `gem install "jekyll-theme-minima"` and
run `jekyll serve`. The website can then be browsed by going to `localhost:4000` in your browser.
=======
The site is built using [Jekyll](https://jekyllrb.com/). To build the site locally, first install the minima theme `gem install "jekyll-theme-minima"`. If you are on Windows, you must then run these two commands: 
```
gem uninstall eventmachine
gem install eventmachine --platform ruby
```
Finally, navigate to the directory where you have cloned duckdb-web and run `jekyll serve`. The website can then be browsed by going to `localhost:4000` in your browser.
>>>>>>> a56802346631e20c76de435b493c4ec4b6e490a4


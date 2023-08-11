# Building the DuckDB documentation

The site is built using [Jekyll](https://jekyllrb.com/) used by GitHub Pages.

## Locally

To build the site locally, follow [GitHub's instructions](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll).
Alternatively, install Ruby (using the version specified in the `.ruby-version` file), and run `bundler` to install the dependencies. If you are on Windows, you must then run these two commands:

```bash
gem uninstall eventmachine
gem install eventmachine --platform ruby
```

## With a Dev Container

Click the green Code button to the top right to open a new codespace with this repository initialized.

## Serve the site using a local Jekyll installation

Navigate to the directory where you have cloned `duckdb-web`.

Serve the website (latest only, archives excluded) with:

```bash
scripts/serve.sh
```

The website can then be browsed by going to <http://localhost:4000/docs/> in your browser.

Serve the full website with:

```sh
scripts/serve-full.sh
```

## Serve the site from Docker

For portability, we provide a [Docker image](Dockerfile).

First, build the image using:

```sh
scripts/docker-build.sh
```

Serve the website (latest only, archives excluded) with:

```sh
scripts/docker-serve.sh
```

Serve the full website with:

```sh
scripts/docker-serve-full.sh
```

To stop the container, run:

```sh
scripts/docker-stop.sh
```

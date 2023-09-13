# Building the DuckDB documentation

The site is built using [Jekyll](https://jekyllrb.com/) used by GitHub Pages.

## Using a local Jekyll installation

### Prerequisites

To install Jekyll, follow [GitHub's instructions](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll).
Alternatively, install Ruby (using the version specified in the `.ruby-version` file), and run `bundler` to install the dependencies. If you are on Windows, you must then run these two commands:

```bash
gem uninstall eventmachine
gem install eventmachine --platform ruby
```

### Syntax highlighter

We use [a fork of the Rouge syntax highligher](https://github.com/duckdb/rouge/blob/duckdb/lib/rouge/lexers/sql.rb), which is extended with keywords not in standard SQL (e.g., `RETURNING`, `ASOF`). This is automatically installed by `bundler`.

### Serving the site using a local Jekyll installation

Serve the website (latest only, archives excluded) with:

```bash
scripts/serve.sh
```

The website can then be browsed by going to <http://localhost:4000/docs/> in your browser.

Serve the full website with:

```sh
scripts/serve-full.sh
```

## Using Docker

### Prerequisites

Install [Docker](https://docs.docker.com/get-docker/).

### Serving the site from Docker

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

## With a Dev Container

If you are using a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers), click the green Code button to the top right to open a new codespace with this repository initialized.

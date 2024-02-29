# Building the DuckDB documentation

## Table of contents

- [Building the DuckDB documentation](#building-the-duckdb-documentation)
  - [Table of contents](#table-of-contents)
  - [Using a local Jekyll installation](#using-a-local-jekyll-installation)
    - [Prerequisites](#prerequisites)
      - [Ruby](#ruby)
      - [Jekyll](#jekyll)
      - [Syntax highlighter](#syntax-highlighter)
    - [Serving the site using a local Jekyll installation](#serving-the-site-using-a-local-jekyll-installation)
  - [Using Docker](#using-docker)
    - [Prerequisites](#prerequisites-1)
    - [Serving the site from Docker](#serving-the-site-from-docker)
  - [With a Dev Container](#with-a-dev-container)
  - [Generating the search index](#generating-the-search-index)

The site is built using [Jekyll](https://jekyllrb.com/) used by GitHub Pages.

## Using a local Jekyll installation

### Prerequisites

The site is built using [Jekyll](https://jekyllrb.com/) 3.9.x.

#### Ruby

Jekyll 3.9.x requires Ruby v2.7.x+. Note that in some systems, the built-in Ruby distribution is older. On macOS, you can install a new Ruby version via [Homebew](https://brew.sh/):

```bash
brew install ruby
```

Then, place it on the path via:

```bash
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc
```

You may also consider using the cross-platform [Ruby Version Manager (RVM)](https://rvm.io/) for installing a custom Ruby version.

#### Jekyll

Install Jekyll and the other required Ruby dependencies using Bundler:

```bash
bundle install
```

If you are on Windows, run these two commands to ensure Jekyll works:

```bash
gem uninstall eventmachine
gem install eventmachine --platform ruby
```

For more details on using Jekyll, consult [GitHub's instructions](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll).

#### Syntax highlighter

We use [a fork of the Rouge syntax highligher](https://github.com/duckdb/rouge/blob/duckdb/lib/rouge/lexers/sql.rb), which is extended with keywords not in standard SQL (e.g., `RETURNING`, `ASOF`). This is automatically installed by Bundler.

### Serving the site using a local Jekyll installation

Serve the website (latest only, archives excluded) with:

```bash
scripts/serve.sh
```

The website can be browsed by going to <http://localhost:4000/docs/> in your browser.

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
scripts/docker-serve-latest.sh
```

The website can be browsed by going to <http://localhost:4000/docs/> in your browser.

Serve the full website with:

```sh
scripts/docker-serve.sh
```

To stop the container, run:

```sh
scripts/docker-stop.sh
```

## With a Dev Container

If you are using a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers), click the green Code button to the top right to open a new codespace with this repository initialized.

## Generating the search index

To generate the search index, run:

```bash
scripts/install-dependencies.sh
scripts/generate-search-index.sh
```

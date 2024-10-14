# Building the DuckDB documentation

## Table of contents

* [Building the DuckDB documentation](#building-the-duckdb-documentation)
  * [Table of contents](#table-of-contents)
  * [Using a local Jekyll installation](#using-a-local-jekyll-installation)
    * [Prerequisites](#prerequisites)
    * [Serving the site using a local Jekyll installation](#serving-the-site-using-a-local-jekyll-installation)
  * [Using Docker](#using-docker)
    * [Prerequisites](#prerequisites-1)
    * [Serving the site from Docker](#serving-the-site-from-docker)
  * [With a Dev Container](#with-a-dev-container)
  * [Generating the search index](#generating-the-search-index)
  * [Updating the release calendar](#updating-the-release-calendar)
  * [Syntax highlighter](#syntax-highlighter)
  * [Troubleshooting](#troubleshooting)
    * [Jekyll doesn't work on Windows](#jekyll-doesnt-work-on-windows)
    * [Cannot install dependency](#cannot-install-dependency)
    * [Jekyll fails](#jekyll-fails)
    * [Bundle update fails](#bundle-update-fails)

The site is built using [Jekyll](https://jekyllrb.com/) used by GitHub Pages.

## Using a local Jekyll installation

### Prerequisites

1. The site is built using [Jekyll](https://jekyllrb.com/). For instructions on setting up Ruby for Jekyll, please visit the [Installation page of Jekyll](https://jekyllrb.com/docs/installation/macos/).

2. Install Jekyll and the other required Ruby dependencies using Bundler:

    ```bash
    bundle install
    ```

    For more details on setting up Jekyll, consult [GitHub's instructions](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll).

### Serving the site using a local Jekyll installation

To serve this website, run:

```bash
scripts/serve-latest.sh
```

Visit <http://localhost:4000/docs/> to browse the website.

Note that to save time on building, the `serve-latest.sh` script only deploys the latest stable version and exclude the archives. To serve the full website with old versions included, run:

```bash
scripts/serve.sh
```

## Using Docker

### Prerequisites

Install [Docker](https://docs.docker.com/get-docker/).

### Serving the site from Docker

For portability, we provide a [Docker image](Dockerfile).

First, build the image using:

```bash
scripts/docker-build.sh
```

Serve the website (latest only, archives excluded) with:

```bash
scripts/docker-serve-latest.sh
```

To browse the website, visit <http://localhost:4000/docs/>.

Serve the full website with:

```bash
scripts/docker-serve.sh
```

To stop the container, run:

```bash
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

## Updating the release calendar

The release calendar is updated automatically by [CI](.github/workflows/jekyll.yml). To manually update the release calendar, run:

```bash
python scripts/get_calendar.py
```

## Syntax highlighter

We use [a fork of the Rouge syntax highligher](https://github.com/duckdb/rouge/blob/duckdb/lib/rouge/lexers/sql.rb), which is extended with keywords not in standard SQL (e.g., `RETURNING`, `ASOF`). This is automatically installed by Bundler.

## Troubleshooting

### Jekyll doesn't work on Windows

If you are on Windows, run these two commands to ensure Jekyll works:

```bash
gem uninstall eventmachine
gem install eventmachine --platform ruby
```

### Cannot install dependency

The following error occurs:

```console
posix-spawn.c:226:27: error: incompatible function pointer types passing 'int (VALUE, VALUE, posix_spawn_file_actions_t *)' (aka 'int (unsigned long, unsigned long,
```

The workaround is to run the following `bundle` command:

```bash
bundle config set --global build.posix-spawn "--with-cflags=-Wno-error=incompatible-function-pointer-types"
```

### Jekyll fails

After upgrading Ruby, Jekyll fails with the following error message:

```console
/opt/homebrew/opt/ruby/bin/bundler:25:in `load': cannot load such file -- /opt/homebrew/lib/ruby/gems/3.3.0/gems/bundler-2.5.4/exe/bundler (LoadError)
	from /opt/homebrew/opt/ruby/bin/bundler:25:in `<main>'
```

The solution is to run the following commands in the repository:

```bash
gem install bundler
bundle install
```

If this workaround is not sufficient, you likely have to upgrade your Bundler version.
To do so, run:

```bash
rm Gemfile.lock
bundle install
```

### Bundle update fails

Bundle update fails with the following error message:

```bash
bundle update
```

```console
Git error: command `git fetch --force --quiet
/opt/homebrew/lib/ruby/gems/3.3.0/cache/bundler/git/minima-4abf4ea566b1c7c640342d1bbff5586f3c10dd05 --depth 1
1d5286cf9a1aae34078420d183d560dd673d98b5` in directory /opt/homebrew/lib/ruby/gems/3.3.0/bundler/gems/minima-1d5286cf9a1a has failed.
fatal: '/opt/homebrew/lib/ruby/gems/3.3.0/cache/bundler/git/minima-4abf4ea566b1c7c640342d1bbff5586f3c10dd05' does not appear to be a git
repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

To resolve this, clean the Jekyll gem cache:

```bash
rm -rf /opt/homebrew/lib/ruby/gems/3.3.0/cache/
```

### Bundle install fails

Bundle install fails with the following error message:

```bash
bundle install
```

```console
The running version of Bundler (2.5.11) does not match the version of the specification installed for it (2.5.18). This can be caused by
reinstalling Ruby without removing previous installation, leaving around an upgraded default version of Bundler. Reinstalling Ruby from
scratch should fix the problem.
```

The solution, according to a [Stack Overflow answer](https://stackoverflow.com/a/63761800), is to run:

```bash
gem update --system
```

### `ERROR bad URI`

The following error occurs when trying to access the locally built website via HTTPS (`https://localhost:4000/`).

```console
[2024-09-17 12:15:36] ERROR bad URI `����\x12`�\x17\x03�L\x00\x00\x14�'.
[2024-09-17 12:15:36] ERROR bad Request-Line ...
```
This happens frequently with browsers looking to force an HTTPS connection such as Safari.
The solution is to use an HTTP connection (`http://localhost:4000`) and optionally try another browser (e.g., Chrome or Firefox).

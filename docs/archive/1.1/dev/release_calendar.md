---
layout: docu
redirect_from:
- /dev/release-dates
- /dev/release-dates/
- /dev/release-calendar
- /dev/release-calendar/
- /dev/docs/archive/1.1/dev/release_calendar
- /dev/docs/archive/1.1/dev/release_calendar/
title: Release Calendar
---

DuckDB follows [semantic versioning](https://semver.org/spec/v2.0.0.html).
Patch versions only ship bugfixes, while minor versions also introduce new features.

## Upcoming Releases

The planned dates of upcoming DuckDB releases are shown below.
**Please note that these dates are tentative** and DuckDB maintainers may decide to push back release dates to ensure the stability and quality of releases.


<!-- markdownlint-disable MD055 MD056 MD058 -->

{% if site.data.upcoming_releases.size > 0 %}
| Date | Version |
|:-----|--------:|
{%- for release in site.data.upcoming_releases reversed %}
| {{ release.start_date }} | {{ release.title }} |
{%- endfor %}
{% else %}
_There are no upcoming releases announced at the moment. Please check back later._
{% endif %}

<!-- markdownlint-enable MD055 MD056 MD058 -->

## Past Releases


In the following, we list DuckDB's past releases along with their codename where applicable.
Between versions 0.2.2 and 0.3.3, all releases (including patch versions) received a codename.
Since version 0.4.0, only major and minor versions get a codename.

<!-- markdownlint-disable MD055 MD056 MD058 -->

| Date | Version | Codename | Named after |      |
|:-----|--------:|----------|-------------|------|
{% for row in site.data.past_releases %}
    {%- capture logo_filename %}images/release-icons/{{ row.version_number }}.svg{% endcapture -%}
    {%- capture logo_exists %}{% file_exists {{ logo_filename }} %}{% endcapture -%}
    | {{ row.release_date }} | [{{ row.version_number }}](https://github.com/duckdb/duckdb/releases/tag/v{{ row.version_number }}) | {% if row.blog_post %}[{{ row.codename }}]({{ row.blog_post }}){% else %}{{ row.codename | default: "–" }}{% endif %} | {% if row.duck_wikipage %}<a href="{{ row.duck_wikipage }}">{% endif %}{{ row.duck_species_primary | default: "–" }}{% if row.duck_wikipage %}</a>{% endif %} {% if row.duck_species_secondary != nil %}_({{ row.duck_species_secondary }})_{% endif %} | {% if logo_exists == "true" %}![Logo of version {{ row.version_number }}](/{{ logo_filename }}){% endif %} |
{% endfor %}

<!-- markdownlint-enable MD055 MD056 MD058 -->

## Release Calendar as a CSV File

You can get a [CSV file containing past DuckDB releases](/data/duckdb-releases.csv) and analyze it using DuckDB's [CSV reader]({% link docs/archive/1.1/data/csv/overview.md %}).
This also [works in the online DuckDB shell](https://shell.duckdb.org/#queries=v0,SELECT-release_date%2C-version_number%2C-codename%2C-duck_species_primary%2C-duck_species_secondary%0AFROM-'https%3A%2F%2Fduckdb.org%2Fdata%2Fduckdb%20releases.csv'~).
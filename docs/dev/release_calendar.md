---
layout: docu
title: Release Calendar
redirect_from:
  - /dev/release-dates
  - /dev/release-dates/
  - /dev/release-calendar
  - /dev/release-calendar/
  - /dev/docs/dev/release_calendar
  - /dev/docs/dev/release_calendar/
---

DuckDB follows [semantic versioning](https://semver.org/spec/v2.0.0.html).
Patch versions only ship bugfixes, while minor versions also introduce new features.

## Upcoming Releases

The planned dates of upcoming DuckDB releases are shown below.
**Please note that these dates are tentative** and DuckDB maintainers may decide to push back release dates to ensure the stability and quality of releases.

<div class="narrow_table"></div>

<!-- markdownlint-disable MD055 MD056 -->

| Date | Version |
|:-----|--------:|
{%- for release in site.data.upcoming_releases reversed %}
| {{ release.start_date }} | {{ release.title | replace: "Release ", "" }} |
{%- endfor %}

<!-- markdownlint-enable MD055 MD056 -->

## Past Releases

<div class="narrow_table"></div>

In the following, we list DuckDB's past releases, including their codename (where applicable).
Prior to version 0.4.0, all releases, including patch versions, received a codename.
Since version 0.4.0, only major and minor versions get a codename.

<!-- markdownlint-disable MD055 MD056 -->

| Date | Version | Codename | Named after |      |
|:-----|--------:|----------|-------------|------|
{% for row in site.data.past_releases %}
    {%- capture logo_filename %}images/release-icons/{{ row.version_number }}.svg{% endcapture -%}
    {%- capture logo_exists %}{% file_exists {{ logo_filename }} %}{% endcapture -%}
    | {{ row.release_date }} | [{{ row.version_number }}](https://github.com/duckdb/duckdb/releases/tag/v{{ row.version_number }}) | {% if row.blog_post %}[{{ row.codename }}]({{ row.blog_post }}){% else %}{{ row.codename | default: "–" }}{% endif %} | {% if row.duck_wikipage %}<a href="{{ row.duck_wikipage }}">{% endif %}{{ row.duck_species_primary | default: "–" }}{% if row.duck_wikipage %}</a>{% endif %} {% if row.duck_species_secondary != nil %}_({{ row.duck_species_secondary }})_{% endif %} | {% if logo_exists == "true" %}![Logo of version {{ row.version_number }}](/{{ logo_filename }}){% endif %} |
{% endfor %}

<!-- markdownlint-enable MD055 MD056 -->

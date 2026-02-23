---
layout: default
redirect_from:
- /cal
- /release-calendar
- /dev/release-dates
- /dev/release-calendar
- /docs/dev/release_calendar
- /docs/stable/dev/release_calendar
- /docs/preview/dev/release_calendar
title: Release Calendar
body_class: release-calendar blog_typography post
max_page_width: medium
toc: false
---

<div class="wrap pagetitle">
  <h1>Release Calendar</h1>
</div>

DuckDB follows [semantic versioning](https://semver.org/spec/v2.0.0.html).
Larger new features are introduced in minor versions,
while patch versions mostly contain bugfixes.

## Upcoming Releases

The planned dates of upcoming DuckDB releases are shown below.
**Please note that these dates are tentative** and DuckDB maintainers may decide to push back release dates to ensure the stability and quality of releases.

<!-- markdownlint-disable MD055 MD056 MD058 -->

{% if site.data.upcoming_releases.size > 0 %}
| Date | Version |
|:-----|--------:|
{%- for release in site.data.upcoming_releases %}
| {{ release.start_date }} | {{ release.title }} |
{%- endfor %}
{% else %}
_There are no upcoming releases announced at the moment. Please check back later._
{% endif %}

<!-- markdownlint-enable MD055 MD056 MD058 -->

For planned new features, see the [DuckDB Development Roadmap]({% link roadmap.md %}).

### LTS Releases

Starting with v1.4.0, every _other_ DuckDB version is going to be a Long-Term Support (LTS) edition.
For LTS DuckDB versions, the support period for [community support](https://duckdblabs.com/community_support_policy/) is currently a year after the release.
[DuckDB Labs](https://duckdblabs.com/) is offering support for older LTS versions after their community support has expired.

<img src="/images/blog/lts-support-light.svg" alt="DuckDB LTS support" width="900" class="lightmode-img">
<img src="/images/blog/lts-support-dark.svg" alt="DuckDB LTS support" width="900" class="darkmode-img">

For an overview of end-of-life information, see the [DuckDB entry on `endoflife.date`](https://endoflife.date/duckdb).

There is no set date yet for the release of DuckDB v1.4.5. We will select the date as necessitated by the issues filed for the DuckDB v1.4.x line. For exampe, if we encounter a critical issue or vulnerability, we will expedite the release of v1.4.5.

## Past Releases

In the following, we list DuckDB's past releases along with their codename where applicable.
Between versions 0.2.2 and 0.3.3, all releases (including patch versions) received a codename.
Since version 0.4.0, only major and minor versions get a codename.

<!-- markdownlint-disable MD034 MD055 MD056 MD058 -->

|      | Date | Version | Codename | Named after | End of life      |
|------|:-----|--------:|----------|-------------|------------------|
{% for row in site.data.past_releases %}
  {%- capture logo_filename %}images/release-icons/{{ row.version_number }}.svg{% endcapture -%}
  {%- capture logo_exists %}{% file_exists {{ logo_filename }} %}{% endcapture -%}
  | {% if logo_exists == "true" %}![Logo of version {{ row.version_number }}](/{{ logo_filename }}){% endif %} | {{ row.release_date }} | [{{ row.version_number }}{% if row.lts == "true" %} LTS{% endif %}](https://github.com/duckdb/duckdb/releases/tag/v{{ row.version_number }}) | {% if row.blog_post %}[{{ row.codename }}]({{ row.blog_post }}){% else %}{{ row.codename | default: "–" }}{% endif %} | {% if row.duck_wikipage %}<a href="{{ row.duck_wikipage }}">{% endif %}{{ row.duck_species_primary | default: "–" }}{% if row.duck_wikipage %}</a>{% endif %} {% if row.duck_species_secondary != nil %}_({{ row.duck_species_secondary }})_{% endif %} | {% if row.end_of_life %}{{ row.end_of_life }}{% endif %} |
{% endfor %}

<!-- markdownlint-enable MD034 MD055 MD056 MD058 -->

## Release Calendar as a CSV File

You can get a [CSV file containing past DuckDB releases](/data/duckdb-releases.csv) and analyze it using DuckDB's [CSV reader]({% link docs/stable/data/csv/overview.md %}).
For example, you can compute the average number of days between releases using the [`lag` window function]({% link docs/stable/sql/functions/window_functions.md %}#lagexpr-offset-default-order-by-ordering-ignore-nulls):

```sql
SELECT avg(diff)::DECIMAL(8, 2) AS average_days_between_releases
FROM (
    SELECT release_date - lag(release_date) OVER (ORDER BY release_date) AS diff
    FROM 'https://duckdb.org/data/duckdb-releases.csv'
);
```

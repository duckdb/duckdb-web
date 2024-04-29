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
The first major version, v1.0, is expected to be released in summer 2024.

## Upcoming Releases

The planned dates of upcoming DuckDB releases are shown below.
**Please note that these dates are tentative** and DuckDB maintainers may decide to push back release dates to ensure the stability and quality of releases.

<div class="narrow_table"></div>
<table>
  <thead>
    <tr>
      <th>Date</th>
      <th>Version</th>
    </tr>
  </thead>
  <tbody>
    {% for release in site.data.upcoming_releases reversed %}
    <tr>
      <td>{{ release.start_date }}</td>
      <td style="text-align: right">{{ release.title | replace: "Release ", "" }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

## Past Releases

<div class="narrow_table"></div>

In the following, we list DuckDB's past releases, including their codename (where applicable).
Prior to version 0.4.0, all releases, including patch versions, received a codename.
Since version 0.4.0, only major and minor versions get a codename.

| Date | Version | Codename | Named after |
|:--|--:|--|--|
| 2024-04-17 | [0.10.2](https://github.com/duckdb/duckdb/releases/tag/v0.10.2) | – | – |
| 2024-03-18 | [0.10.1](https://github.com/duckdb/duckdb/releases/tag/v0.10.1) | – | – |
| 2024-02-13 | [0.10.0](https://github.com/duckdb/duckdb/releases/tag/v0.10.0) | Fusca | [Velvet scoter _(Melanitta fusca)_](https://en.wikipedia.org/wiki/Velvet_scoter) |
| 2023-11-14 | [0.9.2](https://github.com/duckdb/duckdb/releases/tag/v0.9.2)   | – | – |
| 2023-10-11 | [0.9.1](https://github.com/duckdb/duckdb/releases/tag/v0.9.1)   | – | – |
| 2023-09-26 | [0.9.0](https://github.com/duckdb/duckdb/releases/tag/v0.9.0)   | Undulata | [Yellow-billed duck _(Anas undulata)_](https://en.wikipedia.org/wiki/Yellow-billed_duck) |
| 2023-06-13 | [0.8.1](https://github.com/duckdb/duckdb/releases/tag/v0.8.1)   | – | – |
| 2023-05-17 | [0.8.0](https://github.com/duckdb/duckdb/releases/tag/v0.8.0)   | Fulvigula | [Mottled duck _(Anas fulvigula)_](https://en.wikipedia.org/wiki/Mottled_duck) |
| 2023-02-27 | [0.7.1](https://github.com/duckdb/duckdb/releases/tag/v0.7.1)   | – | – |
| 2023-02-13 | [0.7.0](https://github.com/duckdb/duckdb/releases/tag/v0.7.0)   | Labradorius | [Labrador duck _(Camptorhynchus labradorius)_](https://en.wikipedia.org/wiki/Labrador_duck) |
| 2022-12-06 | [0.6.1](https://github.com/duckdb/duckdb/releases/tag/v0.6.1)   | – | – |
| 2022-11-14 | [0.6.0](https://github.com/duckdb/duckdb/releases/tag/v0.6.0)   | Oxyura | [White-headed duck _(Oxyura leucocephala)_](https://en.wikipedia.org/wiki/White-headed_duck) |
| 2022-09-19 | [0.5.1](https://github.com/duckdb/duckdb/releases/tag/v0.5.1)   | – | – |
| 2022-09-05 | [0.5.0](https://github.com/duckdb/duckdb/releases/tag/v0.5.0)   | Pulchellus | [Green pygmy goose _(Nettapus pulchellus)_](https://en.wikipedia.org/wiki/Green_pygmy_goose) |
| 2022-06-20 | [0.4.0](https://github.com/duckdb/duckdb/releases/tag/v0.4.0)   | Ferruginea | [Andean duck _(Oxyura ferruginea)_](https://en.wikipedia.org/wiki/Andean_duck) |
| 2022-04-11 | [0.3.3](https://github.com/duckdb/duckdb/releases/tag/v0.3.3)   | Sansaniensis | [_Chenoanas sansaniensis_](https://species.wikimedia.org/wiki/Chenoanas_sansaniensis) |
| 2022-02-07 | [0.3.2](https://github.com/duckdb/duckdb/releases/tag/v0.3.2)   | Gibberifrons | [Sunda teal _(Anas gibberifrons)_](https://en.wikipedia.org/wiki/Sunda_teal) |
| 2021-11-16 | [0.3.1](https://github.com/duckdb/duckdb/releases/tag/v0.3.1)   | Spectabilis | [King eider _(Somateria spectabilis)_](https://en.wikipedia.org/wiki/King_eider)  |
| 2021-10-06 | [0.3.0](https://github.com/duckdb/duckdb/releases/tag/v0.3.0)   | Gracilis | [Grey teal _(Anas gracilis)_](https://en.wikipedia.org/wiki/Grey_teal) |
| 2021-09-06 | [0.2.9](https://github.com/duckdb/duckdb/releases/tag/v0.2.9)   | Platyrhynchos | [Mallard _(Anas platyrhynchos)_](https://en.wikipedia.org/wiki/Mallard) |
| 2021-08-02 | [0.2.8](https://github.com/duckdb/duckdb/releases/tag/v0.2.8)   | Ceruttii | [_Histrionicus ceruttii_](https://en.wikipedia.org/wiki/Harlequin_duck#Taxonomy) |
| 2021-06-14 | [0.2.7](https://github.com/duckdb/duckdb/releases/tag/v0.2.7)   | Mollissima | [Common eider _(Somateria mollissima)_](https://en.wikipedia.org/wiki/Common_eider) |
| 2021-05-08 | [0.2.6](https://github.com/duckdb/duckdb/releases/tag/v0.2.6)   | Jamaicensis | [Blue-billed ruddy duck _(Oxyura jamaicensis)_](https://en.wikipedia.org/wiki/Ruddy_duck) |
| 2021-03-10 | [0.2.5](https://github.com/duckdb/duckdb/releases/tag/v0.2.5)   | Falcata | [Falcated duck _(Mareca falcata)_](https://en.wikipedia.org/wiki/Falcated_duck) |
| 2021-02-02 | [0.2.4](https://github.com/duckdb/duckdb/releases/tag/v0.2.4)   | Jubata | [Australian wood duck _(Chenonetta jubata)_](https://en.wikipedia.org/wiki/Australian_wood_duck) |
| 2020-12-03 | [0.2.3](https://github.com/duckdb/duckdb/releases/tag/v0.2.3)   | Serrator | [Red-breasted merganser _(Mergus serrator)_](https://en.wikipedia.org/wiki/Red-breasted_merganser) |
| 2020-11-01 | [0.2.2](https://github.com/duckdb/duckdb/releases/tag/v0.2.2)   | Clypeata | [Northern shoveler _(Spatula clypeata)_](https://en.wikipedia.org/wiki/Northern_shoveler) |
| 2020-08-29 | [0.2.1](https://github.com/duckdb/duckdb/releases/tag/v0.2.1)   | – | – |
| 2020-07-23 | [0.2.0](https://github.com/duckdb/duckdb/releases/tag/v0.2.0)   | – | – |
| 2020-06-19 | [0.1.9](https://github.com/duckdb/duckdb/releases/tag/v0.1.9)   | – | – |
| 2020-05-29 | [0.1.8](https://github.com/duckdb/duckdb/releases/tag/v0.1.8)   | – | – |
| 2020-05-04 | [0.1.7](https://github.com/duckdb/duckdb/releases/tag/v0.1.7)   | – | – |
| 2020-04-05 | [0.1.6](https://github.com/duckdb/duckdb/releases/tag/v0.1.6)   | – | – |
| 2020-03-02 | [0.1.5](https://github.com/duckdb/duckdb/releases/tag/v0.1.5)   | – | – |
| 2020-02-03 | [0.1.3](https://github.com/duckdb/duckdb/releases/tag/v0.1.3)   | – | – |
| 2020-01-06 | [0.1.2](https://github.com/duckdb/duckdb/releases/tag/v0.1.2)   | – | – |
| 2019-09-24 | [0.1.1](https://github.com/duckdb/duckdb/releases/tag/v0.1.1)   | – | – |
| 2019-06-27 | [0.1.0](https://github.com/duckdb/duckdb/releases/tag/v0.1.0)   | – | – |

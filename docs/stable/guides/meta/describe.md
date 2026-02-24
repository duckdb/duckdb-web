---
layout: docu
redirect_from:
- /docs/guides/meta/describe
title: Describe
---

## Describing a Table

To view the schema of a table, use the `DESCRIBE` statement (or its aliases `DESC` and `SHOW`) followed by the table name.

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j VARCHAR);
DESCRIBE tbl;
SHOW tbl; -- equivalent to DESCRIBE tbl;
```

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | NO   | PRI  | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

## Describing a Query

To view the schema of the result of a query, prepend `DESCRIBE` to a query.

```sql
DESCRIBE SELECT * FROM tbl;
```

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | YES  | NULL | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

Note that there are subtle differences: compared to the result when [describing a table](#describing-a-table), nullability (`null`) and key information (`key`) are lost.

## Using `DESCRIBE` in a Subquery

`DESCRIBE` can be used as a subquery. This allows creating a table from the description, for example:

```sql
CREATE TABLE tbl_description AS SELECT * FROM (DESCRIBE tbl);
```

## Describing Remote Tables

It is possible to describe remote tables via the [`httpfs` extension]({% link docs/stable/core_extensions/httpfs/overview.md %}) using the `DESCRIBE TABLE` statement. For example:

```sql
DESCRIBE TABLE 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv';
```

|               column_name               | column_type | null | key  | default | extra |
|-----------------------------------------|-------------|------|------|---------|-------|
| season_num                              | BIGINT      | YES  | NULL | NULL    | NULL  |
| episode_num                             | BIGINT      | YES  | NULL | NULL    | NULL  |
| aired_date                              | DATE        | YES  | NULL | NULL    | NULL  |
| cnt_kirk_hookups                        | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_downed_redshirts                    | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_aliens_almost_took_over_planet     | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_aliens_almost_took_over_enterprise | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_vulcan_nerve_pinch                  | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_warp_speed_orders                   | BIGINT      | YES  | NULL | NULL    | NULL  |
| highest_warp_speed_issued               | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_hand_phasers_fired                 | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_ship_phasers_fired                 | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_ship_photon_torpedos_fired         | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_transporter_pax                     | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_damn_it_jim_quote                   | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_im_givin_her_all_shes_got_quote     | BIGINT      | YES  | NULL | NULL    | NULL  |
| cnt_highly_illogical_quote              | BIGINT      | YES  | NULL | NULL    | NULL  |
| bool_enterprise_saved_the_day           | BIGINT      | YES  | NULL | NULL    | NULL  |

---
github_directory: https://github.com/duckdb/duckdb/tree/main/extension/inet
layout: docu
title: inet Extension
---

The `inet` extension defines the `INET` data type for storing [IPv4](https://en.wikipedia.org/wiki/Internet_Protocol_version_4) and [IPv6](https://en.wikipedia.org/wiki/IPv6) Internet addresses. It supports the [CIDR notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation) for subnet masks (e.g., `198.51.100.0/22`, `2001:db8:3c4d::/48`).

## Installing and Loading

The `inet` extension will typically automatically load on first use, but to explicitly install and load the extension, run:

```sql
INSTALL inet;
LOAD inet;
```

## Examples

```sql
SELECT '127.0.0.1'::INET AS ipv4, '2001:db8:3c4d::/48'::INET AS ipv6;
```

|   ipv4    |        ipv6        |
|-----------|--------------------|
| 127.0.0.1 | 2001:db8:3c4d::/48 |

```sql
CREATE TABLE tbl (id INTEGER, ip INET);
INSERT INTO tbl VALUES
    (1, '192.168.0.0/16'),
    (2, '127.0.0.1'),
    (3, '8.8.8.8'),
    (4, 'fe80::/10'),
    (5, '2001:db8:3c4d:15::1a2f:1a2b');
SELECT * FROM tbl;
```

| id |             ip              |
|---:|-----------------------------|
| 1  | 192.168.0.0/16              |
| 2  | 127.0.0.1                   |
| 3  | 8.8.8.8                     |
| 4  | fe80::/10                   |
| 5  | 2001:db8:3c4d:15::1a2f:1a2b |

## Operations on `INET` Values

`INET` values can be compared naturally, and IPv4 will sort before IPv6. Additionally, IP addresses can be modified by adding or subtracting integers.

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('127.0.0.1'::INET + 10),
    ('fe80::10'::INET - 9),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b');
SELECT cidr FROM tbl ORDER BY cidr ASC;
```

|            cidr             |
|-----------------------------|
| 127.0.0.1                   |
| 127.0.0.11                  |
| 2001:db8:3c4d:15::1a2f:1a2b |
| fe80::7                     |

## `host` Function

The host component of an `INET` value can be extracted using the `HOST()` function.

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.0.0/16'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, host(cidr) FROM tbl;
```

|              cidr              |         host(cidr)          |
|--------------------------------|-----------------------------|
| 192.168.0.0/16                 | 192.168.0.0                 |
| 127.0.0.1                      | 127.0.0.1                   |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | 2001:db8:3c4d:15::1a2f:1a2b |
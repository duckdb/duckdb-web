---
layout: docu
title: inet Extension
github_repository: https://github.com/duckdb/duckdb-inet
---

The `inet` extension defines the `INET` data type for storing [IPv4](https://en.wikipedia.org/wiki/Internet_Protocol_version_4) and [IPv6](https://en.wikipedia.org/wiki/IPv6) Internet addresses. It supports the [CIDR notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation) for subnet masks (e.g., `198.51.100.0/22`, `2001:db8:3c4d::/48`).

## Installing and Loading

The `inet` extension will be transparently [autoloaded]({% link docs/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

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


## `netmask` Function

Computes the network mask for the address's network.

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.5/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, netmask(cidr) FROM tbl;
```

|              cidr              |              netmask(cidr)         |
|--------------------------------|------------------------------------|
| 192.168.1.5/24                 | 255.255.255.0/24                   |
| 127.0.0.1                      | 255.255.255.255                    |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | ffff:ffff:ffff:ffff:ffff:ffff::/96 |

## `network` Function

Returns the network part of the address, zeroing out whatever is to the right of the netmask.

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.5/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, network(cidr) FROM tbl;
```

|              cidr              |              network(cidr)         |
|--------------------------------|------------------------------------|
| 192.168.1.5/24                 | 192.168.1.0/24                     |
| 127.0.0.1                      | 255.255.255.255                    |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | ffff:ffff:ffff:ffff:ffff:ffff::/96 |

## `broadcast` Function

Computes the broadcast address for the address's network.

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.5/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, broadcast(cidr) FROM tbl;
```

|              cidr              |            broadcast(cidr)         |
|--------------------------------|------------------------------------|
| 192.168.1.5/24                 | 192.168.1.0/24                     |
| 127.0.0.1                      | 127.0.0.1                          |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | 2001:db8:3c4d:15::/96              |

## `<<=` Predicate 

Is subnet contained by or equal to subnet?

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.0/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, INET '192.168.1.5/32' <<= cidr FROM tbl;
```

|              cidr              | (CAST('192.168.1.5/32' AS INET) <<= cidr)   |
|--------------------------------|---------------------------------------------|
| 192.168.1.5/24                 | true                                        |
| 127.0.0.1                      | false                                       |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | false                                       |

## `>>=` Predicate 

Does subnet contain or equal subnet?

```sql
CREATE TABLE tbl (cidr INET);
INSERT INTO tbl VALUES
    ('192.168.1.0/24'),
    ('127.0.0.1'),
    ('2001:db8:3c4d:15::1a2f:1a2b/96');
SELECT cidr, INET '192.168.0.0/16' >>= cidr FROM tbl;
```

|              cidr              | (CAST('192.168.0.0/16' AS INET) >>= cidr)   |
|--------------------------------|---------------------------------------------|
| 192.168.1.5/24                 | true                                        |
| 127.0.0.1                      | false                                       |
| 2001:db8:3c4d:15::1a2f:1a2b/96 | false                                       |

## HTML Escape and Unescape Functions

```sql
SELECT html_escape('&');
```

```text
┌──────────────────┐
│ html_escape('&') │
│     varchar      │
├──────────────────┤
│ &amp;            │
└──────────────────┘
```

```sql
SELECT html_unescape('&amp;');
```

```text
┌────────────────────────┐
│ html_unescape('&amp;') │
│        varchar         │
├────────────────────────┤
│ &                      │
└────────────────────────┘
```

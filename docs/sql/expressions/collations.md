---
layout: docu
title: Collations
selected: Documentation/Expressions/Collations
expanded: Expressions
railroad: expressions/collate.js
---
<div id="rrdiagram"></div>

Collations provide rules for how text should be sorted or compared in the execution engine. Collations are useful for localization, as the rules for how text should be ordered are different for different languages or for different countries. These orderings are often incompatible with one another. For example, in English the letter "y" comes between "x" and "z". However, in Lithuanian the letter "y" comes between the "i" and "j". For that reason, different collations are supported. The user must choose which collation they want to use when performing sorting and comparison operations.

By default, the `BINARY` collation is used. That means that strings are ordered and compared based only on their binary contents. This makes sense for standard ASCII characters (i.e. the letters A-Z and numbers 0-9), but generally does not make much sense for special unicode characters. It is, however, by far the fastest method of performing ordering and comparisons. Hence it is recommended to stick with the `BINARY` collation unless required otherwise.

### Using Collations
In the stand-alone installation of DuckDB three collations are included: `NOCASE`, `NOACCENT` and `NFC`. The `NOCASE` collation compares characters as equal regardless of their casing. The `NOACCENT` collation compares characters as equal regardless of their accents. The `NFC` collation performs NFC-normalized comparisons, see [here](https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization) for more information.

```sql
SELECT 'hello'='hElLO';
-- false
SELECT 'hello' COLLATE NOCASE='hElLO';
-- true

SELECT 'hello' = 'hëllo';
-- false
SELECT 'hello' COLLATE NOACCENT = 'hëllo';
-- true
```

Collations can be combined by chaining them using the dot operator. Note, however, that not all collations can be combined together. In general, the `NOCASE` collation can be combined with any other collator, but most other collations cannot be combined.

```sql
SELECT 'hello' COLLATE NOCASE='hElLÖ';
-- false
SELECT 'hello' COLLATE NOACCENT='hElLÖ';
-- false
SELECT 'hello' COLLATE NOCASE.NOACCENT='hElLÖ';
-- true
```

### Default Collations
The collations we have seen so far have all been specified *per expression*. It is also possible to specify a default collator, either on the global database level or on a base table column. The `PRAGMA` `default_collation` can be used to specify the global default collator. This is the collator that will be used if no other one is specified.

```sql
PRAGMA default_collation=NOCASE;

SELECT 'hello'='HeLlo';
-- true
```

Collations can also be specified per-column when creating a table. When that column is then used in a comparison, the per-column collation is used to perform that comparison.

```sql
CREATE TABLE names(name VARCHAR COLLATE NOACCENT);
INSERT INTO names VALUES ('hännes');
SELECT name FROM names WHERE name='hannes';
-- hännes
```

Be careful here, however, as different collations cannot be combined. This can be problematic when you want to compare columns that have a different collation specified.

```sql
SELECT name FROM names WHERE name='hannes' COLLATE NOCASE;
-- ERROR: Cannot combine types with different collation!

CREATE TABLE other_names(name VARCHAR COLLATE NOCASE);
INSERT INTO other_names VALUES ('HÄNNES');

SELECT * FROM names, other_names WHERE names.name=other_names.name;
-- ERROR: Cannot combine types with different collation!

-- need to manually overwrite the collation!

SELECT * FROM names, other_names WHERE names.name COLLATE NOACCENT.NOCASE=other_names.name COLLATE NOACCENT.NOCASE;
-- hännes|HÄNNES
```

### ICU Collations
The collations we have seen so far are not region dependent, and do not follow any specific regional rules. If you wish to follow the rules of a specific region or language, you will need to use one of the ICU collations. For that, you need to include the ICU extension. This can be found in the `extension/icu` folder in the project. Using the C++ API, the extension can be loaded as follows:

```cpp
DuckDB db;
db.LoadExtension<ICUExtension>();
```

Loading this extension will add a number of language and region specific collations to your database. These can be queried using `PRAGMA collations` command, or by querying the `pragma_collations` function.

```sql
PRAGMA collations;
SELECT * FROM pragma_collations();
-- [af, am, ar, as, az, be, bg, bn, bo, bs, bs, ca, ceb, chr, cs, cy, da, de, de_AT, dsb, dz, ee, el, en, en_US, en_US, eo, es, et, fa, fa_AF, fi, fil, fo, fr, fr_CA, ga, gl, gu, ha, haw, he, he_IL, hi, hr, hsb, hu, hy, id, id_ID, ig, is, it, ja, ka, kk, kl, km, kn, ko, kok, ku, ky, lb, lkt, ln, lo, lt, lv, mk, ml, mn, mr, ms, mt, my, nb, nb_NO, ne, nl, nn, om, or, pa, pa, pa_IN, pl, ps, pt, ro, ru, se, si, sk, sl, smn, sq, sr, sr, sr_BA, sr_ME, sr_RS, sr, sr_BA, sr_RS, sv, sw, ta, te, th, tk, to, tr, ug, uk, ur, uz, vi, wae, wo, xh, yi, yo, zh, zh, zh_CN, zh_SG, zh, zh_HK, zh_MO, zh_TW, zu]
```

These collations can then be used as the other collations would be used before. They can also be combined with the `NOCASE` collation. For example, to use the German collation rules you could use the following code snippet:

```sql
CREATE TABLE strings(s VARCHAR COLLATE DE);
INSERT INTO strings VALUES ('Gabel'), ('Göbel'), ('Goethe'), ('Goldmann'), ('Göthe'), ('Götz');
SELECT * FROM strings ORDER BY s;
-- "Gabel", "Göbel", "Goethe", "Goldmann", "Göthe", "Götz"
```

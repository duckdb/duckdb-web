---
layout: post
title:  "Announcing DuckDB 1.0.0"
author: Mark Raasveldt and Hannes Mühleisen
thumb: "/images/blog/thumbs/240603.svg"
excerpt: "The DuckDB team is <i>very happy</i> to announce that today we’re releasing DuckDB version 1.0.0, codename “Snow Duck” (anas nivis)."
---

To install the new version, please visit the [installation guide](/docs/installation).
For the release notes, see the [release page](https://github.com/duckdb/duckdb/releases/tag/v1.0.0).

<img src="/images/blog/paddling-of-ducks.svg"
     alt="Logos of DuckDB releases"
     width="800px"
     />

It has been almost six years since the first source code was written for the project back in 2018, and a _lot_ has happened since: There are now over 300&nbsp;000 lines of C++ engine code, over 42&nbsp;000 commits and almost 4&nbsp;000 issues were opened and closed again. DuckDB has also gained significant popularity: the project has attracted tens of thousands of stars and followers on GitHub and social media platforms. Download counts are in the millions each month, and download traffic just for extensions is upwards of four terabytes _each day_. There are even [books](https://www.manning.com/books/duckdb-in-action) [being](https://www.amazon.com/Getting-Started-DuckDB-practical-efficiently/dp/1803241004) [written](https://www.oreilly.com/library/view/duckdb-up-and/9781098159689/) about DuckDB, and – most importantly – now even [Wikipedia considers DuckDB notable](https://en.wikipedia.org/wiki/DuckDB), albeit barely.

## Why now?

Of course, version numbers are somewhat arbitrary and “feely”, despite [attempts](https://semver.org/spec/v2.0.0.html) at making them more mechanical. We could have released DuckDB 1.0.0 back in 2018, or we could have waited ten more years. There is never a great moment, because software (with the exception of [TeX](https://x.com/fermatslibrary/status/1740324503308169507)) is never “done”. Why choose today?

Data management systems – even purely analytical ones – are such core components of any application that there is always an implicit contract of trust between their developers and users. Users rely on databases to provide correct query results and to not lose their data. At the same time, system developers need to be aware of their responsibility of not breaking people’s applications willy-nilly. Intuitively, version 1.0.0 means something else for a data management system than it means for an egg timer app (no offense). From the very beginning, we were committed to making DuckDB a reliable base for people to build their applications on. This is also why the 1.0.0 release is named after the non-existent _snow duck (anas nivis),_ harking back to Apple’s [Snow Leopard](https://arstechnica.com/gadgets/2009/08/mac-os-x-10-6/) release some years ago.

For us, one of the major blockers to releasing 1.0.0 was the storage format. DuckDB has its own custom-built data storage format. This format allows users to manage many (possibly very large) tables in a single file with full transactional semantics and state-of-the-art compression. Of course, designing a new file format is not without its challenges, and we had to make significant changes to the format over time. This led to the suboptimal situation that whenever a new DuckDB version was released, the files created with the old version did not work with the new DuckDB version and had to be manually upgraded. This problem was addressed in v0.10.0 back in February – where we introduced [backward compatibility and limited forward compatibility for DuckDB’s storage format](https://duckdb.org/2024/02/13/announcing-duckdb-0100#backward-compatibility). This feature has now been used in the wild for a while without serious issues – providing us with the confidence to offer a guarantee that DuckDB files created with DuckDB 1.0.0 will be compatible with future DuckDB versions.

## Stability

The core theme of the 1.0.0 release is stability. This contrasts it with previous releases where we have had blog posts talk about long lists of new features. Instead, the 1.0.0 release has very limited new features (a [few](https://github.com/duckdb/duckdb/pull/11677) [might](https://github.com/duckdb/duckdb/pull/11918) [have](https://github.com/duckdb/duckdb/pull/11831) [snuck](https://github.com/duckdb/duckdb/pull/11835) in). Instead, our focus has been on stability.

We’ve observed the frankly staggering growth in the amount and breadth of use of DuckDB in the wild, and have not seen an increase in serious issues being reported. Meanwhile, there are thousands of test cases with millions of test queries being run every night. We run loads of microbenchmarks and standardized benchmark suites to spot performance regressions. DuckDB is constantly being tortured by various fuzzers that construct all manners of wild SQL queries to make sure we don’t miss weird corner cases. All told, this has built the necessary confidence in us to release a 1.0.0.

Another core aspect of stability with the 1.0.0 release is stability across versions. While [never breaking anyone's workflow is likely impossible](https://xkcd.com/1172/), we plan to be much more careful with user-facing changes going forward. In particular, we plan to focus on providing stability for the SQL dialect, as well as the C API. While we do not guarantee that we will never change semantics in these layers in the future – we will try to provide ample warning when doing so, as well as providing workarounds that allow previously working code to keep on working.

## Looking ahead

Unlike many open-source projects, DuckDB also has a healthy long-term funding strategy. [DuckDB Labs](https://duckdblabs.com/), the company that employs DuckDB’s core contributors, has not had any outside investments, and as a result, the company is fully owned by the team. Labs’ business model is to provide consulting and support services for DuckDB, and we’re happy to report that this is going well. With the revenue from contracts, we fund long-term and strategic DuckDB development with a team of almost 20 people. At the same time, the intellectual property in the project is guarded by the independent [DuckDB Foundation](https://duckdb.org/foundation/). This non-profit foundation ensures that DuckDB will be around long-term under the MIT license.

Regarding long-term plans, there are, of course, many things on the roadmap still. One thing we’re very excited about is the ability to expand the extension environment around DuckDB. Extensions are plug-ins that can add new SQL-level functions, file formats, optimizers, etc. while keeping the DuckDB core mean and lean. There are already an impressive number of third-party extensions to DuckDB, and we’re working hard to streamline the process of building and distributing community-contributed extensions. We think DuckDB can become the basis for the next revolution in data through community extensions connected by a high-performance data fabric accessible through a unified SQL interface.

Of course, there will be issues found in today’s release. But rest assured, there will be a 1.0.1 release. There will be a 1.1.0. And there might also be a 2.0.0 at some point. We’re in this for the long run, all of us, together. We have the team and the structures and resources to do so.

## Acknowledgements

First of all, we are very, very grateful to you all. Our massive and heartfelt thanks go to everyone who has contributed code, filed issues or engaged in discussions, promoted DuckDB in their environment, and, of course, all DuckDB users. We could not have done it without you!

We would also like to thank the [CWI Database Architectures group](https://www.cwi.nl/en/groups/database-architectures/) for providing us with the environment and expertise to build DuckDB, the organizations that provided us with research grants early on, the excellent [customers of DuckDB Labs](https://duckdblabs.com/#customers) that make it all work (especially the early ones), and the generous donors to the [DuckDB Foundation](https://duckdb.org/foundation/). We are particularly grateful to our long-standing Gold sponsors [MotherDuck](https://motherduck.com/), [Voltron Data](https://voltrondata.com/) and [Posit](https://posit.co/).

Finally, we would like to thank the [excellent and amazing team at DuckDB Labs](https://duckdblabs.com/#about).

So join us now in being nostalgic, teary-eyed and excited for what’s to come for DuckDB and celebrate the release of DuckDB 1.0.0 with us. We certainly will.

Mark and Hannes

PS: We are holding our next community event, [DuckCon #5](https://duckdb.org/2024/08/15/duckcon5), in Seattle on August 15, only a few short weeks from today. Attendance is free. Hope to see you there!

_For press inquiries, please reach out to [Gabor Szarnyas](mailto:gabor@duckdblabs.com)._

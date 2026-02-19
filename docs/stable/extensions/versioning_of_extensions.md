---
layout: docu
redirect_from:
- /docs/extensions/versioning_of_extensions
title: Versioning of Extensions
---

## Extension Versioning

Most software has some sort of version number. Version numbers serve a few important goals:

* Tie a binary to a specific state of the source code
* Allow determining the expected feature set
* Allow determining the state of the APIs
* Allow efficient processing of bug reports (e.g., bug `#1337` was introduced in version `v3.4.5` )
* Allow determining chronological order of releases (e.g., version `v1.2.3` is older than `v1.2.4`)
* Give an indication of expected stability (e.g., `v0.0.1` is likely not very stable, whereas `v13.11.0` probably is stable)

Just like [DuckDB itself]({% link release_calendar.md %}), DuckDB extensions have their own version number. To ensure consistent semantics
of these version numbers across the various extensions, DuckDB's [Core Extensions]({% link docs/stable/core_extensions/overview.md %}) use
a versioning scheme that prescribes how extensions should be versioned. The versioning scheme for Core Extensions is made up of 3 different stability levels: **unstable**, **pre-release**, and **stable**.
Let's go over each of the 3 levels and describe their format:

### Unstable Extensions

Unstable extensions are extensions that can't (or don't want to) give any guarantees regarding their current stability,
or their goals of becoming stable. Unstable extensions are tagged with the **short git hash** of the extension.

For example, at the time of writing this, the version of the `vss` extension is an unstable extension of version `690bfc5`.

What to expect from an extension that has a version number in the **unstable** format?

* The state of the source code of the extension can be found by looking up the hash in the extension repository
* Functionality may change or be removed completely with every release
* This extension's API could change with every release
* This extension may not follow a structured release cycle, new (breaking) versions can be pushed at any time

### Pre-Release Extensions

Pre-release extensions are the next step up from Unstable extensions. They are tagged with version in the **[SemVer](https://semver.org/)** format, more specifically, those in the `v0.y.z` format.
In semantic versioning, versions starting with `v0` have a special meaning: they indicate that the more strict semantics of regular (`>v1.0.0`) versions do not yet apply. It basically means that an extension is working
towards becoming a stable extension, but is not quite there yet.

For example, at the time of writing this, the version of the `delta` extension is a pre-release extension of version `v0.1.0`.

What to expect from an extension that has a version number in the **pre-release** format?

* The extension is compiled from the source code corresponding to the tag.
* Semantic Versioning semantics apply. See the [Semantic Versioning](https://semver.org/) specification for details.
* The extension follows a release cycle where new features are tested in nightly builds before being grouped into a release and pushed to the `core` repository.
* Release notes describing what has been added each release should be available to make it easy to understand the difference between versions.

### Stable Extensions

Stable extensions are the final step of extension stability. This is denoted by using a **stable SemVer** of format `vx.y.z` where `x>0`.

For example, at the time of writing this, the version of the `parquet` extension is a stable extension of version `v1.0.0`.

What to expect from an extension that has a version number in the **stable** format? Essentially the same as pre-release extensions, but now the more
strict SemVer semantics apply: the API of the extension should now be stable and will only change in backwards incompatible ways when the major version is bumped.
See the SemVer specification for details

## Release Cycle of Pre-Release and Stable Core Extensions

In general for extensions the release cycle depends on their stability level. **unstable** extensions are often in
sync with DuckDB's release cycle, but may also be quietly updated between DuckDB releases. **pre-release** and **stable**
extensions follow their own release cycle. These may or may not coincide with DuckDB releases. To find out more about the release cycle of a specific
extension, refer to the documentation or GitHub page of the respective extension. Generally, **pre-release** and **stable** extensions will document
their releases as GitHub releases, an example of which you can see in the [`delta` extension](https://github.com/duckdb/duckdb-delta/releases).

Finally, there is a small exception: All [in-tree]({% link docs/stable/extensions/advanced_installation_methods.md %}#in-tree-vs-out-of-tree) extensions simply
follow DuckDB's release cycle.

## Nightly Builds

Just like DuckDB itself, DuckDB's core extensions have nightly or dev builds that can be used to try out features before they are officially released.
This can be useful when your workflow depends on a new feature, or when you need to confirm that your stack is compatible with the upcoming version.

Nightly builds for extensions are slightly complicated due to the fact that currently DuckDB extensions binaries are tightly bound to a single DuckDB version. Because of this tight connection,
there is a potential risk for a combinatorial explosion. Therefore, not all combinations of nightly extension build and nightly DuckDB build are available.

In general, there are 2 ways of using nightly builds: using a nightly DuckDB build and using a stable DuckDB build. Let's go over the differences between the two:

### From Stable DuckDB

In most cases, users will be interested in a nightly build of a specific extension, but don't necessarily want to switch to using the nightly build of DuckDB itself. This allows using a specific bleeding-edge
feature while limiting the exposure to unstable code.

To achieve this, Core Extensions tend to regularly push builds to the [`core_nightly` repository]({% link docs/stable/extensions/installing_extensions.md %}#extension-repositories). Let's look at an example:

First we install a [**stable DuckDB build**]({% link install/index.html %}).

Then we can install and load a **nightly** extension like this:

```sql
INSTALL aws FROM core_nightly;
LOAD aws;
```

In this example we are using the latest **nightly** build of the aws extension with the latest **stable** version of DuckDB.

### From Nightly DuckDB

When DuckDB CI produces a nightly binary of DuckDB itself, the binaries are distributed with a set of extensions that are pinned at a specific version. This extension version will be tested for that specific build of DuckDB, but might not be the latest dev build. Let's look at an example:

First, we install a [**nightly DuckDB build**]({% link install/index.html %}). Then, we can install and load the `aws` extension as expected:

```sql
INSTALL aws;
LOAD aws;
```

## Updating Extensions

DuckDB has a dedicated statement that will automatically update all extensions to their latest version. The output will
give the user information on which extensions were updated to/from which version. For example:

```sql
UPDATE EXTENSIONS;
```

| extension_name | repository   | update_result         | previous_version | current_version |
|:---------------|:-------------|:----------------------|:-----------------|:----------------|
| httpfs         | core         | NO_UPDATE_AVAILABLE   | 70fd6a8a24       | 70fd6a8a24      |
| delta          | core         | UPDATED               | d9e5cc1          | 04c61e4         |
| azure          | core         | NO_UPDATE_AVAILABLE   | 49b63dc          | 49b63dc         |
| aws            | core_nightly | NO_UPDATE_AVAILABLE   | 42c78d3          | 42c78d3         |

Note that DuckDB will look for updates in the source repository for each extension. So if an extension was installed from
`core_nightly`, it will be updated with the latest nightly build.

The update statement can also be provided with a list of specific extensions to update:

```sql
UPDATE EXTENSIONS (httpfs, azure);
```

| extension_name | repository   | update_result         | previous_version | current_version |
|:---------------|:-------------|:----------------------|:-----------------|:----------------|
| httpfs         | core         | NO_UPDATE_AVAILABLE   | 70fd6a8a24       | 70fd6a8a24      |
| azure          | core         | NO_UPDATE_AVAILABLE   | 49b63dc          | 49b63dc         |

## Target DuckDB Version

Currently, when extensions are compiled, they are tied to a specific version of DuckDB. What this means is that, for example, an extension binary compiled for version 0.10.3 does not work for version 1.0.0. In most cases, this will not cause any issues and is fully transparent; DuckDB will automatically ensure it installs the correct binary for its version. For extension developers, this means that they must ensure that new binaries are created whenever a new version of DuckDB is released. However, note that DuckDB provides an [extension template](https://github.com/duckdb/extension-template) that makes this fairly simple.

## In-Tree vs. Out-of-Tree

Originally, DuckDB extensions lived exclusively in the DuckDB main repository, `github.com/duckdb/duckdb`. These extensions are called in-tree. Later, the concept
of out-of-tree extensions was added, where extensions were separated into their own repository, which we call out-of-tree.

While from a user's perspective, there are generally no noticeable differences, there are some minor differences related to versioning:

* in-tree extensions use the version of DuckDB instead of having their own version
* in-tree extensions do not have dedicated release notes, their changes are reflected in the regular [DuckDB release notes](https://github.com/duckdb/duckdb/releases)
* core out-of tree extensions tend to live in repositories named `github.com/duckdb/duckdb-⟨extension_name⟩`{:.language-sql .highlight} but the name may vary. See the [full list]({% link docs/stable/core_extensions/overview.md %}) of core extensions for details.

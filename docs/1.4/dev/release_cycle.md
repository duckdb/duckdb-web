---
layout: docu
title: Release Cycle
---

This document outlines the DuckDB and core extension release cycle framework. It is intended for developers working on
DuckDB extensions to better understand the underlying processes.

## Overview

- DuckDB follows [Semantic Versioning](https://semver.org/) (`v<MAJOR>.<MINOR>.<PATCH>`)
- Minor versions are released approximately every 4 months
- Patch releases are issued as needed for:
    - The latest stable version
    - The current Long Term Support (LTS) version
- All releases are listed in the [Release Calendar](https://duckdb.org/release_calendar.html)

### Terminology

In the release docs we use some basic terminology to describe versions and branches. We briefly go over them here.

- **`vx.y.z`**: The latest stable release
- **`vx.y-codename`**: The name of the branch that will produce `vx.y.<n>` releases
- **`vx.<y+1>-codename`**: The branch name that is used for the branch that will produce the next minor release
- **`Main release cycle`**: The branches, commits, and PRs related to producing `vx.<y+1>.0` and `vx.y.<z+1>` releases
- **`Active branch`**: A branch that is part of the main release cycle. Either main or vx.<y+n>-codename where n >= 0
- **`Single branch extension`**: Extension with 1 active branch. Since main is always an active branch this is always
  main. This means all other branches of format `vx.y-codename` must be `vx.<y-n>-codename` where `n >= 1`
- **`Multi branch extension`**: Extension with more than 1 active branch
- **`Two branch extension`**: Extension with two active branches: main and `vx.y-codename`
- **`Three branch extension`**: Extension with three active branches: main, `vx.y-codename`, and `vx.<y+1>-codename`
- **`LTS release`**: Long term support release. These releases will receive support (patch releases) beyond their
  lifetime in the active release cycle. Currently LTS releases will receive 1 year of support
- **`Unstable API extension`**: An extension targeting the *unstable* extension API. This can be both the C++ API or the
  unstable C API. These extensions are not binary-compatible across multiple DuckDB versions
- **`Stable API extension`**: An extension targeting the *stable* C API of DuckDB. These extensions are
  binary-compatible across multiple DuckDB versions
- **`In-tree extensions`**: Extensions that live inside the `duckdb/duckdb` source tree

### Main Branches and Tags

In git-based version control, branches are used to allow multiple versions of the same codebase to co-exist. At DuckDB,
there are two core branches that play the main role in the DuckDB (and extensions) release cycle. We will start off by
listing the format these core branches come in.

- **`main`** branch: the main branch can mean various things, but can generally be considered the catch-all branch
- **`vx.y-codename`** branch: the branch used to produce all `vx.y.z` releases
- **`vx.y.z`** tag: a stable release of DuckDB. These tags are write-only and will always be tied to the same commit

## The Main DuckDB Release Cycle

> LTS (Long-Term Support) releases follow a separate maintenance cycle to provide extended support and stability.

The main DuckDB release cycle consists of 3 main phases: *Mid-cycle*, *Pre-release* and *Feature freeze*. These phases are clearly defined and communicated to ensure the
whole team is synchronized and working together towards the next release.

### Phase 1: Mid-Cycle

#### Active DuckDB Branches

- `main`
- `vx.y-codename`

#### Description

The *mid-cycle* phase is the most common phase of the release cycle, with about 75% of the time being spent in this
phase. It can be seen as *business-as-usual*, where the upcoming release is still far away and the team is working hard
on merging a variety of features and bug-fixes. During this phase, patch releases (`vx.y.<z+n>`) may be created from the
`vx.y-codename` branch. The patches are merged into the `vx.y-codename` branch, and the `vx.y-codename` branch is
frequently merged into main to keep the two in sync.

#### PRs into DuckDB

- Bug-fixes for `vx.y.<z+n>` patch releases are merged into `vx.y-codename`
- Features and bug-fixes for `vx.<y+1>.0` are merged into `main`

### Phase 2: Pre-Release

#### Active Branches

- `main`
- `vx.y-codename`
- `vx.<y+1>-codename`

#### Description

The pre-release phase is intended to prepare for the upcoming `vx.<y+1>.0` minor release. At the start of this phase,
the `vx.<y+1>-codename` branch is created. This branch will be used to produce the upcoming minor release and is the
branch from which all subsequent `vx.<y+1>.<n>` patch releases are released.

#### PRs into DuckDB

- Bug-fixes for `vx.y.<z+1>` patch releases are merged into `vx.y-codename`
- Features and bug-fixes for `vx.<y+1>.0` are merged into `vx.<y+1>-codename`
- Features for `vx.<y+2>.0` are merged into `vx.<y+2>-codename`

### Phase 3: Feature Freeze

#### Active Branches

- `main`
- `vx.y-codename`
- `vx.<y+1>-codename`

#### Description

The feature freeze phase is the phase closest to release. During this phase features are no longer allowed to be merged
into `vx.<y+1>-codename` and only bug fixes are merged. This phase is intended to ensure the quality of the upcoming
release. During this phase additional testing and benchmarking is performed while reducing the risk of introducing
last-minute bugs by disallowing feature merges.

#### PRs into DuckDB

- Bug-fixes for `vx.y.<z+1>` are no longer allowed, should target `vx.<y+1>.0` instead
- Bug-fixes for `vx.<y+1>.0` are merged into `vx.<y+1>-codename`
- Features for `vx.<y+1>.0` are no longer allowed, should target `vx.<y+2>.0` instead
- Features for `vx.<y+2>.0` are merged into `vx.<y+2>-codename`

## Main Extension Release Cycle

Most DuckDB extensions are completely separate from the main `duckdb/duckdb` repository and are free to follow their own
release cycle. In this section we categorize different types of DuckDB extensions and go over their release cycles.

To describe the release cycle of extensions, we need to first categorize extensions in three different groups, as
extensions share the same release cycle based on which of these three categories they belong to.

- In-tree extensions
- Unstable API extensions
- Stable API extensions

We will now go over the release cycles of the three different categories, in order of increasing complexity.

### In-Tree Extensions

For *in-tree extensions*, the release cycle is very simple. Since their code lives in the `duckdb/duckdb` repository,
they move in complete lock-step with DuckDB. This means they share the same versioning and branching. In this sense they
are not really extensions, but more lazy-loadable parts of the `duckdb/duckdb` codebase.

### Stable API Extensions

Stable API extensions in DuckDB are a relatively new concept, but are planned to form the majority of extensions in the
future. Stable API extensions are built on the stable C extension API, making them binary compatible with multiple
versions of DuckDB. This means that their release cycle can/should also be completely separate from the DuckDB release
cycle.

While the release cycle for stable API extensions is still work in progress, the basic idea is that the release cycle of
stable API extensions consists of a similar but separate cycle to that of `duckdb/duckdb`, where every version will
target 1 or more versions of DuckDB.

### Unstable API Extensions

Unstable API extensions currently make up the majority of DuckDB extensions. These extensions either target the C++
extension API, or the unstable C extension API. They are, from a release cycle point of view, the most complex. Every
version of an unstable API extension only targets a single DuckDB version. This 1:1 tie means that the release cycle of
these extensions tends to form a sometimes intricate dance around the main DuckDB release cycle. While the goal is to
move as many extensions over to stable APIs, we expect unstable API extensions to be around for quite some time so there
remains a need to clearly define their lifecycle. Therefore we will use the remainder of this section to describe it.

#### Categorizing by Branching

To start, we will divide the unstable API extensions into different subcategories. Just like DuckDB itself, these
extensions follow the same branching scheme as DuckDB where a combination of `main` and `vx.y-codename` play the main
role. We will now define the three types of unstable extensions by looking at their **number of active branches**.

- **Single branch extensions** have only the `main` *active* branch
- **Two branch extensions** have two *active* branches: `main` and `vx.y-codename`
- **Three branch extensions** have three *active* branches: `main`, `vx.y-codename`, and `vx.<y+1>-codename`

#### DuckDB Targets

Every unstable API extension should target a single version of DuckDB. This target version is defined by a combination
of **the `duckdb` submodule** and the target version in the [`MainDistributionPipeline`](https://github.com/duckdb/extension-template/blob/main/.github/workflows/MainDistributionPipeline.yml) workflow.
Which version an extension targets depends on the release cycle phase and the branch. We will now go over all
combinations

- Phase: **Mid-cycle**
    - Type: **Single branch**
        - Extension **`main`** `->` DuckDB **`vx.y.z`** or **`main`**
    - Type: **Two branch**
        - Extension **`main`** `->` DuckDB **`vx.y.z`** or **`main`**
        - Extension **`vx.y-codename`** `->` DuckDB **`vx.y.z`** or **`vx.y-codename`**
    - Type: **Three branch**: should not exist
- Phase: **Pre-release** / **Patch**
    - Type: **Single branch**
        - Extension **`main`** `->` DuckDB **`vx.y.z`** or **`vx.<y+1>-codename`**
    - Type: **Two branch**
        - Extension **`main`** `->` DuckDB **`vx.y.z`** or **`vx.<y+1>-codename`**
        - Extension **`vx.y-codename`** `->` DuckDB **`vx.y.z`** or **`vx.y-codename`**
    - Type: **Three branch**
        - Extension **`main`** `->` DuckDB **`main`**
        - Extension **`vx.y-codename`** `->` DuckDB **`vx.y.z`** or **`vx.y-codename`**
        - Extension **`vx.<y+1>-codename`** `->` DuckDB **`vx.<y+1>-codename`**

#### Where to Merge PRs

To know where to merge a PR into an unstable API extension depends on two things: the
current release phase and the type of extensions. We will now go over all combinations.

- Phase: **Mid-cycle**
    - Type: **Single branch**
        - if DuckDB target: `vx.y.z`:
            - PR for **`vx.y.<z+1>`** into **`main`**[^1]
            - PR for **`vx.<y+1>.0`** merges into **`main`**
        - if DuckDB target: `main`:
            - PR for **`vx.y.<z+1>`** are **impossible**
            - PR for **`vx.<y+1>.0`** merges into **`main`**
    - Type: **Two branch**
        - PR for **`vx.y.<z+1>`** merges into **`vx.y-codename`**
        - PR for **`vx.<y+1>.0`** merges into **`main`**
    - Type: **Three branch**
        - PR for **`vx.y.<z+1>`** merges into **`vx.y-codename`**
        - PR for **`vx.<y+1>.0`** merges into **`vx.<y+1>-codename`**
        - PR for **`vx.<y+2>.0`** merges into **`main`**
- Phase: **Pre-release** / **Patch**
    - Type: **Single branch**
        - if DuckDB target: `vx.y.z`:
            - PR for **`vx.y.<z+1>`** into **`main`**[^1] [^2]
            - PR for **`vx.<y+1>.0`** merges into **`main`**
        - if DuckDB target: `main`:
            - PR for **`vx.y.<z+1>`** are **impossible**
            - PR for **`vx.<y+1>.0`** merges into **`main`**
    - Type: **Two branch**
        - PR for **`vx.y.<z+1>`** merges into **`vx.y-codename`** [^2]
        - PR for **`vx.<y+1>.0`** merges into **`main`**
    - Type: **Three branch**
        - PR for **`vx.y.<z+1>`** merges into **`vx.y-codename`**[^2]
        - PR for **`vx.<y+1>.0`** merges into **`vx.<y+1>-codename`**
        - PR for **`vx.<y+2>.0`** merges into **`main`**

[^1]: Single branch extensions require manual version updates to ensure changes are included in the targeted release.
[^2]: Patch releases during pre-release or feature-freeze phases are uncommon. Consider targeting changes for the next
minor release instead.

#### What Extension Version Will Be Released?

Every DuckDB release, a complete set of all core extensions should be available. For unstable API extensions, this means
a rebuild of the binaries. For the core extensions, this build generally happens through the `duckdb/duckdb` CI. This
means that the list of extensions that will be available on release is documented in
the [extension config files](https://github.com/duckdb/duckdb/tree/main/.github/config/extensions). However, this config
file may not always be up to date. To decide which version of an extension should be part of the upcoming release, we
define the following sources-of-truth for latest extension version based on the release type (major/minor) and extension
type (single/multi branch):

- Release type: **Patch**
    - Extension type: **Single branch**
        - Latest version: **commit
          in [config files](https://github.com/duckdb/duckdb/tree/main/.github/config/extensions)**
    - Extension type: **Multi branch**
        - Latest version: Extension **`vx.y-codename`** branch
- Release type: **Minor**
    - Extension type: **Single branch**
        - Latest version: Extension **`main`** branch
    - Extension type: **Two branch**
        - Latest version: Extension **`main`** branch
    - Extension type: **Three branch**
        - Latest version: Extension **`vx.<y+1>-codename`** branch

#### Switching between Single Branch, Two Branch and Three Branch

Switching between the different branch types for extensions is a fairly straightforward process and should be done as follows:

- Switch: **Single branch** `->` **Two branch**
    - When: during **any** phase
    - Reasons:
        - When desire arises to merge features not eligible for `vx.y.<z+1>` while also maintaining ability to do releases for `vx.y.<z+n>`
        - To be able to test with latest DuckDB main while maintaining ability to do releases for `vx.y.<z+n>` (including `vx.y.z` itself)
    - Actions:
        - Create branch `vx.y-codename` from a commit on main between HEAD of `main` and the commit in the DuckDB `vx.y.z` config file.
- Switch: **Two branch** `->` **Three branch**
    - When: during **Pre-release** or **Feature-freeze** phase
    - Reasons:
        - Whenever a feature needs to be merged that is not eligible for merging into `vx.<y+1>.0`.
    - Actions:
        - Create `vx.<y+1>-codename` branch from main
- Switch **Three branch** `->` **Two branch** or **Two branch** `->` **Single branch**
    - When: part of transition from **Feature Freeze** `->` **Mid-cycle**
    - Action: happens automatically (`vx.y-codename` becomes *inactive* by definition)

---
layout: post
title: "Dependency Management in DuckDB Extensions"
author: Sam Ansmink
excerpt: While core DuckDB has zero external dependencies, building extensions with dependencies is now very simple, with built-in support for vcpkg, an open-source package manager with support for over 2000 C/C++ packages. Interested in building your own? Check out the [extension template](https://github.com/duckdb/extension-template).
---

## Introduction

Ever since the birth of DuckDB, one of its main pillars has been its strict no-external-dependencies philosophy.
Paraphrasing [this 2019 SIGMOD paper](https://hannes.muehleisen.org/publications/SIGMOD2019-demo-duckdb.pdf) on DuckDB:
*To achieve the requirement of having practical “embeddability” and portability, the database needs to run in whatever
environment the host does. Dependencies on external libraries (e.g. openssh) for either compile- or runtime have been
found to be problematic.*

In this blog post, we will cover how DuckDB manages to stay true to this philosophy without forcing DuckDB developers
down the path of complete abstinence. Along the way, we will show practical examples of how external dependencies are
possible, and how you can use this when creating your own DuckDB extension.

## The difficulties of complete abstinence

Having no external dependencies is conceptually very simple. However, in a real-world system with real-world
requirements, it is difficult to achieve. Many features require complex implementations of protocols and algorithms, and
many high-quality libraries exist that implement them. What this means for DuckDB (and most other systems, for that matter)
is that there are basically three options for handling requirements with potential external dependencies:

1. Inlining external code
2. Rewriting the external dependency
3. Breaking the no-dependency rule

The first two options are pretty straightforward: to avoid depending on some external software, just make it part of
the codebase. By doing so, the unpredictable nature of depending on somebody else is now eliminated! DuckDB has applied
both inlining and rewriting to prevent dependencies. For example, the [Postgres parser](https://github.com/duckdb/duckdb/tree/main/third_party/libpg_query) and
[MbedTLS](https://github.com/duckdb/duckdb/tree/main/third_party/mbedtls) libraries are inlined into DuckDB, whereas the S3 support is provided
using a custom implementation of the AWS S3 protocol.

Okay, great – problem solved, right? Well, not so fast. Most people with some software engineering experience will realize
that both inlining and rewriting come with serious drawbacks. The
most fundamental issue is probably related to code maintenance. Every significant piece of software needs some level of
maintenance. Ranging from fixing bugs to dealing with changing (build) environments or requirements, code will
need to be modified to stay functional and relevant. When inlining/rewriting dependencies, this also copies over the
maintenance burden.

For DuckDB, this historically meant that for each dependency, very careful consideration was made to balance the
increased maintenance burden against the necessity of dependency. Including a dependency meant the responsibility of
maintaining it, so this decision was never taken lightly. This works well in many cases and has the added benefit of forcing
developers to think critically about including a dependency and not mindlessly bolt on library after library. However,
for some dependencies, this just doesn't work. Take, for example, the SDKs of large cloud providers. They tend to be pretty
massive, very frequently updated, and packed with arguably essential functionality for an increasingly mature analytical
database. This leaves an awkward choice: either not provide these essential features or break the no-dependency rule.

## DuckDB extensions

This is where extensions come in. Extensions provide an elegant solution to the dilemma of dependencies by allowing
fine-grained breakage of the no-dependency rule. Moving dependencies out of DuckDB's core into extensions, the core
codebase can remain, and does remain, dependency-free.
This means that DuckDB's “Practical embeddability and portability” remains unthreatened. On the other hand, DuckDB can
still provide features that inevitably require depending on some 3rd party library. Furthermore, by moving dependencies
to extensions, each extension can have different levels of exposure to instability from dependencies. For example, some
extensions may choose to depend only on highly mature, stable libraries with good portability, whereas others may choose
to include more experimental dependencies with limited portability. This choice is then forwarded to the user by
allowing them to choose which extension to use.

At DuckDB, this realization of the importance of extensions and its relation to the no-dependency rule came
[very early](https://github.com/duckdb/duckdb/pull/594), and consequently extensibility has been ingrained into DuckDB's
design since its early days. Today, many parts of DuckDB can be extended. For example, you can add functions (table,
scalar, copy, aggregation), filesystems, parsers, optimizer rules, and much more. Many new features that are added to
DuckDB are added in extensions and are grouped by either functionality or by set of dependencies. Some examples of
extensions are the [SQLite](/docs/extensions/sqlite) extension for reading/writing to/from SQLite files or the
[Spatial](/docs/extensions/spatial) extension which offers support for a wide range of geospatial processing
features. DuckDB's extensions are distributed as loadable binaries for most major platforms (including
[DuckDB-Wasm](/2023/12/18/duckdb-extensions-in-wasm)), allowing loading and installing extensions with two simple SQL
statements:

```sql
INSTALL spatial;
LOAD spatial;
```

For most core extensions maintained by the DuckDB team, there is even an auto-install and auto-load feature which will detect the required extensions for
a SQL statement and automatically install and load them. For a detailed description of which extensions are available
and how to use them, check out the [docs](/docs/extensions/overview).

## Dependency management

So far, we've seen how DuckDB avoids external dependencies in its core codebase by moving them out of the core repository into
extensions. However, we're not out of the woods yet. As DuckDB is written in C++, the most natural way to write
extensions is C++. In C++, though, there is no standard tooling like a package manager and the answer to the
question of how to do dependency management in C++ has been, for many years: *“Through much pain and anguish.”* Given
DuckDB's focus on portability and support for many platforms, managing dependencies manually is not feasible: dependencies generally are built from source, with each their own intricacies requiring special build flags and
configuration for different platforms. With a growing ecosystem of extensions, this would quickly turn into an
unmaintainable mess.

Fortunately, much has changed in the C++ landscape over the past few years. Today, good dependency managers do exist.
One of them is Microsoft's [vcpkg](https://vcpkg.io/). It has become a highly notable player among C++ dependency
managers, as proven by its 20k+ GitHub stars and native support
from [CLion](https://blog.jetbrains.com/clion/2023/01/support-for-vcpkg-in-clion/)
and [Visual Studio](https://devblogs.microsoft.com/cppblog/vcpkg-is-now-included-with-visual-studio/). vcpkg contains
over 2000 dependencies such
as [Apache Arrow](https://github.com/microsoft/vcpkg/tree/master/ports/arrow), [yyjson](https://github.com/microsoft/vcpkg/tree/master/ports/yyjson),
and [various](https://github.com/microsoft/vcpkg/tree/master/ports/azure-core-cpp) [cloud](https://github.com/microsoft/vcpkg/tree/master/ports/aws-sdk-cpp) [provider](https://github.com/googleapis/google-cloud-cpp)
SDKs.

For anyone who has ever used a package manager, using vcpkg will feel quite natural. Dependencies are specified in
a `vcpkg.json` file, and vcpkg is hooked into the build system. Now, when building, vcpkg ensures that the dependencies
specified in the `vcpkg.json` are built and available. vcpkg supports integration with multiple build systems, with a
focus on its seamless CMake integration.

## Using vcpkg with DuckDB

Now that we covered DuckDB extensions and vcpkg, we have shown how DuckDB can manage dependencies without sacrificing
portability, maintainability and stability more than necessary. Next, we'll make things a bit more tangible by looking at
one of DuckDB's extensions and how it uses vcpkg to manage its dependencies.

### Example: Azure extension

The [Azure](/docs/extensions/azure) extension provides functionality related to [Microsoft Azure](https://azure.microsoft.com/),
one of the major cloud providers. DuckDB's Azure extension depends on the Azure C++ SDK to support reading directly from
Azure Storage. To do so it adds a custom filesystem and [secret type](/docs/configuration/secrets_manager), which can be
used to easily query from authenticated Azure containers:

```sql
CREATE SECRET az1 (
    TYPE AZURE,
    CONNECTION_STRING '<redacted>'
);
SELECT column_a, column_b
FROM 'az://my-container/some-file.parquet';
```

To implement these features, the Azure extension depends on different parts of the Azure SDK. These are specified in the
Azure extensions `vcpkg.json`:

```json
{
  "dependencies": [
    "azure-identity-cpp",
    "azure-storage-blobs-cpp",
    "azure-storage-files-datalake-cpp"
  ]
}
```

Then, in the Azure extension's `CMakelists.txt` file, we find the following lines:

```cmake
find_package(azure-identity-cpp CONFIG)
find_package(azure-storage-blobs-cpp CONFIG)
find_package(azure-storage-files-datalake-cpp CONFIG)

target_link_libraries(${EXTENSION_NAME} Azure::azure-identity Azure::azure-storage-blobs Azure::azure-storage-files-datalake)
target_include_directories(${EXTENSION_NAME} PRIVATE Azure::azure-identity Azure::azure-storage-blobs Azure::azure-storage-files-datalake)
```

And that's basically it! Every time the Azure extension is built, vcpkg will be called first to
ensure `azure-identity-cpp`, `azure-storage-blobs-cpp` and `azure-storage-files-datalake-cpp` are built using the correct platform-specific flags and
available in CMake through `find_package`.

## Building your own DuckDB extension

Up until this part, we've focused on managing dependencies from a point-of-view of the developers of core DuckDB
contributors. However, all of this applies to anyone who wants to build an extension. DuckDB maintains a [C++ Extension Template](https://github.com/duckdb/extension-template),
which contains all the necessary build scripts, CI/CD pipeline and vcpkg configuration to build, test and deploy a DuckDB extension in
minutes. It can automatically build the loadable extension binaries for all available platforms, including Wasm.

### Setting up the extension template

To demonstrate how simple this process is, let's go through all the steps of building a DuckDB extension from scratch,
including adding a vcpkg-managed external dependency.

Firstly, you will need to install vcpkg:

```bash
git clone https://github.com/Microsoft/vcpkg.git
./vcpkg/bootstrap-vcpkg.sh
export vcpkg_TOOLCHAIN_PATH=`pwd`/vcpkg/scripts/buildsystems/vcpkg.cmake
```

Then, you create a GitHub repository based on [the template](https://github.com/duckdb/extension-template) by clicking “Use this
template”.

Now to clone your newly created extension repo (including its submodules) and initialize the template:

```bash
git clone https://github.com/⟨your-username⟩/⟨your-extension-repo⟩ --recurse-submodules
cd your-extension-repo
./scripts/bootstrap-template.py url_parser
```

Finally, to confirm everything works as expected, run the tests:

```bash
make test
```

### Adding functionality

In its current state, the extension is, of course, a little boring. Therefore, let's add some functionality! To keep
things simple, we'll add a scalar function that parses a URL and returns the scheme. We'll call the
function `url_scheme`. We start by adding a dependency to the boost url library in our `vcpkg.json` file:

```json
{
  "dependencies": [
    "boost-url"
  ]
}
```

Then, we follow up with changing our `CMakelists.txt` to ensure our dependencies are correctly included in the build.

```cmake
find_package(Boost REQUIRED COMPONENTS url)
target_link_libraries(${EXTENSION_NAME} Boost::url)
target_link_libraries(${LOADABLE_EXTENSION_NAME} Boost::url)
```

Then, in `src/url_parser_extension.cpp`, we remove the default example functions and replace them with our
implementation of the `url_scheme` function:

```cpp
inline void UrlParserScalarFun(DataChunk &args, ExpressionState &state, Vector &result) {
  auto &name_vector = args.data[0];
  UnaryExecutor::Execute<string_t, string_t>(
    name_vector, result, args.size(),
    [&](string_t url) {
          string url_string = url.GetString();
          boost::system::result<boost::urls::url_view> parse_result = boost::urls::parse_uri( url_string );
          if (parse_result.has_error() || !parse_result.value().has_scheme()) {
              return string_t();
          }
          string scheme = parse_result.value().scheme();
          return StringVector::AddString(result, scheme);
      });
}

static void LoadInternal(DatabaseInstance &instance) {
  auto url_parser_scalar_function = ScalarFunction("url_scheme", {LogicalType::VARCHAR}, LogicalType::VARCHAR, UrlParserScalarFun);
  ExtensionUtil::RegisterFunction(instance, url_parser_scalar_function);
}
```

With our extension written, we can run `make` to build both DuckDB and the extension. After the build is finished, we
are ready to try out our extension. Since the build process also builds a fresh DuckDB binary with the extension loaded
automatically, all we need to do is run `./build/release/duckdb`, and we can use our newly added scalar function:

```sql
SELECT url_scheme('https://github.com/duckdb/duckdb');
```

Finally, as we are well-behaved developers, we add some tests by overwriting the default test `test/sql/url_parser.test`
with:

```sql
require url_parser

# Confirm the extension works
query I
SELECT url_scheme('https://github.com/duckdb/duckdb')
----
https

# On parser errors or not finding a scheme, the result is also an empty string
query I
SELECT url_scheme('not:\a/valid_url')
----
(empty)
```

Now all that's left to do is confirm everything works as expected with `make test`, and push these changes to the remote
repository. Then, GitHub Actions will take over and ensure the extension is built for all of DuckDB's supported
platforms.

For more details, check out the template repository. Also, the example extension we built in this blog is published
[here](https://github.com/samansmink/url-parse-extension). Note that in the demo, the Wasm and MinGW builds have been
[disabled](https://github.com/samansmink/url-parse-extension/blob/935c4273eea174d99d25be156d4bfea8f55abfa6/.github/workflows/MainDistributionPipeline.yml#L21)
due to [outstanding](https://github.com/microsoft/vcpkg/issues/35408) [issues](https://github.com/microsoft/vcpkg/issues/35549)
with the boost-url dependency for building on these platforms. As these issues are fixed upstream, re-enabling their builds
for the extension is very simple. Of course, as the author of this extension, it could make a lot of sense to fix these compile issues
yourself in vcpkg and fix them not only for this extension, but for the whole open-source community!

## Conclusion

In this blog post, we've explored DuckDB's journey towards managing dependencies in its extension ecosystem while
upholding its core philosophy of zero external dependencies. By leveraging the power of extensions, DuckDB can maintain
its portability and embeddability while still providing essential features that require external dependencies. To
simplify managing dependencies, Microsoft's vcpkg is integrated into DuckDB's extension build systems both for
DuckDB-maintained extension and third-party extensions.

If this blog post sparked your interest in creating your own DuckDB extension, check out
the [C++ Extension Template](https://github.com/duckdb/extension-template),
the [DuckDB docs on extensions](/docs/extensions/overview),
and the very handy [duckdb-extension-radar repository](https://github.com/mehd-io/duckdb-extension-radar) that tracks public DuckDB extensions.
Additionally, DuckDB has a [Discord server](https://discord.com/invite/tcvwpjfnZx) where you can ask for help on
extensions or anything DuckDB-related in general.

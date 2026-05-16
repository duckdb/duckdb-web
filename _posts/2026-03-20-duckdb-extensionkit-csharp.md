---
layout: post
title: "DuckDB.ExtensionKit: Building DuckDB Extensions in C#"
author: "Giorgi Dalakishvili"
thumb: "/images/blog/thumbs/duckdb-extensionkit-csharp.jpg"
image: "/images/blog/thumbs/duckdb-extensionkit-csharp.svg"
excerpt: "DuckDB.ExtensionKit brings DuckDB extension development to the .NET ecosystem. By building on DuckDB's stable C Extension API and leveraging .NET Native AOT compilation, it lets C# developers define scalar and table functions, which can be shipped as native DuckDB extensions."
tags: ["extensions"]
---

## Introduction

DuckDB has a flexible extension mechanism that allows extensions to be loaded dynamically at runtime. This makes it easy to extend DuckDB’s main feature set without adding everything to the main binary. Extensions can add support for new file formats, introduce custom types, or provide new scalar and table functions. A significant part of DuckDB’s functionality is actually implemented using this extension mechanism in the form of core extensions, which are developed alongside the engine itself by the DuckDB team. For example, DuckDB can read and write JSON files via the `json` extension and integrate with PostgreSQL using the `postgres` extension. 

DuckDB also has a thriving ecosystem of [community extensions]({% link community_extensions/index.md %}), i.e., third-party extensions, maintained by community members, covering a wide range of use cases and integrations. For example, you can expose additional cryptographic functionality through the `crypto` community extension.

## How Extensions Are Built Today

Today, developers can use the same C++ API that the core extensions use for developing extensions. A template for creating extensions is available in the [`extension-template` repository](https://github.com/duckdb/extension-template/). While powerful, the C++ extension API is tightly coupled to DuckDB’s internal APIs, so it can (and often will) change between DuckDB versions. Additionally, using it requires building the whole DuckDB engine and its documentation is not as complete as that of the C API.

To solve these issues, DuckDB also provides an [experimental template](https://github.com/duckdb/extension-template-c) for C/C++ based extensions that link with the **C Extension API** of DuckDB. This API provides a stable, backwards-compatible interface for developing extensions and is designed to allow extensions to work across different DuckDB versions. Because it is a C-based API, it can also be used from other programming languages such as Rust.

Even with the C API, writing extensions still means working at a low level, performing manual memory management, and writing a lot of boilerplate code. While the C API solves stability and compatibility, it doesn’t solve *developer experience* for higher-level ecosystems. This is where DuckDB.ExtensionKit comes in, aiming to make extension development more accessible to developers working in the .NET ecosystem. By building on top of the DuckDB C Extension API and compiling extensions using the [.NET Native AOT (Ahead-of-Time) compilation](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/), DuckDB.ExtensionKit offers the best of both worlds: native DuckDB extensions that integrate like any other extension, combined with the productivity and rich library ecosystem of C# and .NET.

## DuckDB.ExtensionKit

DuckDB.ExtensionKit provides a set of C# APIs and build tooling for implementing DuckDB extensions. It exposes the low-level DuckDB C Extension API as C# methods, and also provides type-safe, higher-level APIs for defining scalar and table functions, while still producing native DuckDB extensions. The toolkit also includes a source generator that automatically generates the required boilerplate code, including the native entry point and API initialization.

With DuckDB.ExtensionKit, building an extension closely resembles building a regular C# library. Extension authors create a C# project that references the ExtensionKit runtime and implements functions using the provided, type-safe APIs that expose DuckDB concepts.

At build time, the source generator emits the required boilerplate, including the native entry point and extension initialization. The project is then compiled using .NET Native AOT, producing a native DuckDB extension binary that can be loaded and used by DuckDB like any other extension, without requiring a .NET runtime.

To show a concrete example for this process, the following snippet shows a small DuckDB extension implemented using DuckDB.ExtensionKit that exposes both a scalar function and a table function for working with JWTs (JSON Web Token). At a high level, writing an extension with DuckDB.ExtensionKit involves defining a C# type that represents the extension and registering functions explicitly. In the example below, this is done by creating a `partial` class annotated with the `[DuckDBExtension]` attribute and implementing the `RegisterFunctions` method. The implementation makes use of the `System.IdentityModel.Tokens.Jwt` NuGet package, illustrating how extensions can easily take advantage of existing .NET libraries.

We'll add two functions, a scalar function for extracting *a single claim* from a JWT and a table function for extracting *multiple claims.*

```cs
public static partial class JwtExtension
{
  private static void RegisterFunctions(DuckDBConnection connection)
  {
    connection.RegisterScalarFunction<string, string, string?>("extract_claim_from_jwt", ExtractClaimFromJwt);

    connection.RegisterTableFunction("extract_claims_from_jwt", (string jwt) => ExtractClaimsFromJwt(jwt),
                                     c => new { claim_name = c.Key, claim_value = c.Value });
  }

  private static string? ExtractClaimFromJwt(string jwt, string claim)
  {
    var jwtHandler = new JwtSecurityTokenHandler();
    var token = jwtHandler.ReadJwtToken(jwt);
    return token.Claims.FirstOrDefault(c => c.Type == claim)?.Value;
  }

  private static Dictionary<string, string> ExtractClaimsFromJwt(string jwt)
  {
    var jwtHandler = new JwtSecurityTokenHandler();
    var token = jwtHandler.ReadJwtToken(jwt);
    return token.Claims.ToDictionary(c => c.Type, c => c.Value);
  }
}
```

In just 25 lines, we have built an extension that adds `extract_claim_from_jwt` and `extract_claims_from_jwt` functions to DuckDB. We can call these functions just like any other function. For example, to extract the `name` field from a claim, we can run:

```sql
SELECT extract_claim_from_jwt(
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImExZmIyY2NjN2FiMjBiMDYyNzJmNGUxMjIwZDEwZmZlIn0.eyJpc3MiOiJodHRwczovL2lkcC5sb2NhbCIsImF1ZCI6Im15X2NsaWVudF9hcHAiLCJuYW1lIjoiR2lvcmdpIERhbGFraXNodmlsaSIsInN1YiI6IjViZTg2MzU5MDczYzQzNGJhZDJkYTM5MzIyMjJkYWJlIiwiYWRtaW4iOnRydWUsImV4cCI6MTc2NjU5MTI2NywiaWF0IjoxNzY2NTkwOTY3fQ.N7h2xc4rgS4oPo8IO9wyG1lnr2wqTUC80YudWTXp7rXmU2JdsUiweKmuYVVbygdJAR4PJmbQtak4_VuZg2fZFILVpzDyLvGITfUW_18XuDQ_SIm3VlfAuHOVHfruuvvSAfjUkTW2Jlrv3ihFYgusV58vjhcVFHssOGMEbtMNo10Jf62dczVVGNZXh_OOLS0nTLffhY94sZddqQIE56W8xhLK5YMO4gO8voMzhUwDwucnVvyNfui38MPDNdTSKjn3Ab0hG8jzOVhbYSCHf0eQsbxPzGtXUCJobScWDb78IphFWec6W4ugIYp5CMh3C_noQi94NYjQg2P-AJ5FLCKzKA',
    'name'
);
```

This returns `Giorgi Dalakishvili`. Let's test the table function:

```sql
SELECT *
FROM extract_claims_from_jwt(
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImExZmIyY2NjN2FiMjBiMDYyNzJmNGUxMjIwZDEwZmZlIn0.eyJpc3MiOiJodHRwczovL2lkcC5sb2NhbCIsImF1ZCI6Im15X2NsaWVudF9hcHAiLCJuYW1lIjoiR2lvcmdpIERhbGFraXNodmlsaSIsInN1YiI6IjViZTg2MzU5MDczYzQzNGJhZDJkYTM5MzIyMjJkYWJlIiwiYWRtaW4iOnRydWUsImV4cCI6MTc2NjU5MTI2NywiaWF0IjoxNzY2NTkwOTY3fQ.N7h2xc4rgS4oPo8IO9wyG1lnr2wqTUC80YudWTXp7rXmU2JdsUiweKmuYVVbygdJAR4PJmbQtak4_VuZg2fZFILVpzDyLvGITfUW_18XuDQ_SIm3VlfAuHOVHfruuvvSAfjUkTW2Jlrv3ihFYgusV58vjhcVFHssOGMEbtMNo10Jf62dczVVGNZXh_OOLS0nTLffhY94sZddqQIE56W8xhLK5YMO4gO8voMzhUwDwucnVvyNfui38MPDNdTSKjn3Ab0hG8jzOVhbYSCHf0eQsbxPzGtXUCJobScWDb78IphFWec6W4ugIYp5CMh3C_noQi94NYjQg2P-AJ5FLCKzKA'
);
```

This returns:

<div class="monospace_table"></div>

<!-- markdownlint-disable MD034 -->

| claim_name | claim_value                      |
| ---------- | -------------------------------- |
| iss        | https://idp.local                |
| aud        | my_client_app                    |
| name       | Giorgi Dalakishvili              |
| sub        | 5be86359073c434bad2da3932222dabe |
| admin      | true                             |
| exp        | 1766591267                       |
| iat        | 1766590967                       |

<!-- markdownlint-enable MD034 -->

## How DuckDB.ExtensionKit Works

DuckDB.ExtensionKit relies on several modern C# language and runtime features to efficiently bridge DuckDB’s C extension API to managed code. These features make it possible to build native extensions in C# without introducing a managed runtime dependency at load time.

## Function Pointers

DuckDB’s C extension API is exposed as a **versioned function table**: a large struct ([duckdb\_ext\_api\_v1](https://github.com/duckdb/extension-template-c/blob/152f7fba8df6ef2d3c48caf344fead63aa1e0501/duckdb_capi/duckdb_extension.h#L70-L545)) whose fields are C function pointers (e.g., `duckdb_open`, `duckdb_register_scalar_function`, `duckdb_vector_get_data`, and so on). DuckDB.ExtensionKit mirrors this mechanism in C#. It defines a [C# representation of the struct](https://github.com/Giorgi/DuckDB.ExtensionKit/blob/99e4b91d50c5c840a3c4f69ea92d4fd4e49e7b76/DuckDB.ExtensionKit/DuckDBExtApiV1.cs#L7-L551) (`DuckDBExtApiV1`), where each field is declared as a [C# function pointer](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code#function-pointers) (`delegate* unmanaged[Cdecl]<...>`). This maps the C ABI directly: calling into DuckDB becomes a simple indirect call through a function pointer field, rather than a delegate invocation with runtime marshaling.

## Entrypoint

A DuckDB extension needs to expose an **entrypoint function** following the C calling convention (the entrypoint that should be exported from the binary is the name of the extension plus `_init_c_api`). This way, DuckDB can locate it when the extension is loaded. In the C extension template, this is handled with macros that generate the exported function and the surrounding boilerplate.

DuckDB.ExtensionKit follows the same model, but generates the boilerplate from C# instead of C macros. The source generator emits a native-compatible entrypoint that retrieves the API table (via the `access` object) and performs the required initialization, just like the C template does. The generated method is annotated with `[UnmanagedCallersOnly(EntryPoint = "...")]`, which instructs the .NET toolchain to [export a real native symbol](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/interop#native-exports) with that name and make it callable from C. With .NET Native AOT, this becomes an actual exported function in the produced binary – allowing DuckDB to load and call into the extension exactly as it would for a C implementation.

## Native AOT

Finally, Native AOT is what makes this approach practical for DuckDB extensions. Once the extension code and generated sources are compiled, the project is published using .NET Native AOT. This step produces a native binary with no dependency on a managed runtime at load time. The resulting artifact is a native DuckDB extension that can be loaded and executed in the same way as extensions written in C or C++. From DuckDB’s perspective, there is no difference between an extension built with DuckDB.ExtensionKit and one implemented in a traditional native language.

## Current Status and Limitations

DuckDB.ExtensionKit, just like the C extension template, is currently experimental. The APIs are still evolving, and not all extension features supported by DuckDB are exposed yet.

The toolkit relies on .NET Native AOT, which means extensions need to be built for specific target platforms (for example, `linux-x64`, `osx-arm64`, or `win-x64`). As with other native extensions, binaries are platform-specific and need to be built accordingly.

## Build Your Own Extension in C\#

[DuckDB.ExtensionKit](https://github.com/Giorgi/DuckDB.ExtensionKit) is available as an open-source project on GitHub under the MIT license. The project includes example extensions that demonstrate how to define and build DuckDB extensions in C#. The repository contains a JWT-based example extension that showcases both scalar functions and table functions, as well as the full build and publishing workflow using .NET Native AOT.

Feedback, bug reports, and contributions are welcome through [GitHub issues](https://github.com/Giorgi/DuckDB.ExtensionKit/issues).

## Closing Thoughts

DuckDB’s extension mechanism has proven to be a flexible foundation for extending the system without complicating the core engine. DuckDB.ExtensionKit explores how this mechanism can be made accessible to a broader audience by leveraging the .NET ecosystem, while still producing native extensions that integrate directly with DuckDB.

Although C# is typically viewed as a high-level language, this project demonstrates that it can also be used to implement low-level, ABI-compatible components when needed. By combining modern C# features with DuckDB’s existing extension interface, it is possible to write extensions in a high-level language without giving up control over native boundaries.

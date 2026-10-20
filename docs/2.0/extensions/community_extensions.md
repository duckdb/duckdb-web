---
layout: docu
redirect_from:
- /docs/extensions/community_extensions
- /docs/stable/extensions/community_extensions
- /docs/current/extensions/community_extensions
- /docs/lts/extensions/community_extensions
- /docs/preview/extensions/community_extensions
title: Community Extensions
---

Community-contributed extensions can be installed from the Community Extensions repository since [summer 2024]({% post_url 2024-07-05-community-extensions %}).
Please visit the [“Community Extensions” section]({% link community_extensions/index.md %}) of the documentation for more details.

> Warning Community extensions are contributed by third parties. They are not written, audited, or maintained by DuckLabs, and they run with the same privileges as DuckDB itself. Signing proves only that an extension was built by the Community Extension CI, not that its code is safe. Install and load community extensions only if you trust their author and source. See the [security considerations]({% link community_extensions/index.md %}#security-considerations-for-using-community-extensions) for details.

> Deprecated Starting with DuckDB 2.0, community extensions are no longer built for the `osx_amd64` platform (macOS on Intel). DuckDB and its [core extensions]({% link docs/2.0/core_extensions/overview.md %}) are still available for `osx_amd64` in DuckDB 2.0, but DuckDB 2.1 will stop supporting this platform. See the [list of supported platforms]({% link docs/2.0/operations_manual/installing_duckdb/requirements.md %}#supported-platforms).

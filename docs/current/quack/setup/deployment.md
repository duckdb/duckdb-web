---
layout: docu
title: Deploying Quack
---

This page collects deployment recipes for running a public-facing Quack server. Today there is one recipe (AWS EC2), we will introduce more over time.

## On AWS EC2

The fastest way to get a public-facing Quack server is the one-click [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template maintained alongside the extension. It provisions a small EC2 instance running DuckDB, the quack extension behind nginx and Let's Encrypt TLS. As its output, it surfaces the per-instance token and connection URI.

### One-Click Launch

1. Open the [Launch Stack URL](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?templateURL=https://duckdb-quack-infra.s3.us-east-1.amazonaws.com/quack.yaml&stackName=quack-demo).
2. Click **Create stack** in the bottom right.
3. Wait about two minutes for `CREATE_COMPLETE`.
4. Open the stack's **Outputs** tab.
5. Click the `ConnectURL` value to open a [shell.duckdb.org](https://shell.duckdb.org) session pre-wired to the new instance, or copy `QuackURI` and `Token` to connect from a local DuckDB session (see below).

The stack defaults to a `t3.micro` instance; other sizes are selectable on the Parameters page when launching. Supported regions: `us-east-1`, `us-east-2`, `us-west-1`, `us-west-2`, `eu-west-1`, `eu-central-1`, `ap-northeast-1`, `ap-southeast-1`.

### Connecting from a Local DuckDB

Copy `QuackURI` and `Token` from the stack's Outputs tab and substitute below:

```sql
INSTALL quack FROM core_nightly;
LOAD quack;

-- Register the credentials once per session.
CREATE SECRET quack_credentials (
    TYPE quack,
    SCOPE '⟨uri⟩',                  -- e.g., 'quack:54.1.2.3.nip.io:443'
    TOKEN '⟨token⟩'
);

-- Who did I just launch?
FROM quack_query('⟨uri⟩', 'FROM whoami()');

-- Anything else you'd normally run, shipped verbatim to the remote.
FROM quack_query('⟨uri⟩', 'SELECT 1 + 1');
```

#### Sticky Session via `ATTACH`

`ATTACH` keeps server-side state (temp tables, `SET` variables) across calls, which `quack_query` alone does not.

```sql
ATTACH '⟨uri⟩' AS remote (TYPE quack);

-- Temp table lives on the remote.
FROM quack_query_by_name('remote', 'CREATE TEMP TABLE t AS SELECT range AS x FROM range(10)');
FROM quack_query_by_name('remote', 'SELECT sum(x) FROM t');

-- Session settings stick.
FROM quack_query_by_name('remote', 'SET threads = 8');
FROM quack_query_by_name('remote', 'SELECT current_setting(''threads'')');
```

### Tearing Down

When you're done with the instance, delete the stack:

```batch
aws cloudformation delete-stack --stack-name quack-demo --region us-east-1
```

Or use the **Delete** button in the CloudFormation console.

### What the Stack Provisions

* An `AWS::EC2::Instance` from a public AMI (per-region map baked into the template) running DuckDB, the quack extension behind nginx and the Let's Encrypt TLS.
* An `AWS::EC2::SecurityGroup` opening ports 80 (ACME challenge) and 443 (HTTPS).
* An `AWS::CloudFormation::WaitCondition` the instance signals once the RPC server is ready.
* CFN `Outputs` carrying the ready URI, per-instance token, and two shareable shell.duckdb.org URLs (`QueryURL`, `ConnectURL`).

### For Maintainers

The CloudFormation template, AMI baking process, and per-region AMI publishing live at [`duckdblabs/duckdb-quack-infra`](https://github.com/duckdblabs/duckdb-quack-infra). Updating the AMI or extending the supported region list happens there.

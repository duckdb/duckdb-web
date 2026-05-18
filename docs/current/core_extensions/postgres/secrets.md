---
layout: docu
redirect_from:
- /docs/preview/core_extensions/postgres/secrets
- /docs/stable/core_extensions/postgres/secrets
title: PostgreSQL Extension and the Secret Manager
---

User credentials and other PostgreSQL database connection details can be stored using the DuckDB [Secrets Manager]({% link docs/current/configuration/secrets_manager.md %}). The following syntax can be used to create a secret:

```sql
CREATE SECRET (
    TYPE postgres,
    HOST '127.0.0.1',
    PORT 5432,
    DATABASE postgres,
    USER 'postgres',
    PASSWORD ''
);
```

The information from the secret will be used when `ATTACH` is called. We can leave the PostgreSQL connection string empty to use all of the information stored in the secret.

```sql
ATTACH '' AS postgres_db (TYPE postgres);
```

We can use the PostgreSQL connection string to override individual options. For example, to connect to a different database while still using the same credentials, we can override only the database name in the following manner.

```sql
ATTACH 'dbname=my_other_db' AS postgres_db (TYPE postgres);
```

By default, created secrets are temporary. Secrets can be persisted using the [`CREATE PERSISTENT SECRET` command]({% link docs/current/configuration/secrets_manager.md %}#persistent-secrets). Persistent secrets can be used across sessions.

## Managing Multiple Secrets

Named secrets can be used to manage connections to multiple PostgreSQL database instances. Secrets can be given a name upon creation.

```sql
CREATE SECRET postgres_secret_one (
    TYPE postgres,
    HOST '127.0.0.1',
    PORT 5432,
    DATABASE postgres,
    USER 'postgres',
    PASSWORD ''
);
```

The secret can then be explicitly referenced using the `SECRET` parameter in the `ATTACH`.

```sql
ATTACH '' AS postgres_db_one (TYPE postgres, SECRET postgres_secret_one);
```

> Warning Avoid including credentials directly in the connection string. If a connection error occurs, the full connection string (including your credentials) may be printed to the terminal output. For better security, store credentials using DuckDB-managed secrets.

## Secret Configuration Options

Secrets of type `postgres` support a number of configuration options. The following options are named after the corresponding [connection options of libpq](https://www.postgresql.org/docs/18/libpq-connect.html#LIBPQ-PARAMKEYWORDS):

* `HOST`
* `HOSTADDR`
* `PORT`
* `DBNAME`
* `USER`
* `PASSWORD`
* `PASSFILE`
* `REQUIRE_AUTH`
* `CHANNEL_BINDING`
* `CONNECT_TIMEOUT`
* `CLIENT_ENCODING`
* `OPTIONS`
* `APPLICATION_NAME`
* `FALLBACK_APPLICATION_NAME`
* `KEEPALIVES`
* `KEEPALIVES_IDLE`
* `KEEPALIVES_INTERVAL`
* `KEEPALIVES_COUNT`
* `TCP_USER_TIMEOUT`
* `REPLICATION`
* `GSSENCMODE`
* `SSLMODE`
* `REQUIRESSL`
* `SSLNEGOTIATION`
* `SSLCOMPRESSION`
* `SSLCERT`
* `SSLKEY`
* `SSLKEYLOGFILE`
* `SSLPASSWORD`
* `SSLCERTMODE`
* `SSLROOTCERT`
* `SSLCRL`
* `SSLCRLDIR`
* `SSLSNI`
* `REQUIREPEER`
* `SSL_MIN_PROTOCOL_VERSION`
* `SSL_MAX_PROTOCOL_VERSION`
* `MIN_PROTOCOL_VERSION`
* `MAX_PROTOCOL_VERSION`
* `KRBSRVNAME`
* `GSSLIB`
* `GSSDELEGATION`
* `SCRAM_CLIENT_KEY`
* `SCRAM_SERVER_KEY`
* `SERVICE`
* `TARGET_SESSION_ATTRS`
* `LOAD_BALANCE_HOSTS`
* `OAUTH_ISSUER`
* `OAUTH_CLIENT_ID`
* `OAUTH_CLIENT_SECRET`
* `OAUTH_SCOPE`

 The following options are renamed to the corresponding keys:

* `DATABASE` – alias to `DBNAME`
* `HOSTNAME` – alias to `HOST`
* `USERNAME` – alias to `USER`

Instead of separate connection options, the full [connection URI](https://www.postgresql.org/docs/18/libpq-connect.html?utm_source=chatgpt.com#LIBPQ-CONNSTRING-URIS)
can be specified instead:

* `URI` – connection URI

Additional option is used for AWS RDS IAM authentication, see details in the next section below:

* `AWS_RDS_SECRET` – the name of the secret of type `rds`

## AWS RDS IAM Authentication

Managed PostgreSQL databases running on RDS/Aurora services allow to use [IAM authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html).
In that case the authentication token is generated using AWS SDK and must be refreshed every 15 minutes.

The `postgres` extension supports IAM authentication, when the password is not specified in the secret, but instead one of the configured AWS Credential Providers is used to generate the password, that is refreshed by the `postgres` extension automatically.

### Connecting with IAM Authentication from Command Line

> This section illustrates the process with `psql` utility, not with DuckDB. This method can be used to check the configuration before setting up DuckDB secrets.

When IAM authentication is performed using `psql` command line tool, the following are the AWS-recommended connection steps:

* Generate authentication token using `aws` CLI.
* Pass this token as a `password` connection option:

  ```bash
  export RDSHOST="database-1-instance-1.xxx.eu-west-1.rds.amazonaws.com" 
  psql "host=$RDSHOST port=5432 dbname=postgres user=postgres sslmode=require password=$(aws rds generate-db-auth-token --hostname $RDSHOST --port 5432 --username postgres --region eu-west-1)"
  ```

### Configuring Secrets for IAM Authentication

Authentication from the `postgres` extension uses the same logic as with `psql`:

* The secret of type `rds` is used to generate the authentication token, it takes the same configuration parameters as the `aws rds generate-db-auth-token` command in the example above:

  ```sql
  CREATE SECRET aws_rds_secret1 (
      TYPE rds,
      PROVIDER credential_chain,
      CHAIN 'env;sso;',
      REGION 'eu-west-1',
      RDS_USER 'postgres',
      RDS_HOST 'database-1-instance-1.xxxxxxxxxxxx.eu-west-1.rds.amazonaws.com',
      RDS_PORT '5432'
  );
  ```

* The secret of type `postgres` is used to create the remaining of the connection string. It takes the same parameters as the `psql` utility in the example above (and additionally any relevant additional `libpq` configuration options) and requires to specify the name of the `rds` secret, that is used to generate and periodically refresh (automatically) the authentication token that is passed to server as a `password`:

  ```sql
  CREATE SECRET pg_rds_secret1 (
      TYPE postgres,
      HOST 'database-1-instance-1.xxxxxxxxxxxx.eu-west-1.rds.amazonaws.com',
      PORT '5432',
      USER 'postgres',
      DATABASE 'postgres',
      SSLMODE require,
      AWS_RDS_SECRET aws_rds_secret1
  );
  ```

The secret of type `rds` requires the `aws` extension to be installed and allows to configure AWS Credential Chain the same way as with the secret of type `s3`, see details in the [AWS extension documentation]({% link docs/current/core_extensions/aws.md %}#credential_chain-provider).

## Storing Secrets inside a PostgreSQL Database

DuckDB [Secrets Manager]({% link docs/current/configuration/secrets_manager.md %}) supports pluggable Storage Providers.
The `postgres` extension implements storing the secrets (of any type) as records in the PostgreSQL database table.

The following example initializes the secrets storage and insers the secret into the `duckdb_secrets` table:

```sql
ATTACH 'postgres:' AS p1 (
    SECRET pg_rds_secret1,
    SECRET_STORAGE_TABLE duckdb_secrets
);

CREATE OR REPLACE SECRET s3_secret1 IN postgres_p1 (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN 'env;sso;',
    PROFILE 'DatabaseAdministrator-⟨account_id⟩',
    REGION 'eu-west-1'
);
```

When `IN postgres_⟨attached_database⟩`{:.language-sql .highlight} clause of `CREATE SECRET` is specified, the secret is persisted to the `duckdb_secrets` table in the specified attached database.

> Warning 
> Secrets are written to the database table in unencrypted binary format. It is advised to use this provider for secrets that do not include confidential credentials (like the `s3` example above). For multi-tenant scenarios it is expected that [Postgres Row-Level Security policies](https://www.postgresql.org/docs/18/ddl-rowsecurity.html) can be used to prevent users to see secrets of other users.

Different table name (for example, in a different schema) can be specified in the `SECRET_STORAGE_TABLE` parameter to the `ATTACH` command.

When the default `duckdb_secrets` table is used, it is not necessary to specify the `SECRET_STORAGE_TABLE` parameter.
When a PostgreSQL database is attached, the table with the default name `duckdb_secrets` is probed automatically. If it exists then the Secret Storage instance is registerd for this attached database making all the stored secrets available in the current session. This allows to use such persistent secrets with “direct attach” scenarios, when only a connection string is specified to the `duckdb` command (other DuckDB clients may require slightly different syntax):

```bash
duckdb postgres:postgresql://username:password@127.0.0.1:5432/db1
```

This method can also be used with [DuckLake](https://ducklake.select/) (with PostgreSQL catalog), when an S3/object storage access secret is stored in the catalog database:

```bash
duckdb ducklake:postgres:postgresql://username:password@127.0.0.1:5432/db1
```

Secrets the are stored in the specific attached database can be listed using the following query:

```sql
FROM duckdb_secrets() WHERE storage = 'postgres_⟨attached_database⟩';
```

To disable the PostgreSQL Secret Storage completely pass the empty string `''` in the `SECRET_STORAGE_TABLE` parameter.

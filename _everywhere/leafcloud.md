---
layout: post
title: "DuckLake on Leafcloud"
date: 2026-03-07
author: "Gábor Szárnyas"
thumb: "/images/everywhere/thumbs/leafcloud.jpg"
image: "/images/everywhere/thumbs/leafcloud.jpg"
excerpt: ""
tags: ["Servers"]
thirdparty: false
---

This tutorial is an adaptation of [“Public DuckLake on Object Storage”](https://ducklake.select/docs/stable/duckdb/guides/public_ducklake_on_object_storage) to the object storage of [Leafcloud](https://leaf.cloud/), an Amsterdam-based cloud provider.

## Setting Up the Object Store

1. Navigate to the [Leafcloud dashboard](https://create.leaf.cloud/).

2. Go to **Object Store**, **Containers** and create a new container. We'll use the name `ducklake-storage`.

3. Tick the checkbox for **Public Access** and copy the link. This will be e.g. the following:

   ```text
   https://leafcloud.store/swift/v1/AUTH_f84982a3c5d04bd0846197d8e8ce3ddd/ducklake-storage
   ```

## Setting Up the OpenStackClient

1. Fetch the credentials from Leafcloud. Navigate to your username in the top right corner, **Settings**, **Identity**, **Application Credentials**, or simply visit <https://create.leaf.cloud/identity/application_credentials/>.

2. Select **Create Application Credential** and download the resulting `app-cred-<your_credential_name>-cred-openrc.sh` and `clouds.yaml` files.

3. Source the credentials in your shell to configure the environment variables:

   ```batch
   source app-cred-<your_credential_name>-cred-openrc.sh
   ```

4. Install OpenStackClient in your favorite Python environment:

   ```batch
   pip install python-openstackclient
   ```

5. Create the credentials for the bucket:

   ```batch
   openstack ec2 credentials create
   ```

6. This will print something like this:

   ```text
   +------------+----------------------------------+
   | Field      | Value                            |
   +------------+----------------------------------+
   | access     | <32-character hexadecimal value> |
   | links      | {'self': '...'}                  |
   | project_id | <32-character hexadecimal value> |
   | secret     | <32-character hexadecimal value> |
   | trust_id   | None                             |
   | user_id    | <32-character hexadecimal value> |
   +------------+----------------------------------+
   ```

7. Save the printed credentials.

## Setting Up Rclone

1. Install [Rclone](https://rclone.org/).

2. Initiate the setup with `rclone config` and add a new remote. We'll name it `lc`.

3. Select **Amazon S3 Compliant Storage Providers** (`s3`), **Any other S3 compatible provider** (`other`).

4. Set the `access_key_id` to the `access` field's value from the table above.

5. Set the `secret_access_key` to the `secret` field's value.

6. Edit the `~/.config/rclone/rclone.conf` manually and set the endpoint to `https://leafcloud.store`.

7. The entry in `rclone.conf` will look like this:

   ```ini
   [lc]
   type = s3
   provider = Other
   access_key_id = <32-character hexadecimal value>
   secret_access_key = <32-character hexadecimal value>
   endpoint = https://leafcloud.store
   ```

## Creating a DuckLake

1. Create a directory called `ducklake-storage` and navigate to this directory.

2. Create a DuckLake following the [“Using a Remote Data Path” DuckLake guide](https://ducklake.select/docs/stable/duckdb/guides/using_a_remote_data_path).

3. When specifying the `DATA_PATH`, use the previously obtained path `https://leafcloud.store/.../ducklake-storage`.

4. Synchronize the DuckLake to the object storage as follows: 

   ```batch
   rclone sync ducklake-storage lc:ducklake-storage
   ```

## Testing

1. Connect to the DuckLake as follows:

   ```batch
   duckdb ducklake:https://leafcloud.store/swift/v1/AUTH_f84982a3c5d04bd0846197d8e8ce3ddd/ducklake-storage/sf1.ducklake
   ```

2. List the tables with `.tables`. This will list a mix of data tables and metadata tables:

   ```text
   D .tables
   Comment                                ducklake_column_tag
   Comment_hasTag_Tag                     ducklake_data_file
   ...
   ```

3. Run any SQL query you like:

   ```sql
   SELECT firstName FROM person LIMIT 1;
   ```

   ```text
   ┌───────────┐
   │ firstName │
   │  varchar  │
   ├───────────┤
   │ Jun       │
   └───────────┘
   ```

## Future Work

Leafcloud's website states that a [managed database service is coming soon](https://leaf.cloud/managed/databases). This could be used to set up DuckLake with Postgres for multi-writer DuckDB.

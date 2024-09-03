<p align="center">
  <img src="https://raw.githubusercontent.com/dbt-labs/dbt/ec7dee39f793aa4f7dd3dae37282cc87664813e4/etc/dbt-logo-full.svg" alt="dbt logo" width="500"/>
</p>

**[dbt](https://www.getdbt.com/)** enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.

dbt is the T in ELT. Organize, cleanse, denormalize, filter, rename, and pre-aggregate the raw data in your warehouse so that it's ready for analysis.

## dbt-greenplum

The `dbt-greenplum` package contains the code enabling dbt to work with Greenplum. For more information on using dbt with Greenplum, consult [the docs](https://docs.getdbt.com/docs/profile-greenplum).

This adapter is based on [dbt-postgres](https://github.com/dbt-labs/dbt-postgres) **v1.8.2**.

Compared to [dbt-postgres](https://github.com/dbt-labs/dbt-postgres), dbt-greenplum supports some Greenplum-Specific features.

For those Greenplum-Specific features, we reference [markporoshin/dbt-greenplum](https://github.com/markporoshin/dbt-greenplum) which is no longer maintained.

### Greenplum-Specific Features

#### Distribution Policy
  
  Greenplum will choose the first column as the distribution column by default while not specifying distribution policy.
  
  You can specify distribution policy explicitly with the following settings.

  - distributed randomly by setting `distributed_randomly=true` in the model config.
  - distributed replicated by setting `distributed_replicated=true` in the model config.
  - distributed by (<column_name> [, ... ]) by setting `distributed_by='<column_name> [, ... ]'` in the model config.

#### Table Storage Model
  - Heap Storage(Default)
  
    You can create heap table with the setting `appendoptimized=false` in the model config.
  
    Here is an example.
    ```SQL
    {{
      config(
        ...
        materialized='table',
        appendoptimized=false,
        ...
      )
    }}

    select 1 as "id"
    ```
 
  - Append-Optimized Storage

    You can create Append-Optimized(AO) table with the setting `appendoptimized=true` in the model config.
  - Row or Column-Oriented Storage

    - Row-Oriented Storage

      Row-oriented storage is used by default.

      Also you can create table with row-oriented storage by setting `orientation=row` in the model config explicitly.

    - Column-Oriented Storage (Append-Optimized Tables Only)

      You can create table with column-oriented storage by setting `orientation=column` in the model config.

      **NOTE: Tables that use column-oriented storage must be append-optimized tables.**

  - Using Compression (Append-Optimized Tables Only)

    You can specify `compresstype`, `level` and `blocksize` settings in the model config.

    Default values are `compresstype=ZLIB`, `compresslevel=1` and `blocksize=32768`.

    **NOTE: Only append-optimized tables can use compression.**

#### Partition Tables

  Greenplum can **NOT** create partition tables with create table as statement.
  
  So to build model with partitions, you need to two steps.
  - create table
  - insert data

  To build model with partitions, we need to configure
  - `fields_string` - definition of columns name, type and constraints
    
    This setting is **must**.

  - one of following way to configure partitions

    - Way 1: using the setting `raw_partition`
      
      Here is an example.
      ```SQL
      {% set fields_string %}
         id int4 null,
         incomingdate timestamp NULL
      {% endset %}

      {% set raw_partition %}
        PARTITION BY RANGE (incomingdate)
        (
          START ('2021-01-01'::timestamp) INCLUSIVE
          END ('2023-01-01'::timestamp) EXCLUSIVE
          EVERY (INTERVAL '1 day'),
          DEFAULT PARTITION extra
        )
      {% endset %}

      {{
        config(
          materialized='table',
          fields_string=fields_string,
          raw_partition=raw_partition,
        )
      }}

      with source_data as (

          select
              1 as id,
              '2022-02-22'::timestamp as incomingdate
          union all
          select
              null as id,
              '2022-02-25'::timestamp as incomingdate
      )
      select *
      from source_data
      ```
      The generated SQL by dbt is as follows. (We mock the model name using <model_identifier>.)
      ```SQL
      create table if not exists <model_identifier> (
         id int4 null,
         incomingdate timestamp NULL
      )
      PARTITION BY RANGE (incomingdate)
      (
         START ('2021-01-01'::timestamp) INCLUSIVE
          END ('2023-01-01'::timestamp) EXCLUSIVE
          EVERY (INTERVAL '1 day'),
          DEFAULT PARTITION extra
      );
    
      insert into <model_identifier> (
      with source_data as (
          select
              1 as id,
              '2022-02-22'::timestamp as incomingdate
          union all
          select
              null as id,
              '2022-02-25'::timestamp as incomingdate
      )
      select *
      from source_data
      );
      ```
    - Way 2: using the settings `partition_type`, `partition_column`, `partition_spec`
      
      Here is an example.
      ```SQL
      {% set fields_string %}
          id int4 null,
          incomingdate timestamp NULL
      {% endset %}

      {%- set partition_type = 'RANGE' -%}
      {%- set partition_column = 'incomingdate' -%}
      {% set partition_spec %}
          START ('2021-01-01'::timestamp) INCLUSIVE
          END ('2023-01-01'::timestamp) EXCLUSIVE
          EVERY (INTERVAL '1 day'),
          DEFAULT PARTITION extra
      {% endset %}

      {{
          config(
              materialized='table',
              fields_string=fields_string,
              partition_type=partition_type,
              partition_column=partition_column,
              partition_spec=partition_spec,
          )
      }}

      with source_data as (

          select
              1 as id,
              '2022-02-22'::timestamp as incomingdate
          union all
          select
              null as id,
              '2022-02-25'::timestamp as incomingdate
      )
      select *
      from source_data
      ```
      Generated SQL by dbt is same as Way 1.    
    - Way 3: using the settings `partition_type`, `partition_column`, `partition_start`, `partition_end`, `partition_every`

      Here is an example.
      ```SQL
      {% set fields_string %}
          id int4 null,
          incomingdate timestamp NULL
      {% endset %}

      {%- set partition_type = 'RANGE' -%} 
      {%- set partition_column = 'incomingdate' -%}
      {%- set partition_start = "'2021-01-01'::timestamp" -%}
      {%- set partition_end = "'2023-01-01'::timestamp" -%}
      {%- set partition_every = '1 day' -%}

      {{
          config(
              materialized='table',
              fields_string=fields_string,
              partition_type=partition_type,
              partition_column=partition_column,
              partition_start=partition_start,
              partition_end=partition_end,
              partition_every=partition_every,
              default_partition_name='extra'
           )
      }}

      with source_data as (

          select
              1 as id,
              '2022-02-22'::timestamp as incomingdate
          union all
          select
              null as id,
              '2022-02-25'::timestamp as incomingdate
      )
      select *
      from source_data
      ```
      Generated SQL by dbt is same as Way 1.
    - Way 4: using the settings `partition_type`, `partition_column`, `partition_values`
    
      Here is an example.
      ```SQL
      {% set fields_string %}
          id int4 null,
          incomingdate timestamp NULL
      {% endset %}

      {%- set partition_type = 'LIST' -%}
      {%- set partition_column = 'code' -%}
      {% set partition_values %}
          PARTITION sales VALUES ('S'),
          PARTITION returns VALUES ('R')
      {% endset %}
      
      {{
          config(
              materialized='table',
              fields_string=fields_string,
              partition_type=partition_type,
              partition_column=partition_column,
              partition_values=partition_values,
              default_partition_name='extra'
          )
      }}
      
      with source_data as (
      
          select
              1 as id,
              'S' as code
          union all
          select
              null as id,
              'N' as code
      )
      select *
      from source_data
      ```
      Generated SQL by dbt is as follows.
      ```SQL
      create table if not exists <model_identifier> (
          id int4 null,
          code char(1)
      )
      PARTITION BY LIST (code)
          (
              PARTITION sales VALUES ('S'),
              PARTITION returns VALUES ('R'),
              DEFAULT PARTITION extra
          )
      ;
      
      insert into <model_identifier> (
      with source_data as (
          select
              1 as id,
              'S' as code
          union all
          select
              null as id,
              'N' as code
      )
      select *
      from source_data
      );
      ```
  - `default_partition_name` - name of default partition, default value is `other`

#### Incremental Strategy

  Valid incremental strategies are `append`, `delete+insert` and `truncate+insert`.
  

## Getting started

- [Install dbt](https://docs.getdbt.com/docs/installation)
- Read the [introduction](https://docs.getdbt.com/docs/introduction/) and [viewpoint](https://docs.getdbt.com/docs/about/viewpoint/)

## Join the dbt Community

- Be part of the conversation in the [dbt Community Slack](http://community.getdbt.com/)
- Read more on the [dbt Community Discourse](https://discourse.getdbt.com)

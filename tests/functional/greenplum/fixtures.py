models__heap_sql = """
{{
    config(
        materialized='table',
        distributed_by='id',
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""

models__ao_sql = """
{{
    config(
        materialized='table',
        distributed_by='id',
        appendoptimized=true,
        orientation='column',
        compresstype='ZLIB',
        compresslevel=1,
        blocksize=32768        
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""

models__default_distribution_sql = """
{{
    config(
        materialized='table',
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""

models__distributed_by_sql = """
{{
    config(
        materialized='table',
        distributed_by='id, name',
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id, 'aaa' as name 
    union all
    select null as id, 'xxx' as name

)

select *
from source_data
"""

models__distributed_replicated_sql = """
{{
    config(
        materialized='table',
        distributed_replicated=true,
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""

models__distributed_randomly_sql = """
{{
    config(
        materialized='table',
        distributed_randomly=true,
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""

models__partition_syntax1_sql = """
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
"""

models__partition_syntax2_sql = """
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
"""

models__partition_syntax3_sql = """
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
"""

models__partition_syntax4_sql = """
{% set fields_string %}
    id int4 null,
    code char(1)
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
"""

models__dry_run_sql = """
{{
    config(
        materialized='table',
        distributed_by='id',
        appendoptimized=false
    )
}}

select * from {{ ref('heap') }}
"""

models__incremental_default_sql = """
{{
    config(
        materialized='incremental',
        distributed_by='id',
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""

models__incremental_delete_insert_sql = """
{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        distributed_by='id',
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""

models__incremental_truncate_insert_sql = """
{{
    config(
        materialized='incremental',
        incremental_strategy='truncate+insert',
        distributed_by='id',
        appendoptimized=false
    )
}}

with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data
"""
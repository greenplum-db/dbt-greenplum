{% macro greenplum__create_table_as(temporary, relation, sql) -%}
  {%- set unlogged = config.get('unlogged', default=false) -%}
  {%- set sql_header = config.get('sql_header', none) -%}


  {# Greenplum specific #}
  {%- set distributed_replicated = config.get('distributed_replicated', default=false) -%}
  {%- set distributed_randomly = config.get('distributed_randomly', default=false) -%}  
  {%- set distributed_by = config.get('distributed_by', none) -%}
  {%- set appendonly = config.get('appendonly', default=false) -%}
  {%- set appendoptimized = config.get('appendoptimized', default=appendonly) -%}
  {%- set orientation = config.get('orientation', default='column') -%}
  {%- set compresstype = config.get('compresstype', default='ZSTD') -%}
  {%- set compresslevel = config.get('compresslevel', default=4) -%}
  {%- set blocksize = config.get('blocksize', default=32768) -%}

  {% set partition_spec = config.get('partition_spec', none) %}

  {%- set raw_partition = config.get('raw_partition', none) -%}
  {%- set fields_string = config.get('fields_string', none) -%}

  {%- set default_partition_name = config.get('default_partition_name', default='other') -%}
  {%- set partition_type = config.get('partition_type', none) -%}
  {%- set partition_column = config.get('partition_column', none) -%}
  {%- set partition_start = config.get('partition_start', none) -%}
  {%- set partition_end = config.get('partition_end', none) -%}
  {%- set partition_every = config.get('partition_every', none) -%}
  {%- set partition_values = config.get('partition_values', none) -%}

  {%- set is_partition = raw_partition is not none or partition_type is not none -%}

  {{ sql_header if sql_header is not none }}

  {% if is_partition and not temporary %}

    {# CREATING TABLE #}
    create table if not exists {{ relation }} (
        {{ fields_string }}
    )
    {{ storage_parameters(appendoptimized, blocksize, orientation, compresstype, compresslevel) }}
    {{ distribution(distributed_by, distributed_randomly, distributed_replicated) }}
    {{ partitions(raw_partition, partition_type, partition_column,
                  default_partition_name, partition_start, partition_end,
                  partition_every, partition_values, partition_spec) }}
    ;

    {# INSERTING DATA #}
    insert into {{ relation }} (
        {{ sql }}
    );

  {% else %}
    create {% if temporary -%}
      temporary
    {%- elif unlogged -%}
      unlogged
    {%- endif %} table {{ relation }}
      {{ storage_parameters(appendoptimized, blocksize, orientation, compresstype, compresslevel) }}
    {% set contract_config = config.get('contract') %}
    {% if contract_config.enforced %}
      {{ get_assert_columns_equivalent(sql) }}
    {% endif -%}
    {% if contract_config.enforced and (not temporary) -%}
        {{ get_table_columns_and_constraints() }} ;
      insert into {{ relation }} (
        {{ adapter.dispatch('get_column_names', 'dbt')() }}
      )
      {%- set sql = get_select_subquery(sql) %}
    {% else %}
      as
    {% endif %}
    (
      {{ sql }}
    )
    {{ distribution(distributed_by, distributed_randomly, distributed_replicated) }}
    ;
  {% endif %}

{%- endmacro %}

{% macro greenplum__get_create_index_sql(relation, index_dict) -%}
  {%- set index_config = adapter.parse_index(index_dict) -%}
  {%- set comma_separated_columns = ", ".join(index_config.columns) -%}
  {%- set index_name = index_config.render(relation) -%}

  create {% if index_config.unique -%}
    unique
  {%- endif %} index
  "{{ index_name }}"
  on {{ relation }} {% if index_config.type -%}
    using {{ index_config.type }}
  {%- endif %}
  ({{ comma_separated_columns }})
{%- endmacro %}

{% macro greenplum__create_schema(relation) -%}
  {{ return(postgres__create_schema(relation)) }}
{% endmacro %}

{% macro greenplum__drop_schema(relation) -%}
  {{ return(postgres__drop_schema(relation)) }}
{% endmacro %}

{% macro greenplum__get_columns_in_relation(relation) -%}
  {{ return(postgres__get_columns_in_relation(relation)) }}
{% endmacro %}


{% macro greenplum__list_relations_without_caching(schema_relation) %}
  {{ return(postgres__list_relations_without_caching(schema_relation)) }}
{% endmacro %}

{% macro greenplum__information_schema_name(database) -%}
  {{ return(postgres__information_schema_name(database)) }}
{%- endmacro %}

{% macro greenplum__list_schemas(database) %}
  {{ return(postgres__list_schemas(database)) }}
{% endmacro %}

{% macro greenplum__check_schema_exists(information_schema, schema) -%}
  {{ return(postgres__check_schema_exists(information_schema, schema)) }}
{% endmacro %}

{% macro greenplum__make_relation_with_suffix(base_relation, suffix, dstring) %}
  {{ return(postgres__make_relation_with_suffix(base_relation, suffix, dstring)) }}
{% endmacro %}

{% macro greenplum__make_intermediate_relation(base_relation, suffix) %}
  {{ return(postgres__make_intermediate_relation(base_relation, suffix)) }}
{% endmacro %}

{% macro greenplum__make_temp_relation(base_relation, suffix) %}
  {{ return(postgres__make_temp_relation(base_relation, suffix)) }}
{% endmacro %}

{% macro greenplum__make_backup_relation(base_relation, backup_relation_type, suffix) %}
  {{ return(postgres__make_backup_relation(base_relation, backup_relation_type, suffix)) }}
{% endmacro %}

{% macro greenplum_escape_comment(comment) -%}
  {{ return(postgres_escape_comment(comment)) }}
{%- endmacro %}


{% macro greenplum__alter_relation_comment(relation, comment) %}
  {{ return(postgres__alter_relation_comment(relation, comment)) }}
{% endmacro %}


{% macro greenplum__alter_column_comment(relation, column_dict) %}
  {{ return(postgres__alter_column_comment(relation, column_dict)) }}
{% endmacro %}

{%- macro greenplum__get_show_grant_sql(relation) -%}
  {{ return(postgres__get_show_grant_sql(relation)) }}
{%- endmacro -%}

{% macro greenplum__copy_grants() %}
  {{ return(postgres__copy_grants()) }}
{% endmacro %}


{% macro greenplum__get_show_indexes_sql(relation) %}
  {{ return(postgres__get_show_indexes_sql(relation)) }}
{% endmacro %}


{%- macro greenplum__get_drop_index_sql(relation, index_name) -%}
  {{ return(postgres__get_drop_index_sql(relation, index_name)) }}
{%- endmacro -%}

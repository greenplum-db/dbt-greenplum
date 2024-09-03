{% macro greenplum__current_timestamp() -%}
    {{ return(postgres__current_timestamp()) }}
{%- endmacro %}

{% macro greenplum__snapshot_string_as_time(timestamp) -%}
    {{ return(postgres__snapshot_string_as_time(timestamp)) }}
{%- endmacro %}

{% macro greenplum__snapshot_get_time() -%}
    {{ return(postgres__snapshot_get_time()) }}
{%- endmacro %}

{% macro greenplum__current_timestamp_backcompat() %}
    {{ return(postgres__current_timestamp_backcompat()) }}
{% endmacro %}

{% macro greenplum__current_timestamp_in_utc_backcompat() %}
    {{ return(postgres__current_timestamp_in_utc_backcompat()) }}
{% endmacro %}

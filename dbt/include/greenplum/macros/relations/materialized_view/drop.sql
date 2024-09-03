{% macro greenplum__drop_materialized_view(relation) -%}
    {{ return(postgres__drop_materialized_view(relation)) }}
{%- endmacro %}

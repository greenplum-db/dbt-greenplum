{% macro greenplum__get_replace_view_sql(relation, sql) -%}
    {{ return(postgres__get_replace_view_sql(relation, sql)) }}
{%- endmacro %}

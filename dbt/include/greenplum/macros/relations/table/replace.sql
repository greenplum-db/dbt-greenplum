{% macro greenplum__get_replace_table_sql(relation, sql) -%}
    {{ return(postgres__get_replace_table_sql(relation, sql)) }}
{%- endmacro %}

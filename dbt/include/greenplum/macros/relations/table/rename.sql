{% macro greenplum__get_rename_table_sql(relation, new_name) %}
    {{ return(postgres__get_rename_table_sql(relation, new_name)) }}
{% endmacro %}

{% macro greenplum__get_rename_view_sql(relation, new_name) %}
    {{ return(postgres__get_rename_view_sql(relation, new_name)) }}
{% endmacro %}

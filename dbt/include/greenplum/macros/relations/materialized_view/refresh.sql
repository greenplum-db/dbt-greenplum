{% macro greenplum__refresh_materialized_view(relation) %}
    {{ return(postgres__refresh_materialized_view(relation)) }}
{% endmacro %}

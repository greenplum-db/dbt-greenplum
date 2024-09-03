{% macro greenplum__describe_materialized_view(relation) %}
    {{ return(postgres__describe_materialized_view(relation)) }}
{% endmacro %}

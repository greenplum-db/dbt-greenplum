{% macro greenplum__any_value(expression) -%}
    {{ return(postgres__any_value(expression)) }}
{%- endmacro %}

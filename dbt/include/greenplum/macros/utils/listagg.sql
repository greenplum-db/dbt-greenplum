{% macro greenplum__listagg(measure, delimiter_text, order_by_clause, limit_num) -%}
    {{ return(postgres__listagg(measure, delimiter_text, order_by_clause, limit_num)) }}
{%- endmacro %}

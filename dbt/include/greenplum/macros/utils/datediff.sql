{% macro greenplum__datediff(first_date, second_date, datepart) -%}
    {{ return(postgres__datediff(first_date, second_date, datepart)) }}
{%- endmacro %}

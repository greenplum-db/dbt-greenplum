{% macro greenplum__last_day(date, datepart) -%}
    {{ return(postgres__last_day(date, datepart)) }}
{%- endmacro %}

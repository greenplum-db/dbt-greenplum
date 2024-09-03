{% macro greenplum__dateadd(datepart, interval, from_date_or_timestamp) %}
    {{ return(postgres__dateadd(datepart, interval, from_date_or_timestamp)) }}
{% endmacro %}

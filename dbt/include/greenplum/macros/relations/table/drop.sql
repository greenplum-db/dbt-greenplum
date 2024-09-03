{% macro greenplum__drop_table(relation) -%}
    {{ return(postgres__drop_table(relation)) }}
{%- endmacro %}

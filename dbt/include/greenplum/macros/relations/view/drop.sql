{% macro greenplum__drop_view(relation) -%}
    {{ return(postgres__drop_view(relation)) }}
{%- endmacro %}

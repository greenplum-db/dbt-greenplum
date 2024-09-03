{% macro greenplum__get_catalog_relations(information_schema, relations) -%}
  {{ return(postgres__get_catalog_relations(information_schema, relations) )}}
{%- endmacro %}


{% macro greenplum__get_catalog(information_schema, schemas) -%}
  {{ return(postgres__get_catalog(information_schema, schemas)) }}
{%- endmacro %}

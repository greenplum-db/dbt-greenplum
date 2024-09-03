{% macro greenplum__split_part(string_text, delimiter_text, part_number) %}
  {{ return(postgres__split_part(string_text, delimiter_text, part_number)) }}
{% endmacro %}

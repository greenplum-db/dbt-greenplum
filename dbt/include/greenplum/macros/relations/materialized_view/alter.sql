{% macro greenplum__get_alter_materialized_view_as_sql(
    relation,
    configuration_changes,
    sql,
    existing_relation,
    backup_relation,
    intermediate_relation
) %}

    -- apply a full refresh immediately if needed
    {% if configuration_changes.requires_full_refresh %}

        {{ get_replace_sql(existing_relation, relation, sql) }}

    -- otherwise apply individual changes as needed
    {% else %}

        {{ greenplum__update_indexes_on_materialized_view(relation, configuration_changes.indexes) }}

    {%- endif -%}

{% endmacro %}

{%- macro greenplum__update_indexes_on_materialized_view(relation, index_changes) -%}
    {{- log("Applying UPDATE INDEXES to: " ~ relation) -}}

    {%- for _index_change in index_changes -%}
        {%- set _index = _index_change.context -%}

        {%- if _index_change.action == "drop" -%}

            {{ postgres__get_drop_index_sql(relation, _index.name) }}

        {%- elif _index_change.action == "create" -%}

            {{ greenplum__get_create_index_sql(relation, _index.as_node_config) }}

        {%- endif -%}
	{{ ';' if not loop.last else "" }}

    {%- endfor -%}

{%- endmacro -%}


{% macro greenplum__get_materialized_view_configuration_changes(existing_relation, new_config) %}
    {{ return(postgres__get_materialized_view_configuration_changes(existing_relation, new_config)) }}
{% endmacro %}

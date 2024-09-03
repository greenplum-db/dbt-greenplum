wrong_specification_block__schema_yml = """
version: 2
models:
  - name: some_seed
    description: "This is my seed under a model"
"""

test_context_where_subq_models__schema_yml = """
version: 2

models:
  - name: model_a
    data_tests:
      - self_referential

"""

test_context_where_subq_models__model_a_sql = """
select 1 as fun

"""

test_utils__dbt_project_yml = """
name: 'test_utils'
version: '1.0'
config-version: 2

profile: 'default'

macro-paths: ["macros"]


"""

test_utils__macros__current_timestamp_sql = """
{% macro current_timestamp() -%}
  {{ return(adapter.dispatch('current_timestamp', 'test_utils')()) }}
{%- endmacro %}

{% macro default__current_timestamp() -%}
  now()
{%- endmacro %}

"""

test_utils__macros__custom_test_sql = """
{% macro test_dispatch(model) -%}
  {{ return(adapter.dispatch('test_dispatch', macro_namespace = 'test_utils')()) }}
{%- endmacro %}

{% macro default__test_dispatch(model) %}
    select {{ adapter.dispatch('current_timestamp', macro_namespace = 'test_utils')() }}
{% endmacro %}

"""

local_dependency__dbt_project_yml = """
name: 'local_dep'
version: '1.0'
config-version: 2

profile: 'default'

macro-paths: ["macros"]

"""

local_dependency__macros__equality_sql = """
{#-- taken from dbt-utils --#}
{% test equality(model, compare_model, compare_columns=None) %}
  {{ return(adapter.dispatch('test_equality')(model, compare_model, compare_columns)) }}
{% endtest %}

{% macro default__test_equality(model, compare_model, compare_columns=None) %}

{% set set_diff %}
    count(*) + abs(
        sum(case when which_diff = 'a_minus_b' then 1 else 0 end) -
        sum(case when which_diff = 'b_minus_a' then 1 else 0 end)
    )
{% endset %}

{#-- Needs to be set at parse time, before we return '' below --#}
{{ config(fail_calc = set_diff) }}

{#-- Prevent querying of db in parsing mode. This works because this macro does not create any new refs. #}
{%- if not execute -%}
    {{ return('') }}
{% endif %}
-- setup
{%- do dbt_utils._is_relation(model, 'test_equality') -%}
{#-
If the compare_cols arg is provided, we can run this test without querying the
information schema — this allows the model to be an ephemeral model
-#}

{%- if not compare_columns -%}
    {%- do dbt_utils._is_ephemeral(model, 'test_equality') -%}
    {%- set compare_columns = adapter.get_columns_in_relation(model) | map(attribute='quoted') -%}
{%- endif -%}

{% set compare_cols_csv = compare_columns | join(', ') %}

with a as (
    select * from {{ model }}
),
b as (
    select * from {{ compare_model }}
),
a_minus_b as (
    select {{compare_cols_csv}} from a
    {{ dbt_utils.except() }}
    select {{compare_cols_csv}} from b
),
b_minus_a as (
    select {{compare_cols_csv}} from b
    {{ dbt_utils.except() }}
    select {{compare_cols_csv}} from a
),

unioned as (

    select 'a_minus_b' as which_diff, * from a_minus_b
    union all
    select 'b_minus_a' as which_diff, * from b_minus_a

)

select * from unioned

{% endmacro %}

"""

case_sensitive_models__schema_yml = """
version: 2

models:
  - name: lowercase
    columns:
      - name: id
        quote: true
        data_tests:
          - unique
  - name: uppercase
    columns:
      - name: id
        quote: true
        data_tests:
          - unique

"""

case_sensitive_models__uppercase_SQL = """
select 1 as id

"""

case_sensitive_models__lowercase_sql = """
select 1 as id

"""

test_context_macros__my_test_sql = """
{% macro test_call_pkg_macro(model) %}
    select {{ adapter.dispatch('current_timestamp', macro_namespace = 'local_utils')() }}
{% endmacro %}

"""

test_context_macros__test_my_datediff_sql = """
{% macro test_my_datediff(model) %}
    select {{ local_utils.datediff() }}
{% endmacro %}

"""

test_context_macros__custom_schema_tests_sql = """
{% test type_one(model) %}

    select * from (

        select * from {{ model }}
        union all
        select * from {{ ref('model_b') }}

    ) as Foo

{% endtest %}

{% test type_two(model) %}

    {{ config(severity = "WARN") }}

    select * from {{ model }}

{% endtest %}

"""

test_context_models_namespaced__schema_yml = """

version: 2

models:
    - name: model_a
      data_tests:
        - type_one
        - type_two
    - name: model_c
      data_tests:
        - call_pkg_macro
        - test_utils.dispatch

"""

test_context_models_namespaced__model_c_sql = """
select 1 as fun

"""

test_context_models_namespaced__model_b_sql = """
select 1 as notfun

"""

test_context_models_namespaced__model_a_sql = """
select 1 as fun

"""

macros_v2__override_get_test_macros_fail__get_test_sql_sql = """
{% macro get_test_sql(main_sql, fail_calc, warn_if, error_if, limit) -%}
    select
      {{ fail_calc }} as failures,
      case when {{ fail_calc }} {{ warn_if }} then 'x' else 'y' end as should_warn,
      case when {{ fail_calc }} {{ error_if }} then 'x' else 'y' end as should_error
    from (
      {{ main_sql }}
      {{ "limit " ~ limit if limit != none }}
    ) dbt_internal_test
{% endmacro %}
"""

macros_v2__macros__tests_sql = """
{% test every_value_is_blue(model, column_name) %}

    select *
    from {{ model }}
    where {{ column_name }} != 'blue'

{% endtest %}


{% test rejected_values(model, column_name, values) %}

    select *
    from {{ model }}
    where {{ column_name }} in (
        {% for value in values %}
            '{{ value }}' {% if not loop.last %} , {% endif %}
        {% endfor %}
    )

{% endtest %}


{% test equivalent(model, value) %}
    {% set expected = 'foo-bar' %}
    {% set eq = 1 if value == expected else 0 %}
    {% set validation_message -%}
      'got "{{ value }}", expected "{{ expected }}"'
    {%- endset %}
    {% if eq == 0 and execute %}
        {{ log(validation_message, info=True) }}
    {% endif %}

    select {{ validation_message }} as validation_error
    where {{ eq }} = 0
{% endtest %}


"""

macros_v2__override_get_test_macros__get_test_sql_sql = """
{% macro get_test_sql(main_sql, fail_calc, warn_if, error_if, limit) -%}
    select
      {{ fail_calc }} as failures,
      case when {{ fail_calc }} {{ warn_if }} then 1 else 0 end as should_warn,
      case when {{ fail_calc }} {{ error_if }} then 1 else 0 end as should_error
    from (
      {{ main_sql }}
      {{ "limit " ~ limit if limit != none }}
    ) dbt_internal_test
{%- endmacro %}
"""

macros_v2__custom_configs__test_sql = """
{% test where(model, column_name) %}
  {{ config(where = "1 = 0") }}
  select * from {{ model }}
{% endtest %}

{% test error_if(model, column_name) %}
  {{ config(error_if = "<= 0", warn_if = "<= 0") }}
  select * from {{ model }}
{% endtest %}


{% test warn_if(model, column_name) %}
  {{ config(warn_if = "<= 0", severity = "WARN") }}
  select * from {{ model }}
{% endtest %}

{% test limit(model, column_name) %}
  {{ config(limit = 0) }}
  select * from {{ model }}
{% endtest %}

{% test fail_calc(model, column_name) %}
  {{ config(fail_calc = "count(*) - count(*)") }}
  select * from {{ model }}
{% endtest %}

"""

test_context_macros_namespaced__my_test_sql = """
{% macro test_call_pkg_macro(model) %}
    select {{ test_utils.current_timestamp() }}
{% endmacro %}

"""

test_context_macros_namespaced__custom_schema_tests_sql = """
{% test type_one(model) %}

    select * from (

        select * from {{ model }}
        union all
        select * from {{ ref('model_b') }}

    ) as Foo

{% endtest %}

{% test type_two(model) %}

    {{ config(severity = "WARN") }}

    select * from {{ model }}

{% endtest %}

"""

seeds__some_seed_csv = """
col_int,col_str
1,hello
2,goodbye
"""

test_context_models__schema_yml = """

version: 2

models:
    - name: model_a
      data_tests:
        - type_one
        - type_two
    - name: model_c
      data_tests:
        - call_pkg_macro
        - local_utils.dispatch
        - my_datediff

"""

test_context_models__model_c_sql = """
select 1 as fun

"""

test_context_models__model_b_sql = """
select 1 as notfun

"""

test_context_models__model_a_sql = """
select 1 as fun

"""

name_collision__schema_yml = """
version: 2
models:
- name: base
  columns:
  - name: extension_id
    data_tests:
    - not_null
- name: base_extension
  columns:
  - name: id
    data_tests:
    - not_null

"""

name_collision__base_sql = """
SELECT 'hello_world' AS extension_id
"""

name_collision__base_extension_sql = """
SELECT 'NOT_NULL' AS id
"""


dupe_generic_tests_collide__schema_yml = """
version: 2
models:
- name: model_a
  columns:
  - name: id
    data_tests:
    - not_null:
        config:
          where: "1=1"
    - not_null:
        config:
          where: "1=2"

"""

dupe_generic_tests_collide__model_a = """
SELECT 'NOT_NULL' AS id
"""


custom_generic_test_config_custom_macro__schema_yml = """
version: 2
models:
- name: model_a
  columns:
  - name: id
    data_tests:
    - not_null:
        config:
          where: "id = (select id from {{ ref('model_a') }} limit 1)"

"""

custom_generic_test_config_custom_macro__model_a = """
SELECT 1 AS id
"""


custom_generic_test_names__schema_yml = """
version: 2
models:
- name: model_a
  columns:
  - name: id
    data_tests:
    - not_null:
        name: not_null_where_1_equals_1
        config:
          where: "1=1"
    - not_null:
        name: not_null_where_1_equals_2
        config:
          where: "1=2"

"""

custom_generic_test_names__model_a = """
SELECT 'NOT_NULL' AS id
"""

custom_generic_test_names_alt_format__schema_yml = """
version: 2
models:
- name: model_a
  columns:
  - name: id
    data_tests:
    - name: not_null_where_1_equals_1
      test_name: not_null
      config:
        where: "1=1"
    - name: not_null_where_1_equals_2
      test_name: not_null
      config:
        where: "1=2"

"""

custom_generic_test_names_alt_format__model_a = """
SELECT 'NOT_NULL' AS id
"""


test_context_where_subq_macros__custom_generic_test_sql = """
/*{# This test will fail if get_where_subquery() is missing from TestContext + TestMacroNamespace #}*/

{% test self_referential(model) %}

    {%- set relation = api.Relation.create(schema=model.schema, identifier=model.table) -%}
    {%- set columns = adapter.get_columns_in_relation(relation) -%}
    {%- set columns_csv = columns | map(attribute='name') | list | join(', ') -%}

    select {{ columns_csv }} from {{ model }}
    limit 0

{% endtest %}

"""

invalid_schema_models__schema_yml = """
version: 2

models:
  name: model
  columns:
    - name: Id
      quote: true
      data_tests:
        - unique
        - not_null

"""

invalid_schema_models__model_sql = """
select 1 as "Id"

"""

all_quotes_schema__schema_yml = """# models/schema.yml
# only comments here, which should be okay!
# https://github.com/dbt-labs/dbt-core/issues/3568"""

models_v2__render_test_cli_arg_models__schema_yml = """
version: 2

models:
  - name: model
    data_tests:
      - equivalent:
          value: "{{ var('myvar', 'baz') }}-bar"

"""

models_v2__render_test_cli_arg_models__model_sql = """
select 1 as id

"""

models_v2__override_get_test_models__schema_yml = """
version: 2

models:
    - name: my_model_pass
      description: "The table has 1 null values, and we're okay with that, until it's more than 1."
      columns:
        - name: id
          description: "The number of responses for this favorite color - purple will be null"
          data_tests:
            - not_null:
                error_if: '>1'
                warn_if: '>1'

    - name: my_model_warning
      description: "The table has 1 null values, and we're okay with that, but let us know"
      columns:
        - name: id
          description: "The number of responses for this favorite color - purple will be null"
          data_tests:
            - not_null:
                error_if: '>1'

    - name: my_model_failure
      description: "The table has 2 null values, and we're not okay with that"
      columns:
        - name: id
          description: "The number of responses for this favorite color - purple will be null"
          data_tests:
            - not_null:
                error_if: '>1'


"""

models_v2__override_get_test_models__my_model_warning_sql = """
select * from {{ ref('my_model_pass') }}
"""

models_v2__override_get_test_models__my_model_pass_sql = """
select 1 as id
UNION ALL
select null as id
"""

models_v2__override_get_test_models__my_model_failure_sql = """
select * from {{ ref('my_model_pass') }}
UNION ALL
select null as id
"""

models_v2__models__schema_yml = """
version: 2

models:
    - name: table_copy
      description: "A copy of the table"
      columns:
        - name: id
          description: "The ID"
          data_tests:
            - not_null
            - unique
          tags:
            - table_id
        - name: first_name
          description: "The user's first name"
          data_tests:
            - not_null
          tags:
            - table_first_name
        - name: ip_address
          description: "The user's IP address"
          data_tests:
            - not_null
        - name: updated_at
          description: "The update time of the user"
          data_tests:
            - not_null
        - name: email
          description: "The user's email address"
          data_tests:
            - unique
        - name: favorite_color
          description: "The user's favorite color"
          data_tests:
            - accepted_values: {
                values: ['blue', 'green'],
                quote: true,
                tags: table_copy_favorite_color  # tags can be a single string
            }
          tags:
            - table_favorite_color
        - name: fav_number
          description: "The user's favorite number"
          data_tests:
            - accepted_values:
                values: [3.14159265]
                quote: false
                tags:  # tags can be a list of strings
                  - favorite_number_is_pi


    - name: table_summary
      description: "The summary table"
      columns:
        - name: favorite_color_copy
          description: "The favorite color"
          data_tests:
            - not_null
            - unique
            - accepted_values: { values: ['blue', 'green'] }
            - relationships: { field: favorite_color, to: ref('table_copy') }
          tags:
            - table_favorite_color
        - name: count
          description: "The number of responses for this favorite color"
          data_tests:
            - not_null

# all of these constraints will fail
    - name: table_failure_copy
      description: "The table copy that does not comply with the schema"
      columns:
        - name: id
          description: "The user ID"
          data_tests:
            - not_null
            - unique
          tags:
            - xfail
        - name: favorite_color
          description: "The user's favorite color"
          data_tests:
            - accepted_values: { values: ['blue', 'green'] }
          tags:
            - xfail

# all of these constraints will fail
    - name: table_failure_summary
      description: "The table summary that does not comply with the schema"
      columns:
        - name: favorite_color
          description: "The favorite color"
          data_tests:
            - accepted_values: { values: ['red'] }
            - relationships: { field: favorite_color, to: ref('table_copy') }
          tags:
            - xfail

# this table is disabled so these tests should be ignored
    - name: table_disabled
      description: "A disabled table"
      columns:
        - name: favorite_color
          description: "The favorite color"
          data_tests:
            - accepted_values: { values: ['red'] }
            - relationships: { field: favorite_color, to: ref('table_copy') }

# all of these constraints will fail
    - name: table_failure_null_relation
      description: "A table with a null value where it should be a foreign key"
      columns:
        - name: id
          description: "The user ID"
          data_tests:
            - relationships: { field: id, to: ref('table_failure_copy') }
          tags:
            - xfail

"""

models_v2__models__table_summary_sql = """
{{
    config(
        materialized='table'
    )
}}

select favorite_color as favorite_color_copy, count(*) as count
from {{ ref('table_copy') }}
group by 1

"""

models_v2__models__table_failure_summary_sql = """
{{
    config(
        materialized='table'
    )
}}

-- force a foreign key constraint failure here
select 'purple' as favorite_color, count(*) as count
from {{ ref('table_failure_copy') }}
group by 1

"""

models_v2__models__table_disabled_sql = """
{{
    config(
        enabled=False
    )
}}

-- force a foreign key constraint failure here
select 'purple' as favorite_color, count(*) as count
from {{ ref('table_failure_copy') }}
group by 1

"""

models_v2__models__table_failure_null_relation_sql = """
{{
    config(
        materialized='table'
    )
}}

-- force a foreign key constraint failure here
select 105 as id, count(*) as count
from {{ ref('table_failure_copy') }}
group by 1

"""

models_v2__models__table_failure_copy_sql = """

{{
    config(
        materialized='table'
    )
}}

select * from {{ this.schema }}.seed_failure

"""

models_v2__models__table_copy_sql = """

{{
    config(
        materialized='table'
    )
}}

select * from {{ this.schema }}.seed

"""

models_v2__malformed__schema_yml = """
version: 2

models:
  # this whole model should fail and not run
  - name: table_copy
    description: "A copy of the table"
    columns:
      - name: id
        description: "The ID"
        data_tests:
          - not_null
          - unique
      - name: favorite_color
        data_tests:
          # this is missing a "-" and is malformed
          accepted_values: { values: ['blue', 'green'] }

  # this whole model should pass and run
  - name: table_summary
    description: "The summary table"
    columns:
      - name: favorite_color
        description: "The favorite color"
        data_tests:
          - not_null
          - unique
          - accepted_values: { values: ['blue', 'green'] }
          - relationships: { field: favorite_color, to: ref('table_copy') }
      - name: count
        description: "The number of responses for this favorite color"
        data_tests:
          - not_null

"""

models_v2__malformed__table_summary_sql = """
{{
    config(
        materialized='table'
    )
}}

select favorite_color, count(*) as count
from {{ ref('table_copy') }}
group by 1

"""

models_v2__malformed__table_copy_sql = """

{{
    config(
        materialized='table'
    )
}}

select * from {{ this.schema }}.seed

"""

models_v2__override_get_test_models_fail__schema_yml = """
version: 2

models:
    - name: my_model
      description: "The table has 1 null values, and we're not okay with that."
      columns:
        - name: id
          description: "The number of responses for this favorite color - purple will be null"
          data_tests:
            - not_null



"""

models_v2__override_get_test_models_fail__my_model_sql = """
select 1 as id
UNION ALL
select null as id
"""

models_v2__custom_configs__schema_yml = """
version: 2

models:
  - name: table_copy
    description: "A copy of the table"
    # passes
    data_tests:
      - where
      - error_if
      - warn_if
      - limit
      - fail_calc
    columns:
      - name: id
        data_tests:
          # relationships with where
          - relationships:
              to: ref('table_copy')  # itself
              field: id
              where: 1=1
  - name: table_copy_another_one
    data_tests:
      - where:  # test override + weird quoting
          config:
            where: "\\"favorite_color\\" = 'red'"
  - name: "table.copy.with.dots"
    description: "A copy of the table with a gross name"
    # passes, see https://github.com/dbt-labs/dbt-core/issues/3857
    data_tests:
      - where

"""

models_v2__custom_configs__table_copy_another_one_sql = """
select * from {{ ref('table_copy') }}

"""

models_v2__custom_configs__table_copy_sql = """

{{
    config(
        materialized='table'
    )
}}

select * from {{ this.schema }}.seed

"""

models_v2__custom_configs__table_copy_with_dots_sql = """
select * from {{ ref('table_copy') }}

"""

models_v2__render_test_configured_arg_models__schema_yml = """
version: 2

models:
  - name: model
    data_tests:
      - equivalent:
          value: "{{ var('myvar', 'baz') }}-bar"

"""

models_v2__render_test_configured_arg_models__model_sql = """
select 1 as id

"""

models_v2__custom__schema_yml = """
version: 2

models:
  - name: table_copy
    description: "A copy of the table"
    columns:
      - name: email
        data_tests:
          - not_null
      - name: id
        description: "The ID"
        data_tests:
          - unique
      - name: favorite_color
        data_tests:
          - every_value_is_blue
          - rejected_values: { values: ['orange', 'purple'] }
    # passes
    data_tests:
      - local_dep.equality: { compare_model: ref('table_copy') }

"""

models_v2__custom__table_copy_sql = """

{{
    config(
        materialized='table'
    )
}}

select * from {{ this.schema }}.seed

"""

models_v2__limit_null__schema_yml = """
version: 2

models:
    - name: table_limit_null
      description: "The table has 1 null values, and we're okay with that, until it's more than 1."
      columns:
        - name: favorite_color_full_list
          description: "The favorite color"
        - name: count
          description: "The number of responses for this favorite color - purple will be null"
          data_tests:
            - not_null:
                error_if: '>1'
                warn_if: '>1'

    - name: table_warning_limit_null
      description: "The table has 1 null value, and we're okay with 1, but want to know of any."
      columns:
        - name: favorite_color_full_list
          description: "The favorite color"
        - name: count
          description: "The number of responses for this favorite color - purple will be null"
          data_tests:
            - not_null:
                error_if: '>1'

    - name: table_failure_limit_null
      description: "The table has some 2 null values, and that's not ok.  Warn and error."
      columns:
        - name: favorite_color_full_list
          description: "The favorite color"
        - name: count
          description: "The number of responses for this favorite color - purple will be null"
          data_tests:
            - not_null:
                error_if: '>1'

"""

models_v2__limit_null__table_warning_limit_null_sql = """
{{
    config(
        materialized='table'
    )
}}

select * from {{ref('table_limit_null')}}
"""

models_v2__limit_null__table_limit_null_sql = """
{{
    config(
        materialized='table'
    )
}}

select favorite_color as favorite_color_full_list, count(*) as count
from {{ this.schema }}.seed
group by 1

UNION ALL

select 'purple' as favorite_color_full_list, null as count
"""

models_v2__limit_null__table_failure_limit_null_sql = """
{{
    config(
        materialized='table'
    )
}}

select * from {{ref('table_limit_null')}}

UNION ALL

select 'magenta' as favorite_color_full_list, null as count
"""

local_utils__dbt_project_yml = """
name: 'local_utils'
version: '1.0'
config-version: 2

profile: 'default'

macro-paths: ["macros"]


"""

local_utils__macros__datediff_sql = """
{% macro datediff(first_date, second_date, datepart) %}
  {{ return(adapter.dispatch('datediff', 'local_utils')(first_date, second_date, datepart)) }}
{% endmacro %}


{% macro default__datediff(first_date, second_date, datepart) %}

    datediff(
        {{ datepart }},
        {{ first_date }},
        {{ second_date }}
        )

{% endmacro %}


{% macro greenplum__datediff(first_date, second_date, datepart) %}

    {% if datepart == 'year' %}
        (date_part('year', ({{second_date}})::date) - date_part('year', ({{first_date}})::date))
    {% elif datepart == 'quarter' %}
        ({{ adapter.dispatch('datediff', 'local_utils')(first_date, second_date, 'year') }} * 4 + date_part('quarter', ({{second_date}})::date) - date_part('quarter', ({{first_date}})::date))
    {% else %}
        ( 1000 )
    {% endif %}

{% endmacro %}


"""

local_utils__macros__current_timestamp_sql = """
{% macro current_timestamp() -%}
  {{ return(adapter.dispatch('current_timestamp')) }}
{%- endmacro %}

{% macro default__current_timestamp() -%}
  now()
{%- endmacro %}

"""

local_utils__macros__custom_test_sql = """
{% macro test_dispatch(model) -%}
  {{ return(adapter.dispatch('test_dispatch', macro_namespace = 'local_utils')()) }}
{%- endmacro %}

{% macro default__test_dispatch(model) %}
    select {{ adapter.dispatch('current_timestamp', macro_namespace = 'local_utils')() }}
{% endmacro %}

"""

ephemeral__schema_yml = """

version: 2
models:
    - name: ephemeral
      columns:
          - name: id
            data_tests:
                - unique

"""

ephemeral__ephemeral_sql = """

{{ config(materialized='ephemeral') }}

select 1 as id

"""

quote_required_models__schema_yml = """
version: 2

models:
  - name: model
    columns:
      - name: Id
        quote: true
        data_tests:
          - unique
          - not_null
  - name: model_again
    quote_columns: true
    columns:
      - name: Id
        data_tests:
          - unique
          - not_null
  - name: model_noquote
    quote_columns: true
    columns:
      - name: Id
        quote: false
        data_tests:
          - unique
          - not_null

sources:
  # this should result in column quoting = true
  - name: my_source
    schema: "{{ target.schema }}"
    quoting:
      column: true
    tables:
      - name: model
        quoting:
          column: false
        columns:
          - name: Id
            quote: true
            data_tests:
              - unique
  - name: my_source_2
    schema: "{{ target.schema }}"
    quoting:
      column: false
    tables:
      # this should result in column quoting = true
      - name: model
        quoting:
          column: true
        columns:
          - name: Id
            data_tests:
              - unique
      # this should result in column quoting = false
      - name: model_noquote
        columns:
          - name: Id
            data_tests:
              - unique


"""

quote_required_models__model_again_sql = """
select 1 as "Id"

"""

quote_required_models__model_noquote_sql = """
select 1 as id

"""

quote_required_models__model_sql = """
select 1 as "Id"

"""

alt_local_utils__macros__type_timestamp_sql = """
{%- macro type_timestamp() -%}
    {{ return(adapter.dispatch('type_timestamp', 'local_utils')()) }}
{%- endmacro -%}

{% macro default__type_timestamp() %}
    {{ return(adapter.dispatch('type_timestamp', 'dbt')()) }}
{% endmacro %}
"""

macro_resolution_order_macros__my_custom_test_sql = """
{% test my_custom_test(model) %}
  select cast(current_timestamp as {{ dbt.type_timestamp() }})
  limit 0
{% endtest %}
"""

macro_resolution_order_models__my_model_sql = """
select 1 as id
"""

macro_resolution_order_models__config_yml = """
version: 2
models:
  - name: my_model
    data_tests:
      - my_custom_test
"""

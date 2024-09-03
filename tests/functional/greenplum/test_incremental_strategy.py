import re

import pytest

from tests.functional.greenplum.fixtures import (
    models__incremental_default_sql,
    models__incremental_delete_insert_sql,
    models__incremental_truncate_insert_sql,
)
from tests.functional.utils import run_dbt, run_dbt_and_capture
from dbt.tests.util import read_file, relation_from_name

def _normalize_whitespace(input: str) -> str:
    subbed = re.sub(r"\s+", " ", input)
    return re.sub(r"\s?([\(\),])\s?", r"\1", subbed).lower().strip()

def _find_and_replace(sql, find, replace):
    sql_tokens = sql.split()
    for idx in [n for n, x in enumerate(sql_tokens) if find in x]:
        sql_tokens[idx] = replace
    return " ".join(sql_tokens)


class TestGreenplumDefaultStrategy:
    @pytest.fixture(scope="class")
    def models(self):
        return {"incremental_default.sql": models__incremental_default_sql}

    @pytest.fixture(scope="class")
    def expected_sql_after_first_run(self):
        return """
create table <model_identifier>
as
(
    with source_data as (
        select 1 as id
        union all
        select null as id
    )

    select *
    from source_data
)
DISTRIBUTED BY (id);
"""

    @pytest.fixture(scope="class")
    def expected_sql_after_second_run(self):
        return """
insert into <model_identifier> ("id")
(
    select "id"
    from <model_identifier>
)
"""

    def test_incremental_default(self, project, expected_sql_after_first_run, expected_sql_after_second_run):
        # First run
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "incremental_default.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "incremental_default", "<model_identifier>")
        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql_after_first_run) == _normalize_whitespace(generated_sql_generic)

        # base table rowcount
        relation = relation_from_name(project.adapter, "incremental_default")
        result = project.run_sql(f"select count(*) as num_rows from {relation}", fetch="one")
        assert result[0] == 2

        # Second run
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "incremental_default.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "incremental_default", "<model_identifier>")

        assert "INSERT 0 2" in log_output
        assert _normalize_whitespace(expected_sql_after_second_run) == _normalize_whitespace(generated_sql_generic)

        result = project.run_sql(f"select count(*) as num_rows from {relation}", fetch="one")
        assert result[0] == 4

class TestGreenplumDeleteInsertStrategy:
    @pytest.fixture(scope="class")
    def models(self):
        return {"incremental_delete_insert.sql": models__incremental_delete_insert_sql}

    @pytest.fixture(scope="class")
    def expected_sql_after_first_run(self):
        return """
create table <model_identifier>
as
(
    with source_data as (
        select 1 as id
        union all
        select null as id
    )

    select *
    from source_data
)
DISTRIBUTED BY (id);
"""

    @pytest.fixture(scope="class")
    def expected_sql_after_second_run(self):
        return """
insert into <model_identifier> ("id")
(
    select "id"
    from <model_identifier>
)
"""

    def test_incremental_delete_insert(self, project, expected_sql_after_first_run, expected_sql_after_second_run):
        # First run
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "incremental_delete_insert.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "incremental_delete_insert", "<model_identifier>")
        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql_after_first_run) == _normalize_whitespace(generated_sql_generic)

        # base table rowcount
        relation = relation_from_name(project.adapter, "incremental_delete_insert")
        result = project.run_sql(f"select count(*) as num_rows from {relation}", fetch="one")
        assert result[0] == 2

        # Second run
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "incremental_delete_insert.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "incremental_delete_insert", "<model_identifier>")

        assert "INSERT 0 2" in log_output
        assert _normalize_whitespace(expected_sql_after_second_run) == _normalize_whitespace(generated_sql_generic)

        result = project.run_sql(f"select count(*) as num_rows from {relation}", fetch="one")
        assert result[0] == 4

class TestGreenplumTruncateInsertStrategy:
    @pytest.fixture(scope="class")
    def models(self):
        return {"incremental_truncate_insert.sql": models__incremental_truncate_insert_sql}

    @pytest.fixture(scope="class")
    def expected_sql_after_first_run(self):
        return """
create table <model_identifier>
as
(
    with source_data as (
        select 1 as id
        union all
        select null as id
    )

    select *
    from source_data
)
DISTRIBUTED BY (id);
"""

    @pytest.fixture(scope="class")
    def expected_sql_after_second_run(self):
        return """
truncate <model_identifier>
insert into <model_identifier> ("id")
(
    select "id"
    from <model_identifier>
)
"""

    def test_incremental_truncate_insert(self, project, expected_sql_after_first_run, expected_sql_after_second_run):
        # First run
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "incremental_truncate_insert.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "incremental_truncate_insert", "<model_identifier>")
        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql_after_first_run) == _normalize_whitespace(generated_sql_generic)

        # base table rowcount
        relation = relation_from_name(project.adapter, "incremental_truncate_insert")
        result = project.run_sql(f"select count(*) as num_rows from {relation}", fetch="one")
        assert result[0] == 2

        # Second run
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "incremental_truncate_insert.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "incremental_truncate_insert", "<model_identifier>")

        assert "INSERT 0 2" in log_output
        assert _normalize_whitespace(expected_sql_after_second_run) == _normalize_whitespace(generated_sql_generic)

        result = project.run_sql(f"select count(*) as num_rows from {relation}", fetch="one")
        assert result[0] == 2



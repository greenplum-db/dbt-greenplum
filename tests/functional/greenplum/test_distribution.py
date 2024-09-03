import re

import pytest

from tests.functional.greenplum.fixtures import (
    models__default_distribution_sql,
    models__distributed_by_sql,
    models__distributed_replicated_sql,
    models__distributed_randomly_sql,
)
from tests.functional.utils import run_dbt, run_dbt_and_capture
from dbt.tests.util import read_file

def _normalize_whitespace(input: str) -> str:
    subbed = re.sub(r"\s+", " ", input)
    return re.sub(r"\s?([\(\),])\s?", r"\1", subbed).lower().strip()

def _find_and_replace(sql, find, replace):
    sql_tokens = sql.split()
    for idx in [n for n, x in enumerate(sql_tokens) if find in x]:
        sql_tokens[idx] = replace
    return " ".join(sql_tokens)


class TestGreenplumDefaultDistribution:
    @pytest.fixture(scope="class")
    def models(self):
        return {"default_distribution.sql": models__default_distribution_sql}

    @pytest.fixture(scope="class")
    def expected_sql(self):
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
);
"""

    def test_default_distribution(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "default_distribution.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "default_distribution", "<model_identifier>")

        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)

class TestGreenplumDistributedBy:
    @pytest.fixture(scope="class")
    def models(self):
        return {"distributed_by.sql": models__distributed_by_sql}

    @pytest.fixture(scope="class")
    def expected_sql(self):
        return """
create table <model_identifier>
as
(
    with source_data as (
        select 1 as id, 'aaa' as name 
        union all
        select null as id, 'xxx' as name
    )

    select *
    from source_data
)
DISTRIBUTED BY (id, name)
;
"""

    def test_distributed_by(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "distributed_by.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "distributed_by", "<model_identifier>")

        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)

class TestGreenplumDistributedReplicated:
    @pytest.fixture(scope="class")
    def models(self):
        return {"distributed_replicated.sql": models__distributed_replicated_sql}

    @pytest.fixture(scope="class")
    def expected_sql(self):
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
DISTRIBUTED REPLICATED
;
"""

    def test_distributed_replicated(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "distributed_replicated.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "distributed_replicated", "<model_identifier>")

        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)

class TestGreenplumDistributedRandomly:
    @pytest.fixture(scope="class")
    def models(self):
        return {"distributed_randomly.sql": models__distributed_randomly_sql}

    @pytest.fixture(scope="class")
    def expected_sql(self):
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
DISTRIBUTED RANDOMLY
;
"""

    def test_distributed_randomly(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "distributed_randomly.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "distributed_randomly", "<model_identifier>")

        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)

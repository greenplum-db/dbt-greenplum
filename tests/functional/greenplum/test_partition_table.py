import re

import pytest

from tests.functional.greenplum.fixtures import (
    models__partition_syntax1_sql,
    models__partition_syntax2_sql,
    models__partition_syntax3_sql,
    models__partition_syntax4_sql,
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

def _expected_sql():
    return """
create table if not exists <model_identifier> (
     id int4 null,
     incomingdate timestamp NULL
)
PARTITION BY RANGE (incomingdate)
(
    START ('2021-01-01'::timestamp) INCLUSIVE
    END ('2023-01-01'::timestamp) EXCLUSIVE
    EVERY (INTERVAL '1 day'),
    DEFAULT PARTITION extra
);

insert into <model_identifier> (
with source_data as (
    select
        1 as id,
        '2022-02-22'::timestamp as incomingdate
    union all
    select
        null as id,
        '2022-02-25'::timestamp as incomingdate
)
select *
from source_data
);
"""

class TestGreenplumPartitionTableSyntax1:
    @pytest.fixture(scope="class")
    def expected_sql(self):
        return _expected_sql()

    @pytest.fixture(scope="class")
    def models(self):
        return {"partition_syntax1.sql": models__partition_syntax1_sql}    

    def test_partition_syntax1(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "partition_syntax1.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "partition_syntax1", "<model_identifier>")

        assert "INSERT 0 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)


class TestGreenplumPartitionTableSyntax2:
    @pytest.fixture(scope="class")
    def expected_sql(self):
        return _expected_sql()

    @pytest.fixture(scope="class")
    def models(self):
        return {"partition_syntax2.sql": models__partition_syntax2_sql}    

    def test_partition_syntax2(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "partition_syntax2.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "partition_syntax2", "<model_identifier>")

        assert "INSERT 0 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)

class TestGreenplumPartitionTableSyntax3:
    @pytest.fixture(scope="class")
    def expected_sql(self):
        return _expected_sql()

    @pytest.fixture(scope="class")
    def models(self):
        return {"partition_syntax3.sql": models__partition_syntax3_sql}    

    def test_partition_syntax3(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "partition_syntax3.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "partition_syntax3", "<model_identifier>")

        assert "INSERT 0 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)

class TestGreenplumPartitionTableSyntax4:
    @pytest.fixture(scope="class")
    def expected_sql(self):
        return """
create table if not exists <model_identifier> (
    id int4 null,
    code char(1)
)
PARTITION BY LIST (code)
    (
        PARTITION sales VALUES ('S'),
        PARTITION returns VALUES ('R'),
        DEFAULT PARTITION extra
    )
;

insert into <model_identifier> (
with source_data as (
    select
        1 as id,
        'S' as code
    union all
    select
        null as id,
        'N' as code
)
select *
from source_data
);
"""

    @pytest.fixture(scope="class")
    def models(self):
        return {"partition_syntax4.sql": models__partition_syntax4_sql}    

    def test_partition_syntax4(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "partition_syntax4.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "partition_syntax4", "<model_identifier>")

        assert "INSERT 0 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)
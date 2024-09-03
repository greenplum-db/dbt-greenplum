import re

import pytest

from tests.functional.greenplum.fixtures import (
    models__heap_sql,
    models__ao_sql,
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


class TestGreenplumHeapStorage:
    @pytest.fixture(scope="class")
    def models(self):
        return {"heap.sql": models__heap_sql}

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
DISTRIBUTED BY (id);
"""

    def test_heap_storage(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "heap.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "heap", "<model_identifier>")

        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)


class TestGreenplumAOStorage:
    @pytest.fixture(scope="class")
    def models(self):
        return {"ao.sql": models__ao_sql}

    @pytest.fixture(scope="class")
    def expected_sql(self):
        return """
create table <model_identifier>
with (
        appendoptimized=True
        , blocksize=32768
        , compresstype=ZLIB
        , compresslevel=1
        , orientation=column
    )
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

    def test_ao_storage(self, project, expected_sql):
        _, log_output = run_dbt_and_capture(["run"], expect_pass=True)

        generated_sql = read_file("target", "run", "test", "models", "ao.sql")
        generated_sql_generic = _find_and_replace(generated_sql, "ao", "<model_identifier>")

        assert "SELECT 2" in log_output
        assert _normalize_whitespace(expected_sql) == _normalize_whitespace(generated_sql_generic)
import re

import pytest

from tests.functional.greenplum.fixtures import (
    models__heap_sql,
    models__dry_run_sql,
)
from tests.functional.utils import run_dbt, run_dbt_and_capture

class TestGreenplumDryRun:
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "heap.sql": models__heap_sql,
            "dry_run.sql": models__dry_run_sql,
        }

    def test_dry_run(self, project):
        _, log_output = run_dbt_and_capture(["run", "--empty"], expect_pass=True)

        assert "SELECT 0" in log_output
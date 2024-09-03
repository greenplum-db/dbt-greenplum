import os

import pytest

from tests.functional.projects import dbt_integration


@pytest.fixture(scope="class")
def dbt_integration_project():
    return dbt_integration()


@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        "type": "greenplum",
        "host": os.getenv("GREENPLUM_TEST_HOST", "localhost"),
        "port": int(os.getenv("GREENPLUM_TEST_PORT", 7000)),
        "user": os.getenv("GREENPLUM_TEST_USER", "gpadmin"),
        "pass": os.getenv("GREENPLUM_TEST_PASS", "password"),
        "dbname": os.getenv("GREENPLUM_TEST_DATABASE", "dbt"),
        "threads": int(os.getenv("GREENPLUM_TEST_THREADS", 4)),
    }

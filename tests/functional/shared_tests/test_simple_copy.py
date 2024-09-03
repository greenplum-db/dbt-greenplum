import pytest
from dbt.tests.adapter.simple_copy.test_copy_uppercase import BaseSimpleCopyUppercase
from dbt.tests.adapter.simple_copy.test_simple_copy import (
    SimpleCopyBase,
    EmptyModelsArentRunBase,
)

# Greenplum-Specific: using greenplum configuration
class TestSimpleCopyUppercase(BaseSimpleCopyUppercase):
    @pytest.fixture(scope="class")
    def dbt_profile_target(self):
        return {
            "type": "greenplum",
            "threads": 4,
            "host": "localhost",
            "port": 7000,
            "user": "gpadmin",
            "pass": "password",
            "dbname": "dbtMixedCase",
        }


class TestSimpleCopyBase(SimpleCopyBase):
    pass


class TestEmptyModelsArentRun(EmptyModelsArentRunBase):
    pass

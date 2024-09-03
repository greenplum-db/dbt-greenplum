import pytest
from dbt.tests.adapter.incremental.test_incremental_merge_exclude_columns import (
    BaseMergeExcludeColumns,
)
from dbt.tests.adapter.incremental.test_incremental_on_schema_change import (
    BaseIncrementalOnSchemaChange,
)
from dbt.tests.adapter.incremental.test_incremental_predicates import BaseIncrementalPredicates
from dbt.tests.adapter.incremental.test_incremental_unique_id import BaseIncrementalUniqueKey

# Greenplum-Specific: Greenplum does NOT support merge statement, so we disable this test case here.
@pytest.mark.skip("Greenplum does NOT support merge statement, so we skip this test case.")
class TestBaseMergeExcludeColumns(BaseMergeExcludeColumns):
    pass

class TestIncrementalOnSchemaChange(BaseIncrementalOnSchemaChange):
    pass


class TestIncrementalPredicatesDeleteInsert(BaseIncrementalPredicates):
    pass


class TestIncrementalUniqueKey(BaseIncrementalUniqueKey):
    pass

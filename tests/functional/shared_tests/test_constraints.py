import pytest
from dbt.tests.adapter.constraints.test_constraints import (
    BaseTableConstraintsColumnsEqual,
    BaseViewConstraintsColumnsEqual,
    BaseIncrementalConstraintsColumnsEqual,
    BaseConstraintsRuntimeDdlEnforcement,
    BaseConstraintsRollback,
    BaseIncrementalConstraintsRuntimeDdlEnforcement,
    BaseIncrementalConstraintsRollback,
    BaseTableContractSqlHeader,
    BaseIncrementalContractSqlHeader,
    BaseModelConstraintsRuntimeEnforcement,
    BaseConstraintQuotedColumn,
    BaseIncrementalForeignKeyConstraint,
)


class TestTableConstraintsColumnsEqual(BaseTableConstraintsColumnsEqual):
    pass


class TestViewConstraintsColumnsEqual(BaseViewConstraintsColumnsEqual):
    pass


class TestIncrementalConstraintsColumnsEqual(BaseIncrementalConstraintsColumnsEqual):
    pass


class TestTableConstraintsRuntimeDdlEnforcement(BaseConstraintsRuntimeDdlEnforcement):
    pass


class TestTableConstraintsRollback(BaseConstraintsRollback):
    pass


class TestIncrementalConstraintsRuntimeDdlEnforcement(
    BaseIncrementalConstraintsRuntimeDdlEnforcement
):
    pass


class TestIncrementalConstraintsRollback(BaseIncrementalConstraintsRollback):
    pass


class TestTableContractSqlHeader(BaseTableContractSqlHeader):
    pass


class TestIncrementalContractSqlHeader(BaseIncrementalContractSqlHeader):
    pass

# Greenplum-Specific: Greenplum requires that UNIQUE or PRIMARY KEY definitions are incompatible with each other.
# So this test case will fail. we disable this test case here.
@pytest.mark.skip("Greenplum requires that UNIQUE or PRIMARY KEY definitions are incompatible with each other.")
class TestModelConstraintsRuntimeEnforcement(BaseModelConstraintsRuntimeEnforcement):
    pass

class TestConstraintQuotedColumn(BaseConstraintQuotedColumn):
    pass


class TestIncrementalForeignKeyConstraint(BaseIncrementalForeignKeyConstraint):
    pass

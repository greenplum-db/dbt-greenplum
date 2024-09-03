from dbt.adapters.greenplum import GreenplumConnectionManager
from dbt.adapters.postgres.impl import PostgresAdapter

"""
TODO: Need to check whether it's ok to disable "merge" policy and enable "truncate+insert" policy
"""
class GreenplumAdapter(PostgresAdapter):
    ConnectionManager = GreenplumConnectionManager

    def valid_incremental_strategies(self):
        """The set of standard builtin strategies which this adapter supports out-of-the-box.
        Not used to validate custom strategies defined by end users.
        """
        return ["append", "delete+insert", "truncate+insert"]


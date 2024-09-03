import psycopg2
from dbt.adapters.events.logging import AdapterLogger
from dbt.adapters.postgres.connections import PostgresCredentials, PostgresConnectionManager
logger = AdapterLogger("Greenplum")

class GreenplumCredentials(PostgresCredentials):

    @property
    def type(self):
        return "greenplum"


class GreenplumConnectionManager(PostgresConnectionManager):
    TYPE = "greenplum"

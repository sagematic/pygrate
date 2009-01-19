import database
import oracle_syntax


class OracleConnection(database.Connection):
    """An oracle database connection wrapper."""

    def __init__( self ):
        database.Connection.__init__( self, oracle_syntax.OracleSyntax() )
        self._last_sql = ""

    def close( self ):
        pass

    def last_sql( self ):
        return self._last_sql

    def execute_sql( self, sql ):
        self._last_sql = sql


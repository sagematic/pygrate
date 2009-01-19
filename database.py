

class Database:
    """An actual database
    """

    def close( self ):
        pass

    def create_table_sql( self, table_name, columns ):
        pass

    def rename_table_sql( self, old_table_name, new_table_name ):
        pass

    def drop_table_sql( self, table_name ):
        """Generic syntax to drop a table."""
        sql = "DROP TABLE %s;" % ( table_name )
        return sql

    def add_column_sql( self, table, column_obj ):
        pass

    def rename_column_sql( self, table, old_name, new_name ):
        pass

    def drop_column_sql( self, table, column_name ):
        pass

    def execute_sql( self, sql ):
        pass

def open( path ):
    import test.mock_database
    return test.mock_database.MockDatabase()


import pygration


class CreateEmployeeTable(pygration.Step):
    def add(self, db):
        db.sql(
                """
                CREATE TABLE employee
                ( id number
                , firstname varchar2(10)
                , lastname varchar2(10)
                );""" )


class CreateJobTable(pygration.Step):
    def add(self, db):
        db.sql( \
                """
                CREATE TABLE job
                ( id number
                , name varchar2(57)
                );
                """ )


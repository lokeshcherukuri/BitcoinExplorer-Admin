import mysql.connector.pooling
from unittest import TestCase, main


class MySQLConnectionPool:

    dbconfig = {
        "host": "127.0.0.1",
        "port": "3306",
        "user": "lcherukuri",
        "password": "password",
        "database": "coinexplorer",
    }

    def __init__(self):
        self.connection_pool = self.createPool()

    def createPool(self):
        pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name='coinexplorer',
            pool_size=10,
            **self.dbconfig
        )
        return pool

    def getConnection(self):
        return self.connection_pool.get_connection()

    # def closeConnection(self, connection, cursor):
    #     if connection is None:
    #         return RuntimeError("Connection object is None")
    #     if cursor is None:
    #         return RuntimeError("Cursor object is None")
    #     connection.close()
    #     cursor.close()

    def execute(self, query, args, querytype):
        connection = self.getConnection()
        cursor = connection.cursor()
        if args is not None:
            cursor.execute(query, args)
        else:
            cursor.execute(query)

        if querytype == 'insertOrUpdate':
            connection.commit()
            return None
        elif querytype == 'select':
            return dict(zip(cursor.column_names, cursor.fetchall()))


class TestMySQLConnectionPool(TestCase):
    def test_execute(self):
        pool = MySQLConnectionPool()
        records = pool.execute("SELECT * FROM timetable;")
        print(records)
        # for record in records:
        #     print(record)


if __name__ == '__main__':
    main()

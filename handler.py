import sqlite3 as sql


class RequestHandler:
    def __init__(self, db_path):
        self._connection = sql.connect(db_path)
        self._cursor = self._connection.cursor()

    def execute(self, request):
        self._cursor.execute(request)
        return self._cursor.fetchall()

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()

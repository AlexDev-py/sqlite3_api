"""

Основная работа с базой данных

"""

import sqlite3 as sql


class Sqlite3:

    def __init__(self, db_path):
        self._connection = sql.connect(db_path)
        self._cursor = self._connection.cursor()

    def fetchall(self, request: str):
        """
        Выполняем запрос `request`
        и возвращаем результат используя fetchall
        """

        self._cursor.execute(request)
        return self._cursor.fetchall()

    def execute(self, request: str):
        """ Выполняем запрос `request` """

        self._cursor.execute(request)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()

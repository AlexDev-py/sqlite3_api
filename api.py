"""

Основная работа с базой данных

"""

import sqlite3 as sql


class Sqlite3ApiOperationalError(sql.OperationalError):
    """
    Ошибки запросов.
    """

    def __init__(self, err: sql.OperationalError, request: str, args: tuple):
        self.err_info = str(err)
        self.request = request  # Запрос, который вызвал исключение
        self.args = args  # Аргументы запроса

    def __str__(self):
        return f'{self.err_info}. request: {self.request}. args: {self.args}'


class Sqlite3:

    def __init__(self, db_path):
        self._connection = sql.connect(
            db_path, detect_types=sql.PARSE_DECLTYPES
        )
        self._cursor = self._connection.cursor()

    def fetchall(self, request: str, *args):
        """
        Выполняем запрос `request`
        и возвращаем результат используя fetchall.
        """

        self.execute(request, *args)
        return self._cursor.fetchall()

    def execute(self, request: str, *args):
        """
        Выполняем запрос `request`.
        """

        try:
            self._cursor.execute(request, args)
        except sql.OperationalError as err:
            raise Sqlite3ApiOperationalError(err, request, args)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()

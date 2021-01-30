"""

Файл с таблицами можно назвать как угодно.
Строчка `from sqlite3_api.Table import Table` должна быть обязательна,
 она импортирует класс `Table`, который позволяет создавать таблицы.

Для того чтобы API могло нормально работать с классами таблиц,
 нужно создать эти классы.
Для того чтобы определить тип столбца, используем встроенные типы данных Python:
 - str (будет храниться как TEXT)
 - int (будет храниться как INTEGER)
 Так же существуют дополнительные типы данных(List и Dict).
 Их вы можете найти в файле types.py.
 Так же там находятся инструменты для создания пользовательских типов данных.

NEXT: create_database.py

"""

from __future__ import annotations
from sqlite3_api.Table import Table
from sqlite3_api.types import List

# Инструмент для создания новых типов данных
from sqlite3_api.types import CustomType


class Students(Table):
    # Поле `first_name`. Тип данных: text. Значение по умолчанию: отсутствует
    first_name: str
    last_name: str
    age: int
    # Поле `course`. Тип данных: integer. Значение по умолчанию: 1
    course: int = 1
    salary: int = 5000
    marks: List = []


"""
Представим, что нам необходимо хранить данные о точках на двумерной плоскости.
Мы не хотим делать отдельные поля `x` и `y` для хранения координат.
Поэтому мы реализуем новый тип данных `Position`
"""


class Position(CustomType):
    """
    Новый тип данных, который хранит координаты на двумерной плоскости
    `x` и `y`.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __sub__(self, other: tuple):
        """
        Будет вызван при вычитании.
        :return: self
        """

        self.x -= other[0]
        self.y -= other[1]
        return self

    def __add__(self, other: tuple):
        """
        Будет вызван при сложении.
        :return: self
        """

        self.x += other[0]
        self.y += other[1]
        return self

    def __repr__(self):
        """
        Будет вызван при переводе в строку.
        :return: (<self.x>;<self.y>)
        """

        return '(%f;%f)' % (self.x, self.y)

    @staticmethod
    def adapter(obj: Position) -> bytes:
        """
        Определяем метод `adapter`,
        который будет возвращать данные в том виде,
        в каком они будут храниться в таблице.
        """

        return ('%f;%f' % (obj.x, obj.y)).encode('ascii')

    def converter(self, obj: bytes) -> Position:
        """
        Определяем метод `converter`,
        который будет возвращать объект этого класса,
        основываясь на данных, полученных из таблицы.
        """

        return Position(*map(float, obj.split(b";")))


class Points(Table):
    # Делаем значение по умолчанию именно такого вида,
    # который возвращает метод `adapter`
    # >>> Position.adapter(Position(x=0, y=0))
    position: Position = '0;0'
    color: str = 'Blue'
    size: int = 1

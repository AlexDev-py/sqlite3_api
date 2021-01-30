"""

Пользовательские типы данных.

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from ast import literal_eval

from .api import sql
from .main import Sqlite3ApiError


class CustomType(ABC):
    """
    Инструмент для создания своих типов данных.
    """

    def __init_subclass__(cls, **kwargs):
        """
        Инициализируем тип данных.
        """

        sql.register_adapter(cls, cls.adapter)
        sql.register_converter(
            cls.__name__.lower(), lambda obj: cls.converter(cls, obj)
        )

    @staticmethod
    def adapter(obj: CustomType) -> bytes:
        """
        Получаем строку для записи в бд.
        :param obj: Объект поля.
        """

        return str(obj).encode('ascii')

    @abstractmethod
    def converter(self, obj: bytes) -> CustomType:
        """
        Возвращает объект поля.
        :param obj: Строка полученная из бд.
        """

        raise Sqlite3ApiError(
            f'Не объявлен метод `converter` в классе `{self.__name__}`'
        )


class List(CustomType, list):
    """
    Список. Может содержать: списки, числа, строки, словари.
    """

    def __init__(self, args):
        super().__init__(args)

    def converter(self, obj: bytes) -> List:
        return List(literal_eval(obj.decode('utf-8')))


class Dict(CustomType, dict):
    """
    Словарь. Может содержать: списки, числа, строки, словари.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def converter(self, obj: bytes) -> Dict:
        return Dict(literal_eval(obj.decode('utf-8')))

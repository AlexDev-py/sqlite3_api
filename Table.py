"""

Всё что нужно для создания класса таблицы

"""

from typing import Dict, List

from .tools import string, integer, list_, dict_


class Table:
    """ Родительский класс для создания классов таблиц """

    id = None

    @classmethod
    def __call__(cls, *args, **kwargs):
        pass

    @classmethod
    def get_types(cls) -> Dict[str, list]:
        """
        Получаем словарь
        {<название поля: str>: <тип данных: list>}
        """

        return {
            k: v
            for k, v in vars(cls).items()
            if not k.startswith('__')
        }

    @classmethod
    def get_fields(cls) -> List[str]:
        """ Получаем названия всех полей исключая `id` """

        return [
            field for field in cls.get_types().keys()
            if field != 'id'
        ]

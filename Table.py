"""

Всё что нужно для создания класса таблицы

"""

from __future__ import annotations
from typing import Literal

from .main import API, Sqlite3ApiError


class Table(object):
    """
    Родительский класс для создания таблиц
    """

    id: int = None

    def __init__(
            self, db_path: str = None,
            _api: API = None,
            **kwargs
    ):
        """
        :param db_path: Путь к базе данных.
        """

        self.__api = _api or API(db_path)
        self.__inited = bool(_api)
        self.__dict__.update(**kwargs)

    def save(self) -> str:
        """
        Сохраняем все изменения.
        :return: "Successfully"
        """

        return self.__api.save(self)

    def update(self, **fields):
        """
        Обновляем значения и автоматически сохраняем.
        :param fields: {<название поля>: <значение>, ...}
        :return:
        """

        self.__dict__.update(**fields)
        return self.save()

    def filter(
            self,
            return_type: Literal['visual', 'classes'] = 'classes',
            return_list: Literal[True, False] = False,
            **where
    ):
        """
        Функция выбирает данные из таблицы на основе указанных параметров.
        :param return_type:
            Для "classes" - вернёт объект класса таблицы.
            Для "visual" - вернёт данные в том виде,
                в котором они хранятся в базе данных.
        :param return_list:
            Для True - вернёт список объектов независимо от их количества.
        :param where: Параметры сортировки.
        :return: Объект класса таблицы.
        """

        if (
                data := self.__api.filter(
                    table_name=self.table_name,
                    **where
                )
        ):
            if return_type == 'visual':
                if return_list:
                    return data

                return data[0] if len(data) == 1 else data

            else:
                data = [self.get_class(obj) for obj in data]
                if return_list:
                    return data

                return data[0] if len(data) == 1 else data

        return [] if return_list else None

    def insert(self, **fields) -> str:
        """
        Функция добавляет данные в таблицу.
        :param fields: {<название поля>: <значение>, ...}.
        :return: "Successfully"
        """

        table_fields = {
            field_name: default_value
            for field_name, default_value in vars(self.__class__).items()
            if not field_name.startswith('__')
        }
        table_fields.update(**fields)

        if len(_fields := set(table_fields) - set(self.get_fields())):
            raise Sqlite3ApiError(
                f'В таблице `{self.table_name}` не найдены поля: '
                f'{", ".join(_fields)}'
            )

        if len(_fields := set(self.get_fields()) - set(table_fields)):
            raise Sqlite3ApiError(
                f'Не переданы значения для полей: {", ".join(_fields)}'
            )

        return self.__api.insert(
            table_name=self.table_name,
            **table_fields
        )

    def create_table(self) -> str:
        """
        Создание таблицы.
        :return: "Successfully"
        """

        return self.__api.create_table(
            table_name=self.table_name,
            **self.get_fields()
        )

    def add_field(self, field_name: str, start_value=None) -> str:
        """
        Добавляет поле в таблицу.
        :param field_name: Название нового поля.
        :param start_value: Значение нового поля.
        :return: "Successfully"
        """

        if not (field_type := self.get_fields().get(field_name)):
            raise Sqlite3ApiError(
                f'Поле `{field_name}` не найдено '
                f'в классе таблицы `{self.table_name}`'
            )

        if start_value is None:
            if (start_value := vars(self.__class__).get(field_name)) is None:
                raise Sqlite3ApiError(
                    f'Не указано значение по умолчанию для поля `{field_name}`'
                )

        return self.__api.add_field(
            table_name=self.table_name,
            field_name=field_name, field_type=field_type,
            start_value=start_value
        )

    def get_class(self, data) -> Table:
        """
        Получаем объект, основываясь на данных, полученных из бд.
        :param data: Данные об объекте.
        :return: Объект класса таблицы.
        """

        fields = dict(id=data[0])
        for field_name, value in zip(self.get_fields(), data[1:]):
            fields[field_name] = value
        return self.__class__(**fields, _api=self.__api)

    @classmethod
    def get_fields(cls):
        """
        Получаем поля и их типы данных.
        """

        types = {'str': 'TEXT', 'int': 'INTEGER'}
        return {
            field_name: (
                field_type.lower()
                if field_type not in types else
                types[field_type]
            )
            for field_name, field_type
            in vars(cls)['__annotations__'].items()
        }

    @property
    def table_name(self):
        """ Название таблицы """

    @table_name.getter
    def table_name(self) -> str:
        """ Получение названия таблицы """

        return type(self).__name__.lower()

    def __repr__(self):
        return '{table_name} OBJECT\n{fields}'.format(
            table_name=self.table_name.upper(),
            fields='\n'.join(
                f'{k}={v}' for k, v in vars(self).items()
                if not k.startswith('_Table_')
            )
        )

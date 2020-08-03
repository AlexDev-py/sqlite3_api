from typing import Tuple, Literal, Union, List, Dict
from .api import Sqlite3
from .tools import *
from .Table import Table


class Sqlite3ApiError(Exception):
    """ Ошибки, которые возникают при работе API """


class API(Sqlite3):

    def __init__(self, tables, db_path: str = None):
        self._active = False

        if db_path:
            Sqlite3.__init__(self, db_path)
            self._active = True

        if type(tables).__name__ != 'module':
            raise Sqlite3ApiError(
                'Параметр `tables` должен быть '
                'импортированным файлом с классами таблиц'
            )

        self._tables: Dict[str, Table] = tables
        self._get_tables()

    def save(self, *table_classes) -> str:
        """
        Сохраняем все изменения.
        :param table_classes: Объекты полученные из базы данных.
        :return: "Successfully"
        """

        self._check_active()

        if len(table_classes) == 0:
            raise Sqlite3ApiError('Не переданы классы таблиц')
        table_classes: Tuple[Table]

        for table_class in table_classes:
            updated_fields = []  # Поля, которые изменили
            old_table_class = self.filter(
                table_name=type(table_class).__name__.lower(),
                return_type='classes',
                id=table_class.id
            )  # Старые данные

            # Проверяем какие поля были изменены
            for field_name, value in vars(table_class).items():
                if not field_name.startswith('_'):
                    if value != old_table_class.__getattribute__(field_name):
                        updated_fields.append('{field_name}={value}'.format(
                            field_name=field_name,
                            value=convert_from_class(value)
                        ))

            if len(updated_fields) != 0:
                self.execute(
                    "UPDATE '%s' SET %s WHERE id = %s" % (
                        type(table_class).__name__.lower(),
                        ', '.join(updated_fields),
                        table_class.id
                    ))
                self.commit()

        return 'Successfully'

    def filter(
            self,
            table_name: str,
            return_type: Literal['visual', 'classes'] = 'visual',
            return_list: Literal[True, False] = False,
            **where
    ) -> Union[
        List[list], list,
        List[Table], Table,
        None
    ]:
        """
        Функция выбирает данные из базы данных на основе указанных параметров.
        :param table_name: Название таблицы, с которой мы работаем.
        :param return_type:
            Для "classes" - вернёт объект класса таблицы.
            Для "visual" - вернёт данные в том виде,
                в котором они хранятся в базе данных.
        :param return_list:
            Для True - вернёт список объектов независимо от их количества.
        :param where: Параметры сортировки
        """

        self._check_active()

        table_name = table_name.lower()
        table = self._get_table(table_name)
        table_fields = table.get_fields()
        conditions = []

        # Формирование параметров сортировки
        for key, value in where.items():
            if '_' in key:
                index = key.rfind('_')
                try:
                    field = key[:index]
                    opt = OPT_MAP[key[index + 1:]]
                except KeyError:
                    field = key
                    opt = '='
            else:
                field = key
                opt = '='

            if field not in table_fields and field != 'id':
                raise Sqlite3ApiError(
                    f'Поле `{field}` не найдено в таблице `{table_name}`'
                )

            conditions.append(
                f'{field} {opt} {str(convert_from_class(value))}'
            )

        # Получение данных
        if len(conditions) != 0:
            data = self.fetchall(
                "SELECT * FROM '%s' WHERE %s" % (
                    table_name,
                    ' and '.join(conditions)
                ))
        else:
            data = self.fetchall(
                "SELECT * FROM '%s'" % table_name
            )

        if len(data) == 0:
            return

        if return_type == 'visual':
            if return_list:
                return data if isinstance(data, list) else [data]

            return data[0] if len(data) == 1 else data

        elif return_type == 'classes':
            data = data if isinstance(data, list) else [data]
            classes = [self.get_class(table_name, cls) for cls in data]

            if not return_list:
                return classes[0] if len(classes) == 1 else classes

            return classes

    def insert(self, table_name: str, **values) -> str:
        """
        Функция добавляет данные в таблицу.
        :param table_name: Название таблицы, с которой мы работаем.
        :param values: Значения полей.
        :return: "Successfully"
        """

        self._check_active()

        table_name = table_name.lower()
        table = self._get_table(table_name)
        table_fields = table.get_fields()
        fields = table_fields.copy()

        for filed, value in values.items():
            if filed not in table_fields:
                raise Sqlite3ApiError(
                    f'Поле `{filed}` не найдено в таблице `{table_name}`'
                )

            fields[fields.index(filed)] = str(convert_from_class(value))
            table_fields.remove(filed)

        if len(table_fields) != 0:
            raise Sqlite3ApiError(
                f'Не переданы значения для полей: '
                f'{", ".join(table_fields)}'
            )

        self._cursor.execute(
            "INSERT INTO '%s' (%s) VALUES (%s)" % (
                table_name,
                ', '.join(table.get_fields()),
                ', '.join(fields)
            ))
        self.commit()

        return 'Successfully'

    def get_class(self, table_name: str, data: Union[list, tuple]) -> Table:
        """
        Возвращает объект класса таблицы на основе его данных `data`
        :param table_name: Название таблицы с, которой мы работаем.
        :param data: Данные которые хранились в базе данных.
        """

        table = self._get_table(table_name.lower())
        types = table.get_types()
        fields = table.get_fields()
        table.__setattr__('id', data[0])
        data = data[1:]

        for i, field in enumerate(fields):
            if types[field][1] in ['list', 'dict']:
                table.__setattr__(
                    field,
                    convert(convert_from_data(data[i]))
                )
            else:
                table.__setattr__(
                    field,
                    convert_from_data(data[i])
                )

        return table

    def add_field(self, table_name: str, field_name: str, start_value) -> str:
        """
        Добавляет поле в таблицу.
        :param table_name: Название таблицы, с которой мы работаем.
        :param field_name: Название нового поля.
        :param start_value: Значение нового поля.
        :return: "Successfully"
        """

        self._check_active()

        table_name = table_name.lower()
        table = self._get_table(table_name)
        table_fields = table.get_fields()

        if field_name not in table_fields:
            raise Sqlite3ApiError(
                f'Поле `{field_name}` не найдено '
                f'в классе таблицы `{table_name}`'
            )

        self._cursor.execute(
            "ALTER TABLE '%s' ADD %s %s" % (
                table_name,
                field_name,
                table.get_types()[field_name][0]  # Тип данных
            ))  # Добавление нового поля
        self._cursor.execute(
            "UPDATE '%s' SET %s = %s" % (
                table_name,
                field_name,
                str(convert_from_class(start_value))
            ))  # Изменение стартового значения
        self.commit()

        return 'Successfully'

    def create_db(self) -> str:
        """
        Создание таблиц.
        :return: "Successfully"
        """

        self._check_active()

        for table_name, table in self._tables.items():
            fields = [
                f'{key}{value[0]}'
                for key, value in table.get_types().items()
                if key != 'id' and not key.startswith('__')
            ]

            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS %s "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, %s)" % (
                    table_name,
                    ', '.join(fields)
                ))

        return 'Successfully'

    def _get_tables(self):
        excluded = [
            'string', 'integer', 'list_', 'dict_', 'Table', 'data_bases',
            'Dict', 'List'
        ]
        tables = {
            k.lower(): v
            for k, v in vars(self._tables).items()
            if not k.startswith('__') and k not in excluded
        }

        self._tables_names: List[str] = [
            name for name in tables.keys()
        ]
        self._tables = tables

    def _check_active(self):
        if not self._active:
            raise Sqlite3ApiError('Файл базы данных не инициализирован')

    def _get_table(self, table_name: str) -> Table:
        if table_name in self._tables_names:
            return self._tables[table_name]()
        else:
            raise Sqlite3ApiError(f'Таблица `{table_name}` не найдена')

    @property
    def cursor(self):
        """ Sqlite3 cursor """

    @cursor.getter
    def cursor(self):
        """ Получение курсора """

        self._check_active()
        return self._cursor

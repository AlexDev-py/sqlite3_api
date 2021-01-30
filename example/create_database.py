"""

В этом файле создадим базу данных.

NEXT: insert_data.py

"""

# Импортируем наши таблицы
from sqlite3_api.example.my_tables import Students, Points
from sqlite3_api import API

"""
Для инициализации наших таблиц, необходимо создать объект класса.
Мы можем сделать это двумя способами:
    1. Указать путь к файлу базы данных.
        Тогда создастся новое подключение.
    2. Мы можем передать уже созданное подключение в аргумент `_api`.
Здесь мы будем использовать второй способ.
"""

sql = API('example.db')  # Создаем подключение к базе данных.
students = Students(_api=sql)  # Инициализируем таблицу `Students`
points = Points(_api=sql)  # Инициализируем таблицу `Points`

# Доказывает, что таблицы используют одно и то же подключение
# print(students._api is points._api)

# Создаем таблицы
print('Создание таблицы `Students`: ', students.create_table())
print('Создание таблицы `Points`: ', points.create_table())

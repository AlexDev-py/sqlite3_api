"""

В этом файле создадим базу данных.
Все таблицы берутся только из файла, который нам нужно импортировать в этот файл
После создания таблиц, обратитесь к файлу insert_data.py

"""

from sqlite3_api.test import my_tables  # Импортируем файл с классами таблиц
from sqlite3_api import *

"""
    Первым аргументом указываем файл с классами таблиц,
    вторым аргументом указываем путь к файлу(если файл не найден, создается автомитически)
"""
sql = API(my_tables, 'test.db')
result = sql.create_db()  # Создаем таблицы
print(result)

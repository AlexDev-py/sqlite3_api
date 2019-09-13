"""

В этом файле создадим базу данных.
Все таблицы берутся только из файла tables.py
После создания таблиц, обратитесь к файлу insert_data.py

"""

from sqlite3_api import *

# Указываем путь к файлу(если файл не найден, создается автомитически)
sql = API('test.sqlite')
result = sql.create_db()
print(result)

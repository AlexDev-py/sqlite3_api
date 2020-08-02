"""

Загрузим данные в наши таблицы

NEXT: main.py

"""

from sqlite3_api.example import my_tables  # Импортируем таблицы
from sqlite3_api import API

sc = 'schoolchildren'
st = 'students'

sql = API(my_tables, 'example.db')

"""
При добавлении данных нужно указать название таблицы и все её поля
"""

sql.insert(
    table_name='schoolchildren',
    first_name='Bob',
    last_name='Gray',
    age=14,
    cls=8,
    evaluation=[5, 5, 4, 5]
)

# В список так же можно добавлять строки, например [1, 'abc']
sql.insert(
    table_name='schoolchildren',
    first_name='Joni',
    last_name='Dep',
    age=14,
    cls=8,
    evaluation=[5, 5, 5, 5]
)
sql.insert(
    table_name='schoolchildren',
    first_name='Max',
    last_name='Brown',
    age=16,
    cls=10,
    evaluation=[5, 3, 4, 5]
)

sql.insert(
    table_name='students',
    first_name='Robin',
    last_name='Green',
    age=21,
    course=1,
    salary=500
)
sql.insert(
    table_name='students',
    first_name='Max',
    last_name='Red',
    age=25,
    course=3,
    salary=2000
)

print('Successfully')

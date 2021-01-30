"""

Загрузим данные в наши таблицы

NEXT: main.py

"""

# Импортируем таблицы
from sqlite3_api.example.my_tables import Students, Points
# Импортируем типы данных
from sqlite3_api.example.my_tables import Position
from sqlite3_api.types import List


# Используем 1-й способ инициализации
students = Students('example.db')  # Инициализируем таблицу `Students`
points = Points('example.db')  # Инициализируем таблицу `Points`

# Не вызовет исключений даже если таблицы уже созданы
students.create_table()
points.create_table()

# Доказывает, что таблицы используют разное подключение
# print(students._api is points._api)

# Заполняем таблицу `students`
students.insert(
    first_name='Bob',
    last_name='Gray',
    age=20,
    # аргументы `по умолчанию` можно не указывать
    # course=1,
    # salary=5000,
    # Значение заменит то, которое стоит `по умолчанию`
    marks=List([5, 5, 4, 5])
)

students.insert(
    first_name='Max',
    last_name='Brown',
    age=23,
    course=3,
    salary=10000,
    # !!! Не забывайте передавать тот тип данных,
    # который указывали при создании класса
    marks=List([5, 5, 5, 5])
)

students.insert(
    first_name='Joni',
    last_name='Dep',
    age=20,
    marks=List([5, 3, 4, 5]),
    salary=3500
)

# Заполняем таблицу `points`

points.insert(
    position=Position(x=1.2, y=6.9),
    size=2
)

# Создаст объект, полностью опираясь на значения `по умолчанию`
points.insert()

points.insert(position=Position(1, 1.1))

print('Successfully')

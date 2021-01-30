"""

Сначала зайдите в файл my_tables.py

"""

from typing import List
from sqlite3_api.example.my_tables import Students, Points

# Используем 1-й способ инициализации
students = Students('example.db')  # Инициализируем таблицу `Students`
points = Points('example.db')  # Инициализируем таблицу `Points`

print('\n      Просмотрим все данные в таблице Students')
# `return_list=True` - вернет список, даже если найден всего один объект
for obj in students.filter(return_list=True):
    print(obj, '\n')

print('\n      Просмотрим все данные в таблице Points')
for obj in points.filter(return_list=True):
    print(obj, '\n')

print(
    '      Как видим у всех объектов есть свой `id`.'
    '\n      Он создаётся автоматически и никогда не повторяется.'
)
print(
    '\n      При фильтрации можно указывать действие(=, !=, >, <, >=, <=),\n'
    '      сделать это можно вот так:\n'
    '      age_no=14, данное выражение будет означать age != 14\n'
    '      так же и с другими действиями\n'
    '      no - !=, gt - >, lt - <, egt - >=, elt - <=\n'
    '      ! Поле и действие должны отделяться подчеркиванием !'
)

print('\n      Получим студентов младше 22 лет')
for obj in students.filter(age_lt=22):
    print(obj, '\n')

print(
    '      Допустим у Макса(id=3) было день рождение,\n'
    '      нам нужно изменить его возраст в базе данных.\n'
    '      Для этого нам нужно получить его данные:'
)
obj = students.filter(
    first_name='Max', last_name='Brown'
)
print(obj)

print(
    '\n      Просмотрим возраст Макса,\n'
    '      для этого воспользуемся объектом класса который получили ранее:'
)
print(f'{obj.age=}')

print('\n      Изменим его возраст')
obj.age += 1
print(f'{obj.age=}')

print(
    '\n      Сохраним изменения, используя метод `save`'
)
print(f'{obj.save()=}')

print(
    '\n      Сделаем то же самое с остальными учениками.'
    '\n      Но в этот раз будем использовать метод `update`.\n'
)

for obj in students.filter(first_name_no='Max', last_name_no='Brown'):
    print(f'{obj.id=}', f'{obj.update(age=obj.age + 1)=}')

print('\n      Попробуем получить список всех учеников с именем Bob:')

# `return_type=visual` вернёт массив данных объекта
# `return_type=classes` вернёт массив объект класса
print(students.filter(return_type='visual', first_name='Bob'))

print(
    '\n      Как мы видим это не список, а просто объект.\n'
    '      Что бы получить список нужно указать параметр `return_list=True`'
)

print(students.filter(
    return_type='visual', return_list=True, first_name='Bob'
))

print('\n      Посмотрим на таблицу в целом')
for obj in students.filter(return_list=True):
    print(obj, '\n')


print('\n\n      Начнем работу с таблицей Points\n')
print('\n      Получим все точки, которые находятся не на нулевых координатах')
objects: List[Points] = points.filter(
    return_list=True, position_no='0;0'
)

for obj in objects:
    print(obj, '\n')

print('\n      Увеличим их размер')
for obj in objects:
    print(f'{obj.id=}', f'{obj.update(size=obj.size + 1)=}')

print(
    '\n      Получим точки, размер которых не превышает 2, '
    'и сделаем их зелёными'
)
for obj in points.filter(return_list=True, size_elt=2):
    print(f'{obj.id=}', f'{obj.update(color="green")=}')

print('\n      Изменим позицию первой точки')
obj = points.filter(id=1)
print(f'{obj.position=}')
obj.position += (0.8, 3.1)
print(f'{obj.position=}')
print(f'{obj.save()=}')

print('\n      Посмотрим на таблицу в целом')
for obj in points.filter(return_list=True):
    print(obj, '\n')

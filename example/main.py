"""

Сначала зайдите в файл my_tables.py

"""

from sqlite3_api.example import my_tables
from sqlite3_api import *

sc = 'schoolchildren'
st = 'students'

sql = API(my_tables, 'example.db')  # Инициализация

print('\n      Просмотрим все данные в таблице SchoolChildren')
print(sql.filter(sc))
print('\n      Просмотрим все данные в таблице Students')
print(sql.filter(st))

print(
    '\n      При фильтрации можно указывать действие(=, !=, >, <, >=, <=),\n'
    '      сделать это можно вот так:\n'
    '      age_no=14, данное выражение будет означать age != 14\n'
    '      так же и с другими действиями\n'
    '      no - !=, gt - >, lt - <, egt - >=, elt - <=\n'
    '      ! Поле и действие должны отделяться подчеркиванием !'
)

print('\n      Получим учеников старше 14 лет')
print(sql.filter(sc, age_gt=14))

print(
    '\n      Допустим у Макса было день рождение,\n'
    '      нам нужно изменить его возраст в базе данных.\n'
    '      Для этого нам нужно получить его данные в виде класса:'
)
data = sql.filter(
    sc, return_type='classes',
    first_name='Max', last_name='Brown'
)
print(data)

print(
    '\n      Если мы попробуем вывести `data`, то получим объект класса.\n'
    '      Что бы увидеть всю информацию воспользуемся методом `get_visual` '
    'из пакета sqlite3_api.tools.\n'
    '      Вот результат:'
)

print(get_visual(data))

print(
    '\n      Просмотрим возраст Макса,\n'
    '      для этого воспользуемся объектом класса который получили ранее:'
)
print(data.age)

print('\n      Изменим его возраст')

data.age += 1
print(data.age)

print(
    '\n      Сохраним изменения, передав в команду save() объект класса Макса'
)

print(sql.save(data))

print('\n      Сделаем то же самое с остальными учениками\n')

bob, joni = sql.filter(sc, 'classes', age=14)
print(get_visual(bob))
print(get_visual(joni))

bob.age += 1
joni.age += 1

print(
    '\n      Сохранять можно сразу несколько объектов,\n'
    '      нужно просто передать их в функцию save'
)

print(sql.save(bob, joni))

print('\n      Попробуем получить список всех учеников с именем Bob:')

print(sql.filter(sc, 'classes', first_name='Bob'))

print(
    '\n      Как мы видим это не список, а просто объект.\n'
    '      Что бы получить список нужно указать параметр return_list=True'
)

print(sql.filter(sc, 'classes', return_list=True, first_name='Bob'))

print(
    '\n\n      Такие же действия можно произвести '
    'со студентами в таблице students'
)

robin, max_ = sql.filter(st, 'classes')
print(get_visual(robin))
print(get_visual(max_))

robin.course += 1
robin.salary += 500

max_.age += 1
max_.course += 1
max_.salary += 500

print(sql.save(max_, robin))

print('\n      Снова просмотрим все данные')

print(sql.filter(sc))
print(sql.filter(st))

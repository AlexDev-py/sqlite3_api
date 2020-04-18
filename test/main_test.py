from sqlite3_api.test import my_tables
from sqlite3_api import *

sc = 'schoolchildren'
st = 'students'

sql = API(my_tables, 'test.db')  # Инициализация

print("""      просмотрим все данные в таблице SchoolChildren""")
print(sql.filter(sc))
print("""      просмотрим все данные в таблице Students""")
print(sql.filter(st))

print("""
      При фильтрации можно указывать действие(=, !=, >, <, >=, <=), сделать это можно вот так: 
      age_no=14, данное выражение будет означать age != 14,
      так же и с другими действиями(no - !=, gt - >, lt - <, egt - >=, elt - <=),
      поле и действие должны отделяться подчеркиванием
""")

print()
print("""Получим учеников старше 14 лет""")
print(sql.filter(sc, age_gt=14))

print("""
      Допустим у Макса было день рождение, нам нужно изменить его возраст в базе данных.
      Для этого нам нужно получить его данные в виде класса.
""")

data = sql.filter(sc, 'classes', first_name='Max', last_name='Brown')
print(data)

print("""
      Если мы попробуем вывести data, то получим объект класса,
      что увидеть всю информацию воспользуемся методом get_visual
""")

print(get_visual(data))

print("""
      Просмотрим возраст Макса, для этого воспользуемся объектом класса который получили ранее
""")

print(data.age)

print("""      Изменим его возраст""")

data.age += 1
print(data.age)

print("""
      Сохраним изменения, передав в команду save() объект класса Макса
""")

print(sql.save(data))

print("""
      Сделаем то же самое с остальными учениками
""")

bob, joni = sql.filter(sc, 'classes', age=14)
print()
print(get_visual(bob))
print(get_visual(joni))

bob.age += 1
joni.age += 1

print("""
      Сохранять можно сразу несколько объектов, нужно просто передать их в функцию save
""")

print(sql.save(bob, joni))

print("""
      Попробуем получить список всех учеников с мименем Bob
""")

print()
print(sql.filter(sc, 'classes', first_name='Bob'))

print("""
      Как мы видим это не список, а просто объект, для этого нужно указать параметр return_list=True
""")

print(sql.filter(sc, 'classes', return_list=True, first_name='Bob'))

print("""
      Такие же действия можно произвести со студентами в таблице students
""")

robin, max_ = sql.filter(st, 'classes')
print(get_visual(robin))
print(get_visual(max_))

robin.course += 1
robin.salary += 500

max_.age += 1
max_.course += 1
max_.salary += 500

print(sql.save(max_, robin))

print("""
      Снова просмотрим все данные
""")

print(sql.filter(sc))
print(sql.filter(st))

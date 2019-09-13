from sqlite3_api import *


sc = 'schoolchildren'
st = 'students'

sql = API('test.sqlite')  # Инициализация

# просмотрим все данные в таблице SchoolChildren
print(sql.select(sc))
# просмотрим все данные в таблице Students
print(sql.select(st))

"""
    При фильтрации можно указывать действие(=, !=, >, <, >=, <=), сделать это можно вот так: 
    age_no=14, данное выражение будет означать age != 14,
    так же и с другими действиями(no - !=, gt - >, lt - <, egt - >=, elt - <=),
    поле и действие должны отделяться подчеркиванием
"""
# Получим учеников старше 14 лет
print()
print(sql.filter(sc, age_gt=14))
"""
Допустим у Макса было день рождение, нам нужно изменить его возраст в базе данных.
Для этого нам нужно получить его данные в виде класса.
"""

data = sql.filter(sc, 'classes', first_name='Max', last_name='Brown')
print(data)
"""
Если мы попробуем вывести data, то получим объект класса,
что увидеть всю информацию воспользуемся методом get_visual
"""
print(get_visual(data))
"""
Просмотрим возраст Макса, для этого воспользуемся объектом класса который получили ранее
"""
print(data.age)
"""
Изменим его возраст
"""
data.age += 1
print(data.age)
"""
Сохраним изменения, передав в команду save() объект класса Макса
"""
sql.save(data)
"""
Сделаем тоже самое с остальными учениками
"""
bob, joni = sql.filter(sc, 'classes', age=14)
print()
print(get_visual(bob))
print(get_visual(joni))

bob.age += 1
joni.age += 1

"""
Сохранять можно сразу несколько объектов, нужно просто передать их в функцию save
"""
sql.save(bob, joni)

"""
Такие же действия можно произвести со студентами в таблице students
"""
robin, max_ = sql.filter(st, 'classes')
print(get_visual(robin))
print(get_visual(max_))

robin.course += 1
robin.salary += 500

max_.age += 1
max_.course += 1
max_.salary += 500

sql.save(max_, robin)

"""
Снова просмотрим все данные
"""
print(sql.select(sc))
print(sql.select(st))

"""

Файл с таблицами можно назвать как угодно.
Строчка `from sqlite3_api.tables import *` должна быть обязательна,
 она импортирует родительский класс таблиц и типы данных.

WARNING: Других переменных и импортов быть не должно

Для того чтобы API могло нормально работать с классами таблиц,
 нужно создать эти классы.
Для того чтобы определить тип столбца используем типы из файла tools.py,
 всего доступно 5 типов данных:
    текст(text()),
    строка(string()),
    число(integer()),
    список(list_()),
    словарь(dict_())
 Подробнее о них можно узнать в файле tools.py

Если первые 3 есть в sqlite3, то последних нет.
В таблице они определяются как - TEXT,
 но при команде filter с параметром return_type='classes',
 поля с этом типом данных конвертируются в список или словарь.

NEXT: create_database.py

"""

from sqlite3_api.Table import *


class SchoolChildren(Table):
    first_name = string()
    last_name = string()
    age = integer()
    cls = integer()
    evaluation = list_()


class Students(Table):
    first_name = string()
    last_name = string()
    age = integer()
    course = integer()
    salary = integer()

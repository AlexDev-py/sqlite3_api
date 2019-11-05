"""

Файл с таблицами можно назвать как угодно.
Строчка "from sqlite3_api.tables import *" должна быть обязательна, она импортирует родительский класс таблиц и
типы данных.
WARNING: Поле id в классе должно быть обязательно!!!

Для того чтобы API могло нормально работать с классами таблиц, нужно создать эти классы.
Для того чтобы определить тип столбца используем типы из файла utils.py, всего доступно 4 типа данных:
строка(string()), число(integer()), список(list_()), словарь(dict_()).
Если первые 2 есть в sqlite3, то последних нет. В таблице они определяется как - TEXT,
но при команде filter с параметром ret_type='classes',
поля с этом типом данных конвертируются в список или словарь.

После полного оформления этого файла обратитесь к файлу create_database.py в папке test

"""

from sqlite3_api.Table import *


class SchoolChildren(Table):
    id = None
    first_name = string()
    last_name = string()
    age = integer()
    cls = integer()
    evaluation = list_()


class Students(Table):
    id = None
    first_name = string()
    last_name = string()
    age = integer()
    course = integer()
    salary = integer()

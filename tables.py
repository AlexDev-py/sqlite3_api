"""

Для того чтобы API могло нормально работать с классами таблиц, нужно создать эти классы.
Для того чтобы определить тип столбца используем типы из файла utils.py, всего доступно 3 типа данных:
строка(string()), число(integer()) и список(list_()).
Если первые 2 есть в sqlite3, то последнего нет. В таблице он определяется как - TEXT,
но при команде filter с параметром ret_type='classes',
поля с этом типом данных конвертируются в список.

WARNING: Поле id должно быть обязательно!!!

После создания классов таблиц нам нужно передать их в переменую data_bases.
После чего создать функцию get(table_name). Сделать её нужно такой же как и в этом файле.
Обратите внимание, названия классов в этой функции должны быть написанны строчными буквами.

После полного оформления этого файла обратитесь к файлу create_database.py в папке test

"""

from .utils import *


class SchoolChildren:
    def __init__(self):
        self.id = None

        self.first_name = string()
        self.last_name = string()
        self.age = integer()
        self.cls = integer()
        self.evaluation = list_()


class Students:
    def __init__(self):
        self.id = None

        self.first_name = string()
        self.last_name = string()
        self.age = integer()
        self.course = integer()
        self.salary = integer()


data_bases = [SchoolChildren(), Students()]


def get(table_name):
    if table_name == 'schoolchildren':
        return SchoolChildren()
    elif table_name == 'students':
        return Students()

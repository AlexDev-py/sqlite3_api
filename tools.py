from ast import literal_eval


def text():
    """
    Строковое поле(Для длинного текста)
    Для обозначения типа данных в таблице
    """

    return [f" TEXT", 'str']


def string(max_length=100):
    """
    Строковое поле.
    Для обозначения типа данных в таблице.
    :param max_length: Максимальная длина строки
        (если текст большой лучше использовать тип `text`)
    """

    return [f" VARCHAR({max_length})", 'str']


def integer():
    """
    Числовое поле
    Для обозначения типа данных в таблице
    """

    return [" INTEGER", 'int']


def list_():
    """
    Поле типа `list`
    Для обозначения типа данных в таблице
    """

    return [" TEXT", 'list']


def dict_():
    """
    Поле типа `dict`
    Для обозначения типа данных в таблице
    """

    return [" TEXT", 'dict']


def convert_from_data(value):
    """ Получаем данные для представления класса """

    if isinstance(value, (str, list, dict)):
        value = '{}'.format(str(value).replace("`", "'"))

    return value


def convert_from_class(value):
    """ Получаем данные для сохранения в базу данных """

    if isinstance(value, (str, list, dict)):
        value = "'{}'".format(str(value).replace("'", "`"))

    return value


def get_visual(obj):
    """
    Получаем данные в том виде,
    в котором они хранятся в базе данных
    """

    if isinstance(obj, list):
        return [[i for i in vars(obj_class).values()] for obj_class in obj]

    return [i for i in vars(obj).values()]


def convert(obj):
    """ Конвертируем строку в список или словарь """

    return literal_eval(obj)


# Постфиксы для выражения действий при вызове метода `filter`.
# filter(table_name, filed_no=1, filed2_egt=5)
# Получится запрос “SELECT * FROM table_name WHERE filed != 0 AND field2 >= 5”
OPT_MAP = {
    'gt': '>',
    'lt': '<',
    'no': '!=',
    'egt': '>=',
    'elt': '<=',
}

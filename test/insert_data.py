"""

Загрузим данные в наши таблицы
После этого файла, обратитесь к main_test.py

"""

from sqlite3_api import API

sc = 'schoolchildren'
st = 'students'

sql = API('test.sqlite')

""" При добавлении данных нужно указать название таблицы и все поля как показано ниже """
sql.insert(sc, first_name='Bob', last_name='Gray', age=14, cls=8, evaluation=[5, 5, 4, 5])
# В список так же можно помещять строки, например [1, 'abc']
sql.insert(sc, first_name='Joni', last_name='Dep', age=14, cls=8, evaluation=[5, 5, 5, 5])
sql.insert(sc, first_name='Max', last_name='Brown', age=16, cls=10, evaluation=[5, 3, 4, 5])

sql.insert(st, first_name='Robin', last_name='Green', age=21, course=1, salary=500)
sql.insert(st, first_name='Max', last_name='Red', age=25, course=3, salary=2000)

print('Successfully')

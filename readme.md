Installation
------------

Install from [PyPi](https://pypi.org/project/sqlite3-api)

    pip install sqlite3-api


Install from [GitHub](https://github.com/AlexDev-py/sqlite3_api.git)

    git clone https://github.com/AlexDev-py/sqlite3_api.git

Create table classes
--------------------

    import sqlite3_api.Table as TableTemplate

    class MyTable(TableTemplate.Table):
        my_first_field = TableTemplate.string()
        my_second_field = TableTemplate.integer()

In file 
[example/my_tables.py](https://github.com/AlexDev-py/sqlite3_api/blob/master/example/my_tables.py),
there is an instruction to create classes(in Russian language)

Using
------------

Import file with tables::

    import my_tables

Import package::

    import sqlite3_api

Initiate the database::

    sql = sqlite3_api.API(my_tables, 'file_name.db')

Create tables::

    sql.create_db()

Getting data::

    table_name = 'test_table'
    data = sql.filter(table_name)

Sorting data::

    table_name = 'test_table'
    data = sql.filter(table_name, field_name='value')


More information in the 
[example folder](https://github.com/AlexDev-py/sqlite3_api/tree/master/example)

VK: [AlexDev](https://vk.com/sys.exit1)
Installation
------------

Install from [PyPi](https://pypi.org/project/sqlite3-api)

    pip install sqlite3-api


Install from [GitHub](https://github.com/AlexDev-py/sqlite3_api.git)

    git clone https://github.com/AlexDev-py/sqlite3_api.git

Create table classes
--------------------

    from sqlite3_api.Table import Table

    class MyTable(Table):
        my_first_field: str
        my_second_field: int

In file 
[example/my_tables.py](https://github.com/AlexDev-py/sqlite3_api/blob/2.0.0/example/my_tables.py),
there is an instruction to create classes(in Russian language)

Using
------------

Initiate the database:

    from my_tables import MyTable 
    my_table = MyTable('MyDataBase.sqlite')

Create tables:

    my_table.create_table()

Inserting data:

    my_table.insert(
        my_first_field='first',
        my_second_field='second',
    )

Getting data:

    data = my_table.filter()

Sorting data:

    data = my_table.filter(my_field='value')


More information in the 
[example folder](https://github.com/AlexDev-py/sqlite3_api/tree/2.0.0/example)

VK: [AlexDev](https://vk.com/sys.exit1)
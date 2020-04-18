from .api import Sqlite3
from .utils import *


class SqlApiError(Exception):
    pass


class API(Sqlite3):
    def __init__(self, tables, db_path=None):
        self._active = False
        if db_path:
            Sqlite3.__init__(self, db_path)
            self._active = True
        self._databases = tables
        if type(self._databases).__name__ != 'module':
            raise SqlApiError("The tables_file option should be imported file with table classes")
        self._get_databases()

    def save(self, *table_classes, table_classes_=()):
        """
        Saves all changes
        :param table_classes: Object or objects received by filter function
        :param table_classes_: Object or objects received by filter function
        :return: Successfully
        """

        self._check_active()
        table_classes = table_classes_ if len(table_classes) == 0 else table_classes
        if len(table_classes) != 0:
            for table in table_classes:
                fields = []
                old_table = self.filter(type(table).__name__.lower(), 'classes', id=table.id)
                for key, value in vars(table).items():
                    if key != 'id':
                        if value != get_field(old_table, key):
                            fields.append('{}={}'.format(key, convert_from_class(value)))
                if len(fields) != 0:
                    self._cursor.execute("UPDATE '%s' SET %s WHERE id = %s" % (type(table).__name__.lower(),
                                                                               str(', '.join(fields)), table.id))
                    self.commit()
            return 'Successfully'

        else:
            raise SqlApiError('Not transferred to the pill classes')

    def filter(self, table_name, return_type='visual', return_list=False, **where):
        """
        The function selects data from the database based on the specified parameters
        :param table_name: Table name
        :type table_name: str
        :param return_type: Return the item of class of data received if you specify "classes",
         if you specify "visual" return the list of data
        :type return_type: str
        :param return_list: If True, return the list not depending on the number of objects
        :type return_list: bool
        :param where: Filtering options
        :return: list or object
        """

        self._check_active()
        table_name = table_name.lower()
        obj = self._get_obj(table_name)
        obj_fields = obj.get_fields()
        condition = []

        for key, value in where.items():
            if '_' in key:
                index = key.rfind('_')
                try:
                    field = key[:index]
                    opt = opt_map[key[index + 1:]]
                except KeyError:
                    field = key
                    opt = '='
            else:
                field = key
                opt = '='
            if field not in obj_fields and field != 'id':
                raise SqlApiError(f'Field {field} not found in table {table_name}')
            value = convert_from_class(value)
            condition.append("{} {} {}".format(field, opt, str(value)))

        if len(condition) != 0:
            data = self.execute("SELECT * FROM '%s' WHERE %s" % (table_name, ' and '.join(condition)))
        else:
            data = self._select(table_name)

        if len(data) == 0:
            return

        if return_type == 'visual':
            if return_list:
                return data if type(data).__name__ == 'list' else [data]
            return data[0] if len(data) == 1 else data

        elif return_type == 'classes':
            data = data if type(data).__name__ == 'list' else [data]
            classes = []
            for cls in data:
                classes.append(self.get_class(table_name, cls))
            if not return_list:
                return classes[0] if len(classes) == 1 else classes
            return classes

    def insert(self, table_name, **values):
        """
        The function adds data to the table
        :param table_name: Table name
        :param values: Values of the columns
        :return: Successfully
        """

        self._check_active()
        table_name = table_name.lower()
        obj = self._get_obj(table_name)
        obj_fields = obj.get_fields()
        fields = [i for i in obj_fields]

        for key, value in values.items():
            if key not in obj_fields:
                raise SqlApiError(f'Field {key} not found in table {table_name}')
            fields[fields.index(key)] = str(convert_from_class(value))
            obj_fields.remove(key)

        if len(obj_fields) != 0:
            raise SqlApiError(f'No value{"s" if len(obj_fields) > 1 else ""} for'
                              f' field{"s" if len(obj_fields) > 1 else ""}: {", ".join(obj_fields)}')

        self._cursor.execute("INSERT INTO '%s' (%s) VALUES (%s)" % (table_name,
                                                                    ', '.join(obj.get_fields()),
                                                                    ', '.join(fields)))
        self.commit()
        return 'Successfully'

    def get_class(self, table_name, data):
        """
        Returns table class object based on its data
        :param table_name: Table name
        :param data: Data obtained by metod Filter
        :return: Table class
        """

        obj = self._get_obj(table_name.lower())
        types = obj.get_types()
        fields = obj.get_fields()
        obj.__dict__['id'] = data[0]
        data = data[1:]

        for i in range(len(fields)):
            if types[fields[i]][1] == 'list' or types[fields[i]][1] == 'dict':
                obj.__dict__[fields[i]] = convert(convert_from_data(data[i]))
            else:
                obj.__dict__[fields[i]] = convert_from_data(data[i])

        return obj

    def add_field(self, table_name, field_name, start_value):
        """
        Adds a field to the table
        :param table_name: Table name
        :param field_name: Field name
        :param start_value: The starting value of this field
        :return: Successfully
        """

        self._check_active()
        table_name = table_name.lower()
        obj = self._get_obj(table_name)
        obj_fields = obj.get_fields()

        if field_name not in obj_fields:
            raise SqlApiError(f'Field {field_name} not found in table class')

        self._cursor.execute("ALTER TABLE '%s' ADD %s %s" % (table_name, field_name,
                                                             obj.get_types()[f'{field_name}'][0]))
        self.commit()
        self._cursor.execute("UPDATE '%s' SET %s = %s" % (table_name, field_name,
                                                          str(convert_from_class(start_value))))
        self.commit()
        return 'Successfully'

    def create_db(self):
        """
        Table-creating function
        :return: Successfully
        """

        self._check_active()
        for table_name, table in self._databases.items():
            fields = ''
            fields_dict = table.get_types()
            for key, value in fields_dict.items():
                if key != 'id':
                    fields += f'{key}{value[0]}, '
            fields = fields[:len(fields)-2]
            request = f'''
                          CREATE TABLE IF NOT EXISTS {table_name}
                          (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, {fields})
                       '''
            self._cursor.execute(request)
        return 'Successfully'

    def _select(self, table_name):
        return self.execute("SELECT * FROM '%s'" % table_name.lower())

    def _get_databases(self):
        filt = ['string', 'integer', 'list_', 'dict_', 'Table', 'data_bases']
        databases = {}
        for k, i in vars(self._databases).items():
            if not k.startswith('__') and k not in filt:
                databases[k.lower()] = i
        self._database_names = [name for name in databases.keys()]
        self._databases = databases

    def _check_active(self):
        if not self._active:
            raise SqlApiError('The database file not inital')

    def _get_obj(self, table_name):
        if table_name in self._database_names:
            return self._databases[table_name]()
        else:
            raise SqlApiError(f'Table {table_name} not found')

    def get_cursor(self):
        """
        :return: Cursor object
        """
        self._check_active()
        return self._cursor

from .handler import RequestHandler
from .tables import *
from .utils import *


class SqlApiError(Exception):
    pass


class API(RequestHandler):
    def __init__(self, db_path):
        """
        :param db_path: The path to the file
        :type db_path: str
        """
        RequestHandler.__init__(self, db_path)
        try:
            self.data_bases = globals()['data_bases']
        except KeyError:
            raise SqlApiError("The variable data_bases is not listed in the tables.py file")
        if len(data_bases) == 0:
            raise SqlApiError("The tables.py file does not show the table classes")
        try:
            for db in self.data_bases:
                if shadow_fields(db):
                    raise SqlApiError(f"Discovered the same fields in the table {type(db).__name__}")
        except ValueError:
            pass

    def save(self, *table_classes):
        """
        Saves all changes
        :param table_classes: Object or objects received by filter function
        :return: Successfully
        """
        if len(table_classes) != 0:
            for table in table_classes:
                fields = []
                for key, value in vars(table).items():
                    if key != 'id':
                        fields.append('{}={}'.format(key, add_quotes(value)))
                self._cursor.execute("UPDATE '%s' SET %s WHERE id = %s" % (type(table).__name__.lower(),
                                                                           str(', '.join(fields)), table.id))
                self.commit()
            return 'Successfully'

        else:
            raise SqlApiError('Not transferred to the pill classes')

    def select(self, table_name):
        return self.execute("SELECT * FROM '%s'" % table_name.lower())

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
        table_name = table_name.lower()
        obj = self.get_obj(table_name)
        obj_fields = get_fields(obj)
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
            value = add_quotes(value)
            condition.append("{} {} {}".format(field, opt, str(value)))

        if len(condition) != 0:
            data = self.execute("SELECT * FROM '%s' WHERE %s" % (table_name, ' and '.join(condition)))

        else:
            data = self.select(table_name)

        if len(data) == 0:
            return

        if return_type == 'visual':
            if return_list:
                return data if type(data).__name__ == 'list' else [data]
            return data

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
        table_name = table_name.lower()
        obj = self.get_obj(table_name)
        obj_fields = get_fields(obj)
        fields = [i for i in obj_fields]

        for key, value in values.items():
            if key not in obj_fields:
                raise SqlApiError(f'Field {key} not found in table {table_name}')
            fields[fields.index(key)] = str(add_quotes(value))
            obj_fields.remove(key)

        if len(obj_fields) != 0:
            raise SqlApiError(f'No value{"s" if len(obj_fields) > 1 else ""} for'
                              f' field{"s" if len(obj_fields) > 1 else ""}: {", ".join(obj_fields)}')

        self._cursor.execute("INSERT INTO '%s' (%s) VALUES (%s)" % (table_name,
                                                                    ', '.join(get_fields(obj)),
                                                                    ', '.join(fields)))
        self.commit()
        return 'Successfully'

    def get_class(self, table_name, data):
        obj = self.get_obj(table_name.lower())
        types = vars(self.get_obj(table_name.lower()))
        fields = get_fields(obj)
        exec("obj.id = {}".format(data[0]))
        data = data[1:]

        for i in range(len(fields)):
            if types[fields[i]][1] == 'list':
                exec("obj.{} = {}".format(fields[i], convert_to_list(add_quotes(data[i]))))
                continue
            exec("obj.{} = {}".format(fields[i], str(add_quotes(data[i]))))

        return obj

    def create_db(self):
        """
        Table-creating function
        :return: Successfully
        """

        for table in self.data_bases:
            fields = ''
            table_name = type(table).__name__.lower()
            fields_dict = vars(table)
            for key, value in fields_dict.items():
                if key != 'id':
                    fields += f'{key}{value[0]}, '
            fields = fields[:len(fields)-2]
            request = f'''
                          CREATE TABLE {table_name}
                          (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, {fields})
                       '''
            self._cursor.execute(request)
        return 'Successfully'

    @staticmethod
    def get_obj(table_name):
        table = get(table_name.lower())
        if table:
            return table
        else:
            raise SqlApiError(f'Table {table_name} not found')

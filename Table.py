from sqlite3_api.utils import string, integer, list_, dict_


class Table:
    @classmethod
    def get_types(cls):
        _vars = {}
        for k, i in vars(cls).items():
            if not k.startswith('__'):
                _vars[k] = i
        return _vars

    @classmethod
    def get_fields(cls):
        fields = [i for i in cls.get_types().keys()]
        fields.remove('id')
        return fields

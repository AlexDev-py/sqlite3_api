from sqlite3_api.utils import string, integer, list_, dict_


class Table:

    @classmethod
    def get_types(cls):
        vars_ = {}
        for k, i in vars(cls).items():
            if not k.startswith('__'):
                vars_[k] = i
        return vars_

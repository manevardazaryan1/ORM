"""File is for inheritance and form creation."""


import sqlite3


class BaseMeta(type):
    """Creates database by form fields."""

    cls_name = None
    conn = sqlite3.connect("database.sqlite3")
    cur = conn.cursor()
    attr_list = []

    def __new__(cls, name, base, attrs):
        BaseMeta.cls_name = name
        for key, value in attrs.items():
            value = str(value)
            BaseMeta.attr_list.append(f'{key} {value}')
        fields = ",".join(BaseMeta.attr_list[8:])
        if name != 'BaseModel':
            execute = f'''CREATE TABLE IF NOT EXISTS {name}({fields})'''
            BaseMeta.cur.execute(execute)
        return type.__new__(cls, name, base, attrs)


class BaseModel(metaclass=BaseMeta):
    """Class created using the 'BaseMeta' class."""

    KEY_VALUE = {}

    @staticmethod
    def return_kargs(kargs):
        """Concatenates and returns keywords."""

        keys_list = []
        values_list = []
        for key, value in kargs.items():
            keys_list.append(key)
            values_list.append(f"'{value}'")
        keys = ",".join(keys_list)
        values = ",".join(values_list)
        BaseModel.KEY_VALUE = {'keys': keys, 'values': values}

    class Storage:
        """Class created to work with form fields."""

        @staticmethod
        def insert(**kargs):
            """Imports the data into the database."""

            BaseModel.return_kargs(kargs)
            BaseMeta.cur.execute(
                f'''
                INSERT INTO {BaseMeta.cls_name}({BaseModel.KEY_VALUE['keys']})
                VALUES ({BaseModel.KEY_VALUE['values']})
                ''')

        @staticmethod
        def get_by_field(**kargs):
            """Gets the data from the database according to the condition."""

            BaseModel.return_kargs(kargs)
            execute = f"""SELECT * FROM {BaseMeta.cls_name} WHERE {BaseModel.KEY_VALUE['keys']} = {BaseModel.KEY_VALUE['values']}"""
            data = BaseMeta.cur.execute(execute).fetchall()
            return data

        @staticmethod
        def update(*args):
            """Updates the base data according to the received argument and the matching condition."""

            execute = f"""UPDATE {BaseMeta.cls_name} SET {args[1]} WHERE {args[0]}"""
            BaseMeta.cur.execute(execute)

        @staticmethod
        def delete(**kargs):
            """Deletes the data from the database according to the received argument and the corresponding condition."""

            BaseModel.return_kargs(kargs)

            execute = f"""DELETE FROM {BaseMeta.cls_name} WHERE {BaseModel.KEY_VALUE['keys']} = {BaseModel.KEY_VALUE['values']}"""
            BaseMeta.cur.execute(execute)


class Field:
    """Creates a form field. Takes field name and typical parameters as arguments."""

    def __init__(self, *args, **kargs):
        self.args = args
        self.kargs = kargs
        self.karg = []
        for key, value in kargs.items():
            if value is None:
                value = 'NULL'
            if not value and value is not None:
                value = "''"
            self.karg.append(f"{key} {value}")

    def __str__(self):
        return f"{' '.join(self.args)} {' '.join(self.karg)}"

import logging
from collections import deque

from dollarify.db import Database
from dollarify.utils import hashing, uuid


class Model:
    """
    The model class is the superclass of all the models in the database.
    """

    table = None
    """
    The name of the database table where the data is stored.
    """

    column_names = None
    """
    The name of all the columns in the table (including the primary key column name)
    """

    pk_col_index = 0
    """
    The index of the primary key (col 1 is index 0). By default it is the first one (0).
    """

    loaded = None
    """
    The loaded variable is instantiated as a "collections.deque()" when the model should be stored in memory 
    for quick and recurrent access. A "maxlen" should also be defined (proportional to the amount needed). 
    When the "maxlen" count is reached, the oldest record is popped out of the collection and the new one take 
    the most recent place. 
    """

    excluded_vars = None # = ('bar','foo', ...)
    """
    The excluded variables tuple lists the variables that are not suitable for public/human readability (such as binary data).
    If the value is None, no variable is excluded from the str() and repr().
    """


    def __init__(self):
        raise NotImplementedError("The constructor is not usable.")


    def __new__(cls: type, pk, **attribs):
        model = None
        for m in cls.loaded:
            if m.pk == pk:
                model = m
                cls.loaded.remove(m)
                break
        if model is None:
            model = super(type(cls), cls).__new__(cls)
            model.pk = pk
            for k, v in attribs.items():
                setattr(model, f'_{k}', v)

        cls.loaded.appendleft(model)
        return model


    def fetch(cls, pk):
        try:
            response = Database.select_one(cls.table, pk)
            response = [value for i, value in enumerate(response) if i != cls.pk_col_index]
            column_names = cls.get_column_names(cls)
            return dict(zip(column_names, response))
        except ValueError:
            return None


    def get(cls, pk) -> type:
        assert cls is not Model.__class__, "Model class must be implemented first (This is the superclass of all models)."
        assert issubclass(cls, Model), "This model must be implemented first (This is the superclass of all models)."
        assert cls.table is not None, "The name of the table where the data if stored have to be provided."
        assert cls.column_names is not None, "The columns of the table have to be provided."
        assert cls.pk_col_index >= 0 and cls.pk_col_index < len(cls.column_names), "The primary key column index of the table have to be provided."
        assert pk is not None, "The primary key (pk) should be specified, otherwise, it is impossible to find a specific instance."
        
        attribs = cls.fetch(cls, pk)
        if attribs is None:
            return None
        return cls.__new__(cls, pk, **attribs)


    def create(cls, pk, commit=True, **attribs) -> type:

        if cls.exists(cls, pk):
            logging.warn(f"The model with the primary key {pk} already exists.")
            return None

        Database.insert_one(cls.table, tuple(attribs.keys()), tuple(attribs.values()), commit=commit)
        return cls.get(cls, pk)
        
        
    def exists(cls, pk):
        pk_col = cls.column_names[cls.pk_col_index]
        Database.query(f"SELECT {pk_col} FROM {cls.table} WHERE {pk_col}=?", task=(pk, ))
        return Database.CURSOR.fetchone() is not None


    def get_column_names(cls, pk_included: bool = False) -> tuple:
        if pk_included:
            return cls.column_names
        return [name for i, name in enumerate(cls.column_names) if i!= cls.pk_col_index]


    def push(self, commit=True):
        """
        Push the data to the database.
        commit: Commit the changes (this may be false)
        """
        values = [getattr(self, f"_{value}") for value in self.get_column_names()]
        Model.update_db(self.__class__.table, self.get_column_names(), (*values, self.pk), self.__class__.column_names[self.__class__.pk_col_index], commit)


    def __str__(self) -> str:
        header = f"[ {self.pk} ]".center(52, '=') + '\n'
        body = ""
        for col_name in self.__class__.column_names:
            if col_name != self.column_names[self.pk_col_index] and (self.__class__.excluded_vars is None or col_name not in self.__class__.excluded_vars):
                body = body + f"{col_name}:".ljust(20) + str(self.__dict__[f'_{col_name}']) + '\n'
        return header + body


    def __repr__(self) -> str:
        return str(self.__dict__)


class User(Model):

    table = 'users'
    loaded = deque(maxlen=32) # When new objects are added beyong 32, it pops those on the right (oldest).
    excluded_vars = ('password', 'salt')
    pk_col_index = 0
    column_names = ('uuid', 'username', 'password', 'salt', 'latest_balance')

    def create(cls, username: str, password_raw: str, latest_balance: float = 0.0, commit=True) -> str:
        user_uuid = uuid.generate()
        attribs = dict(zip(('uuid', 'username', 'password', 'salt', 'latest_balance'), (user_uuid, username, *hashing.hash_password(password_raw), latest_balance)))
        return Model.create(User, user_uuid, commit=commit, **attribs)

    @property
    def uuid(self):
        return self.pk

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def salt(self):
        return self._salt

    @property
    def latest_balance(self):
        return self._latest_balance
    
    @username.setter
    def username(self, value):
        if type(value) is not str:
            raise TypeError("The username must be of str type.")
        if len(value) > 64:
            raise ValueError("The username length should be a maximum of 64 characters.")
        self._username = value
        logging.debug("The username have been changed successfully!")

    @uuid.setter
    def uuid(self):
        raise NotImplementedError("The uuid can not be changed.")
    
    @password.setter
    def password(self, raw_password: str):
        password, salt = hashing.hash_password(raw_password)
        self._password = password
        self._salt = salt
        logging.debug("The password have been changed successfully!")
    
    @salt.setter
    def salt(self, value):
        raise NotImplementedError("The salt can only be changed by setting a new password.")

    @latest_balance.setter
    def latest_balance(self, value):
        self._latest_balance = value



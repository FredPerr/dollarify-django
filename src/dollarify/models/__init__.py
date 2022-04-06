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

    def get(cls, pk) -> type:
        assert cls.__class__ is not Model.__class__, 'This model must be implemented first (This is the superclass of all models).'


    def __init__(self, pk, column_names: tuple, pk_col_index = 0):
        """
        manager_class: The manager class is the class that extended this Model class.
        pk: the primary key of the object to load.
        column_names: The name of each columns of the model registered in the database (including the primary key column).
        """

        # if self.__class__ is Model.__class__:
        #     raise NotImplementedError("")

        if not issubclass(__class__, Model):
            raise TypeError("The type of the manager_class does not implement the Model class.")
        
        if self.__class__.table is None:
            raise NotImplementedError("The name of the table where the data if stored have to be provided.")

        if pk is None:
            raise TypeError("The primary key (pk) should be specified, otherwise, it is impossible to find a specific instance.")
        
        if pk_col_index < 0 or pk_col_index >= len(column_names):
            raise ValueError("The pk column index should range from 0 to the amount of columns - 1 (0-indexed).")
        
        self.pk = pk
        self._column_names = column_names
        self._pk_col_index = pk_col_index

        if self.__class__.loaded is not None:
            popped = None
            for model in self.__class__.loaded:
                if model.pk == pk:
                    popped = model
                    self.__class__.loaded.remove(model)
                    break

            if popped is None:
                self.fetch(pk=pk)
            else:
                self = popped
                self._username = popped._username

            self.__class__.loaded.appendleft(self)
        else:
            self.fetch(pk=pk)


    def get_column_names(self, pk_included: bool = False) -> tuple:
        if pk_included:
            return self._column_names

        return [name for i, name in enumerate(self._column_names) if i!=self._pk_col_index]
        

    def fetch(self, pk=None):
        if self.pk is None and pk is None:
            raise ValueError("The instance pk or the pk parameter should be provided.")
        response = Model.load_db(self.__class__.table, pk if self.pk is None else self.pk)
        response = [value for i, value in enumerate(response) if i!=self._pk_col_index]
        column_names = self.get_column_names()
        for i in range(len(response)):
            setattr(self, f'_{column_names[i]}', response[i])
            

    def push(self, commit=True):
        """
        Push the data to the database.
        commit: Commit the changes (this may be false)
        """
        values = [getattr(self, f"_{value}") for value in self.get_column_names()]
        Model.update_db(self.__class__.table, self.get_column_names(), (*values, self.pk), self._column_names[self._pk_col_index], commit)


    def load_db(table: str, pk: str, columns: str = '*'):
        Database.query(f'SELECT {columns} FROM {table} WHERE uuid=?;', task=(pk,))
        response = Database.CURSOR.fetchone()
        if response is None or len(response) == 0:
            raise ValueError(f"The model with the uuid {pk} was not found in the table {table}")
        return response


    def insert_db(table: str, columns: tuple, task: tuple, commit=True):
        values = (len(task) * '?,').strip(',')
        Database.query(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({values});", task, commit=commit)
    

    def update_db(table: str, columns: tuple, task: tuple, pk_col: str, commit=True):
        """
        Update a row in the database.
        task:   The values to replace the columns old values. 
                The value of the primary key should be added at the end of the task.
        pk_col: The name of the primary key column.
        """
        # create a column placeholder for the values: col1=?,col2=?,col3=?
        columns_str = ''
        for col in columns:
            columns_str += f"{col}=?,"
        columns_str = columns_str.strip(',')

        Database.query(f"UPDATE {table} SET {columns_str} WHERE {pk_col}=?", task, commit=commit)

class User(Model):

    table = 'users'
    loaded = deque(maxlen=32) # When new objects are added beyong 32, it pops those on the right (oldest).

    excluded_vars = ('uuid', 'username', 'latest_balance')

    def create(username: str, password_raw: str, latest_balance: int = 0) -> str:
        user_uuid = uuid.generate()
        Model.insert_db(User.table, ('uuid', 'username', 'password', 'salt', 'latest_balance'), (user_uuid, username, *hashing.hash_password(password_raw), latest_balance))
        return user_uuid

    def create_and_fetch(username: str, password_raw: str, latest_balance: int = 0):
        uuid = User.create(username, password_raw, latest_balance)
        return User(uuid)

    def __init__(self, uuid):
        super().__init__(uuid, ('uuid', 'username', 'password', 'salt', 'latest_balance'))

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if type(value) is not str:
            raise TypeError("The username must be of str type.")
        if len(value) > 64:
            raise ValueError("The username length should be a maximum of 64 characters.")
        self._username = value
        logging.debug("The username have been changed successfully!")

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self):
        raise NotImplementedError("The uuid can not be changed.")
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, raw_password: str):
        password, salt = hashing.hash_password(raw_password)
        self._password = password
        self._salt = salt
        logging.debug("The password have been changed successfully!")

    @property
    def salt(self):
        raise NotImplementedError("The salt of a password is not accessible.")
    
    @salt.setter
    def salt(self, value):
        raise NotImplementedError("The salt can only be changed by setting a new password.")
    
    @property
    def latest_balance(self):
        return self._latest_balance

    @latest_balance.setter
    def latest_balance(self, value):
        self._latest_balance = value

    def __str__(self) -> str:
        msg_len = 50
        header = f"[ {self.uuid} ]".center(msg_len, '=') + '\n'
        body = ""
        
        for var_name in self._public_vars:
            body = body + f"{var_name}:".ljust(20) + str(self.__dict__[var_name]) + '\n'
        return header + body

    def __repr__(self) -> str:
        return str(self.__dict__)

import logging
from dollarify.db import Database
from dollarify.utils import hashing, uuid


class Model:

    table = None
    # loaded = None

    def __init__(self):
        raise NotImplementedError()

    def load_db(table: str, uuid: str, columns: str = '*'):
        Database.query(f'SELECT {columns} FROM {table} WHERE uuid=?;', task=(uuid,))
        response = Database.CURSOR.fetchone()
        if response is None or len(response) == 0:
            raise ValueError(f"The model with the uuid {uuid} was not found in the table {table}")
        return response

    def insert_db(table: str, columns: tuple, task: tuple, commit=True):
        if len(task) == 0 or not len(task) == len(columns):
            raise ValueError("The columns count is 0 or it does not match the task count.")
        values = (len(task) * '?,').strip(',')
        Database.query(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({values});", task, commit=commit)



class User(Model):

    table = 'users'
    # loaded = []

    _public_vars = ('_uuid', '_username', '_latest_balance')

    def create(username: str, password_raw: str, latest_balance: int = 0) -> str:
        user_uuid = uuid.generate()
        Model.insert_db(User.table, ('uuid', 'username', 'password', 'salt', 'latest_balance'), (user_uuid, username, *hashing.hash_password(password_raw), latest_balance))
        return user_uuid

    def create_and_fetch(username: str, password_raw: str, latest_balance: int = 0):
        uuid = User.create(username, password_raw, latest_balance)
        return User(uuid)


    def __init__(self, uuid):
        self.reload(uuid)

    def reload(self, uuid=None):

        # The user has already been loaded.
        if uuid is None:
            uuid = self.uuid

        response = Model.load_db(User.table, uuid)
        self._uuid = response[0]
        self._username = response[1]
        self._password = response[2]
        self._salt = response[3]
        self._latest_balance = response[4]

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if type(value) is not str:
            raise TypeError("The username must be of str type.")
        if len(value) > 64:
            raise ValueError("The usename length should be a maximum of 64 characters.")
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

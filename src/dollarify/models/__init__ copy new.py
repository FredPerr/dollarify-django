from datetime import date
import inspect
import logging
from collections import deque

from dollarify.db import DBType, Database, DBAttribute
from dollarify.utils import hashing, uuid
from dollarify.models.validators import *


LENGTH_EXCEEDED_CHARACTERS = "The length of %s must not exceed %i characters."


class ModelField:

    def __init__(self, db_type: tuple, name: str, max_length: int = 0, default = None,  pk: bool = False, nullable: bool = False, validators: tuple = None):
        """
        db_type: Type of the field in the database (SQLite3: detected by default for VARCHAR(%i), TEXT, INTEGER, FLOAT, BLOB, BOOLEAN).
        name: The name of the columns used to store this field in the database.
        max_length: Maximum length of the field. If 0, it is ignored.
        default: The default value set to the field. If None, the nullable parameter must also be set to True.
        pk: True if the field is the primary key of the table in the database.
        nullable: Set to True if the field can store None value.
        validators: A tuple of functions (callables) with the value as parameter to validate conditions.
        """
        assert db_type is not None, "The database type of this field can't be None."
        assert type(db_type) is tuple and len(db_type) == 2, "The db_type must be a tuple of a type and the database equivalent of that type."
        assert type(name) is str, "The name of the field have to be a string."
        assert len(name) > 0, "the name length should at least be one character long."
        assert type(max_length) is int, "The maximum length of the field must be an integer."
        assert max_length >= 0, "The length of the field can't be negative."
        assert type(nullable) is bool, "The nullable parameter have to be set to True to allow for None value or False for the contrary."
        assert type(pk) is bool, "The type of the primary key (pk) parameter have to be a boolean of True or False."
        assert re.match(r"^[a-z][a-z0-9_]{1,16}$", name) is not None, "The name should start with a letter contain and be all lowercased. 0-9 or underscores (_) allowed and maximum length is 16."

        self.db_type = db_type
        self.name = name
        self.max_length = max_length
        self.default = default
        self.pk = pk,
        self.nullable = nullable
        self.validators = validators


    def validate(self, value) -> bool:
        for validator in self.validators:
            if not validator(value):
                return False
        return True

    @property
    def type_db(self):
        return self.db_type[1]

    @property
    def attributes_db(self):
        return f"{DBAttribute.DEFAULT % self.default if self.default is not None else ' '}" \
        f"{' ' + DBAttribute.NOT_NULL if self.nullable is False else ''}" \
        f"{' ' + DBAttribute.PRIMARY_KEY if self.pk else ''}"


class IntegerField(ModelField):

    def __init__(self, name: str, default=None, pk: bool = False, nullable: bool = False, validators: tuple = None, min=None, max=None):
        super().__init__(DBType.INTEGER, name, 0, default, pk, nullable, validators)
        assert_min_max(int, min, max)
        self.max = max
        self.min = min
        

    def validate(self, value) -> bool:
        basic_validation = super().validate(value)
        if not basic_validation:
            return False
        return validate_min_max(value, self.min, self.max)
        

class FloatField(ModelField):

    def __init__(self, name: str, default=None, pk: bool = False, nullable: bool = False, validators: tuple = None, min=None, max=None):
        super().__init__(DBType.REAL, name, 0, default, pk, nullable, validators)
        self.max = max
        self.min = min

    def validate(self, value) -> bool:
        basic_validation = super().validate(value)
        if not basic_validation:
            return False
        return validate_min_max(value, self.min, self.max)


class BooleanField(ModelField):

    def __init__(self, name: str, default=None, nullable: bool = False, validators: tuple = None):
        super().__init__(DBType.BOOLEAN, name, 0, default, False, nullable, validators)


class BytesField(ModelField):

    def __init__(self, name: str, default=None, pk: bool = False, nullable: bool = False, validators: tuple = None, min=None, max=None):
        super().__init__(DBType.BLOB, name, 0, default, pk, nullable, validators)
        assert_min_max(bytes, min, max)
        self.min = min
        self.max = max


class CharField(ModelField):
    
    def __init__(self, name: str, max_length: int, default=None, pk: bool = False, nullable: bool = False, validators: tuple = None, min=None, max=None):
        """
        NOTE: The VARCHAR uses format of %i for the maximum length of the field.
        """
        super().__init__(DBType.VARCHAR, name, 0, default, pk, nullable, validators)
        assert max_length > 0, "The maximum length have to be more than 0 for the Char type of field."
        assert_min_max(str, min, max)
        self.min = min
        self.max = max
    
    @property
    def type_db(self):
        return self.db_type[1] % self.max_length


class TextField(ModelField):
    
    def __init__(self, name: str = None, default=None, nullable: bool = False, validators: tuple = None, min=None, max=None):
        super().__init__(DBType.TEXT, name, 0, default, False, nullable, validators)
        assert_min_max(str, min, max)
        self.min = min
        self.max = max


########################
#       Model          #
########################


class Model:
    """
    The model class is the superclass of all the models in the database.
    """

    table = None
    """
    The name of the database table where the data is stored.
    """

    column_names = None # TODO Delete
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
        if cls.loaded is not None:
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

    
    def __getattribute__(self, __name: str):
        value = object.__getattribute__(self, __name)
        if isinstance(value, ModelField):
            if value.pk:
                return object.__getattribute__(self, 'pk')
            __name = f'_{__name}'
        return object.__getattribute__(self, __name)

    # TODO: redefine
    def __setattr__(self, __name: str, __value):
        field = self.__getattribute__(__name)
        if isinstance(field, ModelField):
            if not field.validate(__value):
                 logging.warn(f"The value set {__value} is not valid.")
                 return
            object.__setattr__(self, f'_{__name}', __value)
        else:
            super().__setattr__(__name, __value)


    def fetch(cls, pk):
        try:
            response = Database.select_one(cls.table, pk, cls.column_names(cls)[cls.pk_col_index])
            response = [value for i, value in enumerate(response) if i != cls.pk_col_index]
            return dict(zip(cls.column_names(cls), response))
        except ValueError:
            return None

    def get_fields(cls, only_names=False):
        members = inspect.getmembers(cls, lambda x: (not inspect.isroutine(x) and isinstance(x, ModelField))) 
        if only_names:
            return (member[0] for member in members)
        return members

    def column_names(cls, pk_included = False):
        fields = cls.get_fields(cls)
        names = []
        for field in fields:
            print(field)
            if not pk_included and field.pk:
                continue
            names.append(field.name)
        return names


    def get(cls, pk) -> type:
        assert cls is not Model.__class__, "Model class must be implemented first (This is the superclass of all models)."
        assert issubclass(cls, Model), "This model must be implemented first (This is the superclass of all models)."
        assert cls.table is not None, "The name of the table where the data if stored have to be provided."
        assert cls.pk_col_index >= 0 and cls.pk_col_index < len(cls.column_names(cls)), "The primary key column index of the table have to be provided."
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
        
    def delete(self, commit=True):
        clazz = self.__class__
        if not clazz.exists(clazz, self.pk):
            logging.warn(f"The model wit hthe primary key {self.pk} does not exist.")
            return
        
        Database.delete_one(clazz.table, clazz.column_names[clazz.pk_col_index], self.pk, commit=commit)
        if clazz.loaded is not None:
            clazz.loaded.remove(self)

        
    def exists(cls, pk):
        pk_col = cls.column_names(cls)[cls.pk_col_index]
        Database.query(f"SELECT {pk_col} FROM {cls.table} WHERE {pk_col}=?", task=(pk, ))
        return Database.CURSOR.fetchone() is not None


    def push(self, commit=True):
        """
        Push the data to the database.
        commit: Commit the changes (this may be false)
        """
        values = [getattr(self, f"_{value}") for value in self.column_names()]
        Database.update_one(self.__class__.table, self.column_names(), (*values, self.pk), self.__class__.column_names[self.__class__.pk_col_index], commit)


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
    # column_names = ('uuid', 'username', 'password', 'salt', 'latest_balance')

    uuid = CharField('uuid', 32, validators=(validate_uuid, ), pk=True)
    username = CharField('username', 64, validators=(validate_username, ))
    password = BytesField('password')
    salt = BytesField('salt')
    latest_balance = FloatField('latest_balance', default=0)


    def create(cls, username: str, password_raw: str, latest_balance: float = 0.0, commit=True):

        if len(username) > 64:
            raise ValueError(LENGTH_EXCEEDED_CHARACTERS.format('username', 64))

        user_uuid = uuid.generate()
        attribs = dict(zip(('uuid', 'username', 'password', 'salt', 'latest_balance'), (user_uuid, username, *hashing.hash_password(password_raw), latest_balance)))
        return Model.create(User, user_uuid, commit=commit, **attribs)


class AccountType(Model):

    table = 'account_types'
    loaded = deque(maxlen=5)
    pk_col_index = 0
    column_names = ('name', 'information')

    name_max_length = 16


    def create(cls, name: str, information: str, commit=True):
        if len(name) > cls.name_max_length:
            raise ValueError(LENGTH_EXCEEDED_CHARACTERS % ('name', cls.name_max_length))

        if len(information) > 255:
            raise ValueError(LENGTH_EXCEEDED_CHARACTERS % ('information', 255))

        attribs = dict(zip(cls.column_names(cls), (name, information)))
        return Model.create(cls, name, commit=commit, **attribs)

    @property
    def name(self):
        return self._name

    def name(self, value):
        if value > 16:
            raise ValueError(LENGTH_EXCEEDED_CHARACTERS % ('name', self.__class__.name_max_length))
        self._name = value
    

class AccountAttribute(AccountType):

    table = 'account_attributes'
    loaded = deque(maxlen=5)
    pk_col_index = 0
    column_names = ('uuid', 'provider_id')


class Provider(AccountType):

    table = 'providers'
    loaded = deque(maxlen=10)
    pk_col_index = 0
    column_names = ('name', 'information')
    name_max_length = 32


class Account(Model):

    table = 'accounts'
    loaded = deque(maxlen=50)
    column_names = ('uuid', 'provider', 'owners', 'name', 
                    'type_name', 'attribute_name', 'latest_balance',
                    'open_date', 'closed_date')
    
    
    def create(cls, provider: str, owners: tuple, name: str, type_name: str,
                attribute_name: str, latest_balance: float, open_date: date = None, closed_date: date = None, commit=True):

        account_uuid = uuid.generate()
        assert len(owners) < 9, "An account can only have 8 owners maximum."
        for owner in owners:
            assert len(owner) == 32, "The owners' UUID must be 32 character length."
        owners = ''.join(owners)

        assert len(name) <= 64, "The name of the account must not be greater than 64 characters."
        assert len(type_name) <= 16, "The length of the name of the type of the account should not be greater than 16 characters." 
        if attribute_name is not None:
            assert len(attribute_name) <= 16, "The length of the name of the type of the account should not be greater than 16 characters." 
        if open_date is None:
            open_date = date.today()
        if closed_date is not None:
            assert closed_date >= open_date, "The date on which the account was created can not be after the date on which the account was closed."

        attribs = dict(zip(cls.column_names(cls), (account_uuid, provider, ''.join(owners), name, type_name, attribute_name, latest_balance, open_date, closed_date)))
        return Model.create(cls, account_uuid, commit=commit, **attribs)

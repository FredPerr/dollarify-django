from datetime import datetime
import inspect
import sys
from types import ModuleType
from typing import Tuple

from dollarify.db import DBType, DBAttribute, Database
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
        self.pk = pk
        self.nullable = nullable
        self.validators = validators


    def validate(self, value) -> bool:
        if not self.validators:
            return True
        for validator in self.validators:
            if not validator(value):
                return False
        return True

    @property
    def type_db(self):
        return self.db_type[1]

    @property
    def attributes_db(self):
        attribs = []
        if self.default is not None:
            attribs.append(DBAttribute.DEFAULT % f"'{self.default}'")
        if not self.nullable:
            attribs.append(DBAttribute.NOT_NULL)
        if self.pk:
            attribs.append(str(DBAttribute.PRIMARY_KEY))
        return ' '.join(attribs)


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
        super().__init__(DBType.VARCHAR, name, max_length, default, pk, nullable, validators)
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


class DateField(ModelField):

    def __init__(self, name: str, default=None, pk: bool = False, nullable: bool = False, validators: tuple = None):
        super().__init__(DBType.TEXT, name, 0, default, pk, nullable, validators)


class DateTimeField(DateField):

    def __init__(self, name: str, default=None, pk: bool = False, nullable: bool = False, validators: tuple = None):
        super().__init__(name, default, pk, nullable, validators)



########################
#       Model          #
########################


class Model:

    table_name = None

    # fields here to be added here in the subclass #


    def __init__(self):
        raise NotImplementedError("The constructor is not usable.")
                

    def __setattr__(self, __name: str, __value):
        field = self.__class__._get_field_from_name(self.__class__, __name)
        is_field = not field is None
        if is_field and not field[1].validate(__value):
            raise ValueError(f"The value {str(__value)} of the field {__name} is not valid.")            
        object.__setattr__(self, f'_{__name}' if is_field else __name, __value)
    

    def __getattribute__(self, __name: str):
        value = object.__getattribute__(self, __name)
        return object.__getattribute__(self, f'_{__name}' if isinstance(value, ModelField) else __name)


    def __repr__(self) -> str:
        return str({field[0]: getattr(self, field[0]) for field in self.__class__.get_fields(self.__class__)})


    def __str__(self) -> str:
        pk_field_name = self.__class__.get_pk_field(self.__class__, name_only=True)
        header = f"[ {self.__class__.__name__} : {str(getattr(self, pk_field_name))} ]".center(60, '-') + '\n'
        lines = tuple(f"{field[0]}:".ljust(20) + f" {getattr(self, field[0])}" for field in self.__class__.get_fields(self.__class__))
        return header + '\n'.join(lines)


    def create(cls, commit=True, **field_values) -> type:
        model = cls.__new__(cls, **field_values)
        columns = tuple(cls._get_field_from_name(cls, key)[1].name for key in tuple(field_values.keys()))
        # Database.insert_one(cls.table_name, columns, tuple(field_values.values()), commit) TODO: remove comment
        return model

    def fetch(cls, pk):
        try:
            response = Database.select_one(cls.table_name(cls), pk, cls.get_pk_field(cls)[1].name)
            response = [value for i, value in enumerate(response) if i != cls.pk_col_index]
            return dict(zip(cls._get_db_columns(cls), response))
        except ValueError:
            return None


    def get_fields(cls, names_only: bool = False):
        """
        Get the fields of the models (variable name, field object).
        names_only: True to return only the name of the variables.
        """
        return tuple([member[0] if names_only else member for member in inspect.getmembers(cls, lambda x: (not inspect.isroutine(x) and isinstance(x, ModelField)))][::-1]) 
    

    def get_pk_field(cls, name_only: bool = False):
        """
        Get the primary key field name (variable name) and Field object attached to it.
        name_only: True to return only the name of the variable.
        """
        fields = cls.get_fields(cls)
        for field in fields:
            if field[1].pk:
                return field[0] if name_only else field
        raise ValueError("No field was set as the primary key. The pk field can't be returned.")
    

    def _get_field_from_name(cls, field_name):
        """
        Get a field from its variable name.
        """
        for field in cls.get_fields(cls):
            if field[0] == field_name:
                return field
        return None


    def _get_db_columns(cls):
        return tuple((field[1].name for field in cls.get_fields()))


    def create_table(cls):
        fields = cls.get_fields(cls)
        columns_sql = tuple(f"{field[0]} {field[1].type_db} {field[1].attributes_db}" for field in fields)
        Database.query(f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({', '.join(columns_sql)});", commit=True)


    def __new__(cls: type, **field_values):
        model = super(type(cls), cls).__new__(cls)
        fields = cls.get_fields(cls)
        field_keys = tuple(field_values.keys())
        pk = False
        for field in fields:
            if field[1].pk is True:
                if pk:
                    raise ValueError(f"The model cannot have more than one primary key; ({field[0]} is the second one loaded).")
                else:
                    pk = True 
            if field[0] in field_keys:
                setattr(model, field[0], field_values[field[0]])
            elif field[1].nullable and field[1].default is not None:
                setattr(model, field[0], field[1].default)
            else:
                raise ValueError(f"A value must be provided for the field {field[0]}.")
        if not pk:
            raise ValueError("The model must have a primary key.")
        return model


class User(Model):

    table_name = 'users'

    uuid = CharField('uuid', 32, pk=True)
    username = CharField('username', 64)
    password = BytesField('password')
    salt = BytesField('salt')
    latest_balance = FloatField('latest_balance', 0, nullable=True)


class Provider(Model):

    table_name = 'providers'

    name = CharField('name', 32, pk=True)
    information = TextField('information', max=255)


class AccountType(Model):

    table_name = 'account_types'

    name = CharField('name', 32, pk=True)
    information = TextField('information', max=255)


class AccountAttribute(Model):

    table_name = 'account_attributes'

    name = CharField('name', 32, pk=True)
    information = TextField('information', max=255)
    region = CharField('region', 3)


class Account(Model):

    table_name = 'accounts'

    uuid = CharField('uuid', 32, pk=True)
    provider = CharField('provider_uuid', 32, nullable=True)
    owners = CharField('owners', 256) # allows for 8 different uuids.
    name = CharField('name', 16)
    type_name = CharField('type_name', 16)
    attribute_name = CharField('attribute_name', 16)
    latest_balance = FloatField('latest_balance', nullable=True)
    open_date = DateField('open_date', default=datetime.now().strftime('%Y-%m-%d'))
    closed_date = DateField('closed_date', nullable=True)


class Trade(Model):

    table_name = 'trades'

    id = IntegerField('id', pk=True)
    account = CharField('account_uuid', 32)
    ticker = CharField('ticker', 8)
    buy_date = DateTimeField('buy_datetime', default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    shares = IntegerField('shares')
    buy_value = FloatField('buy_value')
    fees = FloatField('fees', default=0)
    sell_value = FloatField('sell_value', nullable=True)
    sell_date = DateField('sell_date', nullable=True)


####################
# Module functions #
####################


def get_models_classes(modules: Tuple[ModuleType]):
    """
    Get the registered models in this module and in the specified modules
    """
    modules = sys.modules[__name__], *modules
    models = []
    for module in modules:
        for member in inspect.getmembers(module, inspect.isclass):
            if issubclass(member[1], Model) and not member[1] == Model:
                models.append(member[1])
    return models

        

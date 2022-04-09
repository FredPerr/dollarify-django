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
    
    table_name = None

    test = CharField('this_is_a_test', 50)

    # fields

    def get_fields(cls, names_only: bool = False):
        return tuple(member[0] if names_only else member for member in inspect.getmembers(cls, lambda x: (not inspect.isroutine(x) and isinstance(x, ModelField)))) 

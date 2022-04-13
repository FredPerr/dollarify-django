import logging
import sqlite3
import os
from typing import Tuple
from pathlib import Path
import inspect

from dollarify.db import sqlite3
from dollarify.static import staticfiles
from importlib.resources import Package
from dollarify.settings import BASE_DIR


class DBType:

    BOOLEAN = (bool, 'BOOLEAN')
    BLOB = (bytes, 'BLOB')
    VARCHAR = (str, 'VARCHAR(%i)')
    TEXT = (str, 'TEXT')
    REAL = (float, 'REAL')
    INTEGER = (int, 'INTEGER')


class DBAttribute:

    NOT_NULL = 'NOT NULL'
    PRIMARY_KEY = 'PRIMARY KEY'
    DEFAULT = "DEFAULT %s"


class Database:

    CURSOR = None
    CONNECTION = None
    TYPES = None
    ATTRIBUTES = None


    def __init__(self) -> None:
        raise NotImplementedError("No instance of this class should be created.")

    def query(*args, **kwargs):
        """
        Perform a SQL Query with arguments (task) and allowing for {keyword} replacement.
        task: tuple of the data to replace the question mark (?) in the query (optional).
        replace: keyword to be replace with their values.
        """
        raise NotImplementedError()

    def query_script_file(*args, **kwargs):
        """
        Perform a SQL Query stored inside a file. 
        Tasks are not allowed but replacements are.
        """
        raise NotImplementedError()

    def connect(cls, *args, **kwargs):
        """
        Connect to the database.
        :return: A tuple: (database_connection, database_cursor)
        """
        func_list = [name for name, value in inspect.getmembers(Database, predicate=inspect.isfunction) 
                    if not name.startswith("__") and not name == Database.connect.__name__]
        
        for name in func_list:
            setattr(Database, name, getattr(cls, name))

        Database.TYPES = cls.TYPES
        Database.ATTRIBUTES = cls.ATTRIBUTES
        
        cls._connect(*args, **kwargs)

    def commit():
        raise NotImplementedError()


    def close():
        """
        Terminate the connection to the database.
        """
        raise NotImplementedError()

    
    def insert_one():
        """
        Insert a row into a table.
        """
        raise NotImplementedError()

    def select_one():
        """
        Select a row from a table.
        """
        raise NotImplementedError()

    def select_all():
        """
        Select all the rows from a table.
        """
        raise NotImplementedError()

    def update_one():
        """
        Update a row into a table.
        """
        raise NotImplementedError()

    def delete_one():
        "Delete a row from the table."
        raise NotImplementedError()


class SQLiteDB(Database):

    TYPES = (DBType.VARCHAR, DBType.BLOB, DBType.BOOLEAN, DBType.INTEGER, DBType.TEXT, DBType.REAL)
    ATTRIBUTES = (DBAttribute.NOT_NULL, DBAttribute.PRIMARY_KEY)

    def _connect(db_path) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        path = os.path.join(Path(BASE_DIR).parent, db_path)
        exists = os.path.isfile(path)
        
        if not exists:
            logging.warning(f'The database "{path}" did not exist on the file system, it will be created.')

        Database.CONNECTION = sqlite3.connect(db_path, check_same_thread=False)
        Database.CURSOR = Database.CONNECTION.cursor()
        logging.debug('Connected to the database successfully!')

    def close():
        Database.CONNECTION.close()
        Database.CONNECTION, Database.CURSOR = None, None
        logging.debug('Closed the connection to the database!')
    
    def query(sql, task=(), commit=False, replacements={}):
        sql = sql.format(**replacements)
        Database.CURSOR.execute(sql, task)
        if commit:
            Database.CONNECTION.commit()
    
    def query_script_file(script_filename: str, package: Package, commit=False, replacements={}):
        Database.CURSOR.executescript(staticfiles.load_static(script_filename, pkg=package).format(**replacements))
        if commit:
            Database.CONNECTION.commit()

    def commit():
        Database.CONNECTION.commit()

    # def insert_one(table: str, columns: tuple, task: tuple, or_replace=False, commit=True):
    #     values = (len(task) * '?,').strip(',')
    #     Database.query(f"INSERT {'OR REPLACE ' if or_replace else ''}INTO {table} ({','.join(columns)}) VALUES ({values});", task, commit=commit)
    

    def insert_one(table: str, key_values: dict, or_replace=False, commit=True):
        kvalues = tuple(key_values.values())
        values = (len(kvalues) * '?,').strip(',')
        Database.query(f"INSERT {'OR REPLACE ' if or_replace else ''}INTO {table} ({','.join(tuple(key_values.keys()))}) VALUES ({values});", kvalues, commit=commit)
    

    def select_one(table: str, pk: str, pk_col_name: str, columns: str = '*'):
        Database.query(f'SELECT {columns} FROM {table} WHERE {pk_col_name}=?;', task=(pk,))
        response = Database.CURSOR.fetchone()
        if response is None or len(response) == 0:
            raise ValueError(f"The model with the {pk_col_name} {pk} was not found in the table {table}")
        return response

    def select_all(table: str):
        Database.query(f'SELECT * FROM {table};')
        response = Database.CURSOR.fetchall()
        if response is None or len(response) == 0:
            raise ValueError(f'Could not load the rows in the database.')
        return response

    def update_one(table: str, columns: tuple, task: tuple, pk_col: str, commit=True):
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
    
    def delete_one(table: str, pk_col_name: str, pk, commit=True):
        """
        Delete a row from the table.
        pk_col_name: Name of the pk column.
        pk: the primary key to search for.
        """
        Database.query(f"DELETE FROM {table} WHERE {pk_col_name}=?", task=(pk,), commit=commit)


def backup_db(db_name: str, to_path: Path):
    import shutil
    try:
        shutil.copyfile(db_name, to_path)
        logging.info(f'The backup ({db_name}) -> ({to_path}) was succesffully completed!')
    except:
        logging.error(f'The backup failed ({db_name}) -> ({to_path})')


####################################
# Specific Dollarify DB Management #
####################################

def init():
    
    # Inititialize tables
    from dollarify.models import get_models_classes, Model, AccountAttribute, AccountType
    
    # Create the table if not exist
    for model_class in get_models_classes([]):
        Model.create_table(model_class)


    Database.insert_one(AccountAttribute.table_name, {
        'name': 'TFSA',
        'region': 'CAN',
        'information': 'No capital gain tax;Predefined limit of contribution per year'
    }, or_replace=True)


    Database.insert_one(AccountAttribute.table_name, {
        'name': 'RRSP',
        'region': 'CAN',
        'information': 'Delayed taxation on contribution;Predefined or calculated limit of contribution per year'
    }, or_replace=True)




    Database.insert_one(AccountType.table_name, {
        'name': 'CHQ',
        'information': 'Checking Account;0.01% Interest Rate;No transactional fee;Not taxed'
    }, or_replace=True)

    Database.insert_one(AccountType.table_name, {
        'name': 'HISA',
        'information': 'High Interest Savings Account;0.1% Interest Rate;No transactional fee;Not taxed'
    }, or_replace=True)

    
    Database.insert_one(AccountType.table_name, {
        'name': 'CREDIT',
        'information': 'Credit card account;Variable Interest Rate;Variable Cashback or BONUSDOLLARS;Not taxed'
    }, or_replace=True)
    

    Database.insert_one(AccountType.table_name, {
        'name': 'STOCK',
        'information': 'Stock Market trading account'
    }, or_replace=True)



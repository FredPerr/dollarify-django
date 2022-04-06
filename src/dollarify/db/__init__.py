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


class Database:

    CURSOR = None
    CONNECTION = None

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
        cls._connect(*args, **kwargs)

        func_list = [name for name, value in inspect.getmembers(Database, predicate=inspect.isfunction) 
                    if not name.startswith("__") and not name == Database.connect.__name__]
        
        for name in func_list:
            setattr(Database, name, getattr(cls, name))
        

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

    def update_one():
        """
        Update a row into a table.
        """
        raise NotImplementedError()


class SQLiteDB(Database):

    def _connect(db_path) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        path = os.path.join(Path(BASE_DIR).parent, db_path)
        exists = os.path.isfile(path)
        
        if not exists:
            logging.warning(f'The database "{path}" did not exist on the file system, it will be created.')

        Database.CONNECTION = sqlite3.connect(db_path)
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

    def insert_one(table: str, columns: tuple, task: tuple, commit=True):
        values = (len(task) * '?,').strip(',')
        Database.query(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({values});", task, commit=commit)
    
    def select_one(table: str, pk: str, columns: str = '*'):
        Database.query(f'SELECT {columns} FROM {table} WHERE uuid=?;', task=(pk,))
        response = Database.CURSOR.fetchone()
        if response is None or len(response) == 0:
            raise ValueError(f"The model with the uuid {pk} was not found in the table {table}")
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
    



####################################
# Specific Dollarify DB Management #
####################################

def init():
    
    # Inititialize tables
    from dollarify.static.db.sqlite3 import queries

    Database.query_script_file('create_tables.sql', queries)
    Database.query_script_file('init_tables.sql', queries, commit=True)


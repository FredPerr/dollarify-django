import logging
import sqlite3
import os
from typing import Tuple
from pathlib import Path

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
        Database.close = cls.close
        Database.query = cls.query
        Database.query_script_file = cls.query_script_file
        Database.commit = cls.commit
        

    def commit():
        raise NotImplementedError()


    def close():
        """
        Terminate the connection to the database.
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
            

# Specific Dollarify DB Management #

def init():
    # Inititialize tables
    from dollarify.static.db.sqlite3 import queries

    Database.query_script_file('create_tables.sql', queries)
    Database.query_script_file('init_tables.sql', queries, commit=True)


import importlib
import logging
import sqlite3
from dollarify.static import staticfiles
from dollarify.static.db.sqlite3 import queries
from dollarify import settings
from dollarify.utils import uuid, hashing


DB_MODULE, DB_CONNECTION, DB_CURSOR = None, None, None


class Table:

    def __init__(self, name: str, column_sql: str):
        """
        name: name of the table
        columns_sql: columns part of the sql query referencing columns names and attributes. For instance, (uuid VARCHAR(32), name VARCHAR(32))
        """
        if len(name) < 1:
            raise ValueError("The name of the table should be at least one character long.")

        if len(column_sql) < 2 or not column_sql[0] == '(' or not column_sql[-1] == ')':
            raise ValueError("The column_sql should respect the following format: (col_name1 VARCHAR(5), col_name2 DECIMAL(5,2), ...)")
        self.name = name
        self.column_sql = column_sql

    def insert(self, *args, **kwargs):
        """
        Insert a row in the table.
        """
        pass

    def delete(self, *args, **kwargs):
        """
        Delete a row in the table.
        """
        pass

    def select(self, *args, **kwargs):
        """
        Select row(s) in the table.
        """
        pass

    def create(self, ignore_if_exists = True):
        execute_query(f"""CREATE TABLE {'IF NOT EXISTS' if ignore_if_exists else ''} {self.name} {self.column_sql};""")

    def drop(self):
        execute_query(f"""DROP TABLE IF NOT EXISTS {self.name};""")
    
    def columns(self, names = True, types = True, flags = True):
        cols = Table._parse_columns_sql(self.column_sql)
        feedback = []
        for col in cols:
            current = []
            if names:
                current.append(col[0])
            if types:
                current.append(col[1])
            if flags:
                current.append(col[2])
            feedback.append(current)
        return feedback

    def query(self, sql, task=None, **kwargs):
        """
        Execute the sql provided with variable replacement. 
        This includes the given keyword argument and the name of the table (table_name).
        """
        return execute_query(sql.format(table_name=self.name, **kwargs), task)

    def query_from_script(self, script, **kwargs):
        """
        Query SQL via a script (**multiple queries allowed**).
        script: name of the script in the 'queries' folder/package with its extension.
        """
        sql = staticfiles.load_static(script, pkg=queries)
        sql = sql.format(table_name=self.name, **kwargs)
        print(sql)
        execute_queries(sql)

    @classmethod
    def _parse_column_sql(cls, sql):
        """
        Parse (column_name REAL NOT DEFAULT 10) into 'column_name', 'REAL', 'NOT NULL DEFAULT 10'
        """
        if sql[0] == '(' and sql[-1] == ')':
            sql = sql[1:-1]
        
        try:
            name, sql_attribs = sql.strip().split(' ', 1)
            sql_flags = ''
            if ' ' in sql_attribs.strip():
                sql_type, sql_flags = sql_attribs.strip().split(' ', 1)
            else:
                sql_type = sql_attribs
            return name.strip(), sql_type.strip(), sql_flags.strip()
        except ValueError:
            logging.error(f'The sql provided "{sql}" does not contain sql attributes.')
    
    @classmethod
    def _parse_columns_sql(cls, sql):
        """
        Parse (col1_name REAL NOT NULL DEFAULT 10, col2_name VARCHAR(5) NOT NULL) into 
              (('col1_name', 'REAL', 'NOT NULL'), ...)
        """
        if sql[0] == '(' and sql[-1] == ')':
            sql = sql[1:-1]
        
        columns_split = sql.strip().split(',')
        return tuple([cls._parse_column_sql(col) for col in columns_split])


class Users(Table):

    def __init__(self, name: str, column_sql: str):
        super().__init__(name, column_sql)

    def insert(self, uuid: str, username: str, password: bytes, salt: bytes, latest_balance: float):
        sql = staticfiles.load_static('insert_users.sql', pkg=queries)
        self.query(sql, (uuid, username, password, salt, latest_balance))

    def get_user_by_uuid(self, uuid: str):
        result_set = self.query(f"SELECT * FROM {self.name} WHERE uuid=?", (uuid,))
        return result_set.fetchone()


# Database generic functions #
def connect(db_type: str):
    db_type_import = settings.DB_SYSTEMS.get(db_type)

    if db_type_import is None:
        logging.fatal(f'Could not load the database system {db_type}')
    
    db_module = importlib.import_module(db_type_import)
    return db_module, *db_module.connect(f'database.{db_type}')


def execute_queries(sql: str):
    DB_CURSOR.executescript(sql)
    DB_CONNECTION.commit()


def execute_query(sql: str, task=None):
    result_set = None
    if task is not None:
        result_set = DB_CURSOR.execute(sql, task)
    else:
        result_set = DB_CURSOR.execute(sql)

    DB_CONNECTION.commit()
    return result_set


def execute_from_script(script_query_filename: str, **kwargs):
    sql = staticfiles.load_static(script_query_filename, pkg=queries)
    DB_CURSOR.executescript(sql.format(**kwargs))
    DB_CONNECTION.commit()


def add_row(table_name, items: dict):
    DB_MODULE.add_row(table_name, items)


# Specific Dollarify DB Management #
trades_table = Table('trades', staticfiles.load_static('columns_trades.sql', pkg=queries))
accounts_table = Table('accounts', staticfiles.load_static('columns_accounts.sql', pkg=queries))
account_types_table = Table('account_types', staticfiles.load_static('columns_account_types.sql', pkg=queries))
account_attributes_table = Table('account_attributes', staticfiles.load_static('columns_account_attributes.sql', pkg=queries))
users_table = Users('users', staticfiles.load_static('columns_users.sql', pkg=queries))


def init():

    DB_MODULE.init()
    trades_table.create()
    accounts_table.create()
    account_types_table.create()
    account_attributes_table.create()
    users_table.create()

    account_attributes_table.query_from_script('insert_account_attributes.sql')
    account_types_table.query_from_script('insert_account_types.sql')

    print(users_table.get_user_by_uuid('1'))
    


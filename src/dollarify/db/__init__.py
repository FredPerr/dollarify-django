import importlib
import logging
from dollarify.static import staticfiles
from dollarify.static.db.sqlite3 import queries
from dollarify import settings


class TableModel():

    # __slots__ = ('_name', 'column_sql')

    def __init__(self, name: str, column_sql: str):
        """
        name: name of the table
        columns_sql: columns part of the sql query referencing columns names and attributes. For instance, (uuid VARCHAR(32), name VARCHAR(32))
        """
        if len(name) < 1:
            raise ValueError("The name of the table should be at least one character long.")

        if len(column_sql) < 2 or not column_sql[0] == '(' or not column_sql[-1] == ')':
            raise ValueError("The column_sql should respect the following format: (col_name1 VARCHAR(5), col_name2 DECIMAL(5,2), ...)")
        self._name = name
        self.column_sql = column_sql

    @property
    def name(self):
        return self._name

    def create():
        pass

    def drop():
        pass

    @property
    def columns(self):
        trimmed = self.column_sql[1:-1]
        column_strings = trimmed.split(', ')
        return {k.strip().split(' '):v for k, v in column_strings}
    
    @classmethod
    def _parse_column_sql(cls, sql):
        if sql[0] == '(' and sql[-1] == ')':
            sql = sql[1:-1]
        
        try:
            name, sql_attribs = sql.split(' ', 1)
            sql_type, sql_flags = sql_attribs.strip().split(' ', 1)
            return name, sql_type, sql_flags
        except ValueError:
            logging.error(f'The sql provided "{sql}" does not contain sql attributes.')
    
    @classmethod
    def _parse_columns_sql(cls, sql):
        pass

    @property
    def columns(self, names: bool, types: bool, flags: bool):
        pass

if __name__ == '__main__':
    # t = TableModel('test', '(name VARCHAR(5), amount DECIMAL(5,2))')
    test = TableModel._parse_column_sql('(col_name1 VARCHAR(5))')
    print(test)
    


DB_MODULE, DB_CONNECTION, DB_CURSOR = None, None, None


def connect(db_type: str):
    db_type_import = settings.DB_SYSTEMS.get(db_type)

    if db_type_import is None:
        logging.fatal(f'Could not load the database system {db_type}')
    
    db_module = importlib.import_module(db_type_import)
    return db_module, *db_module.connect(f'database.{db_type}')


def execute_queries(sql: str):
    DB_CURSOR.executescript(sql)
    DB_CONNECTION.commit()


def execute_query(sql: str):
    DB_CURSOR.execute(sql)
    DB_CONNECTION.commit()


def execute_from_script(script_query_filename: str, **kwargs):
    sql = staticfiles.load_static(script_query_filename, pkg=queries)
    DB_CURSOR.executescript(sql.format(**kwargs))
    DB_CONNECTION.commit()


def add_row(table_name, items: dict):
    DB_MODULE.add_row(table_name, items)


# Specific Dollarify DB Management #
TRADES_TABLE = 'trades'
ACCOUNTS_TABLE = 'accounts'
ACCOUNT_TYPES_TABLE = 'account_types'
ACCOUNT_ATTRIBUTES_TABLE = 'account_attributes'
USERS_TABLE = 'users'


def init(**kwargs):
    DB_MODULE.init()
    init_tables(**kwargs)


def init_tables(**kwargs):
    table_names = {
        'TRADES_TABLE': TRADES_TABLE, 
        'ACCOUNTS_TABLE': ACCOUNTS_TABLE, 
        'ACCOUNT_TYPES_TABLE': ACCOUNT_TYPES_TABLE, 
        'ACCOUNT_ATTRIBUTES_TABLE': ACCOUNT_ATTRIBUTES_TABLE, 
        'USERS_TABLE': USERS_TABLE
    }
    execute_from_script('create_tables.sql', **table_names)
    execute_from_script('insert_account_types.sql', ACCOUNT_TYPES_TABLE=ACCOUNT_TYPES_TABLE)
    execute_from_script('insert_account_attributes.sql', ACCOUNT_ATTRIBUTES_TABLE=ACCOUNT_ATTRIBUTES_TABLE)
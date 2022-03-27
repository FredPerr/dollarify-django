import importlib
import logging
from dollarify.static import staticfiles
from dollarify.static.db.sqlite3 import queries
from dollarify import settings


def connect(db_type: str):
    db_type_import = settings.DB_SYSTEMS.get(db_type)

    if db_type_import is None:
        logging.fatal(f'Could not load the database system {db_type}')
    
    db_module = importlib.import_module(db_type_import)
    return db_module, *db_module.connect(f'database.{db_type}')


def execute_queries(sql: str):
    settings.DB_CURSOR.executescript(sql)
    settings.DB_CONNECTION.commit()


def execute_query(sql: str):
    settings.DB_CURSOR.execute(sql)
    settings.DB_CONNECTION.commit()


def execute_from_script(script_query_filename: str, **kwargs):
    sql = staticfiles.load_static(script_query_filename, pkg=queries)
    settings.DB_CURSOR.executescript(sql.format(**kwargs))
    settings.DB_CONNECTION.commit()


def add_row(table_name, items: dict):
    settings.DB_MODULE.add_row(table_name, items)


# Specific Dollarify DB Management #
TRADES_TABLE = 'trades'
ACCOUNTS_TABLE = 'accounts'
ACCOUNT_TYPES_TABLE = 'account_types'
ACCOUNT_ATTRIBUTES_TABLE = 'account_attributes'
USERS_TABLE = 'users'


def init(**kwargs):
    settings.DB_MODULE.init()
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
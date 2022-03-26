import importlib
import logging
import dollarify
from dollarify.static import staticfiles
from dollarify.static.db.sqlite3 import queries
from dollarify import dollarify


def connect(db_type: str):
    db_type_import = dollarify.DB_SYSTEMS.get(db_type)

    if db_type_import is None:
        logging.fatal(f'Could not load the database system {db_type}')
    
    db_module = importlib.import_module(db_type_import)
    return db_module, *db_module.connect(f'database.{db_type}')


def execute_queries(sql: str):
    dollarify.DB_CURSOR.executescript(sql)
    dollarify.DB_CONNECTION.commit()


def execute_query(sql: str):
    dollarify.DB_CURSOR.execute(sql)
    dollarify.DB_CONNECTION.commit()


def execute_from_script(script_query_filename: str, **kwargs):
    sql = staticfiles.load_static(script_query_filename, pkg=queries)
    dollarify.DB_CURSOR.executescript(sql.format(**kwargs))
    dollarify.DB_CONNECTION.commit()


# Specific Dollarify Content Management #
TRADE_TABLE_NAME = 'trades'


def init(**kwargs):
    dollarify.DB_MODULE.init()
    init_tables(**kwargs)


def init_tables(**kwargs):
    scripts = ('create_trade_table.sql', )
    for script in scripts:
        execute_from_script(script, trade_table_name=TRADE_TABLE_NAME, **kwargs)


def add_row(table_name, items: dict):
    dollarify.DB_MODULE.add_row(table_name, items)
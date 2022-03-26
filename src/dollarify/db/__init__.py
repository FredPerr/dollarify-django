import importlib
import logging
from dollarify.static import staticfiles
from dollarify.static.db.sqlite3 import queries


DB_SYSTEMS = {
    'sqlite3': 'dollarify.db.sqlite3',
}

def connect(db_type: str):
    db_type_import = DB_SYSTEMS.get(db_type)

    if db_type_import is None:
        logging.fatal(f'Could not load the database system {db_type}')
    
    db_module = importlib.import_module(db_type_import)
    return db_module, *db_module.connect(f'database.{db_type}')


def execute_queries(connection, cursor, sql: str):
    cursor.executescript(sql)
    connection.commit()


def execute_query(connection, cursor, sql: str):
    cursor.execute(sql)
    connection.commit()


def execute_from_script(connection, cursor, script_query_filename: str, **kwargs):
    sql = staticfiles.load_static(script_query_filename, pkg=queries)
    cursor.executescript(sql.format(**kwargs))
    connection.commit()


# Specific Dollarify Content Management #
TRADE_TABLE_NAME = 'trades'


def init(db_module, connection, cursor, **kwargs):
    db_module.init()
    init_tables(connection, cursor, **kwargs)


def init_tables(connection, cursor, **kwargs):
    scripts = ('create_trade_table.sql', )
    for script in scripts:
        execute_from_script(connection, cursor, script, trade_table_name=TRADE_TABLE_NAME, **kwargs)


def add_row(db_module, connection, table_name, items: dict):
    db_module.add_row(connection, table_name, items)
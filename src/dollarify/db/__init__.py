from importlib.resources import Package, read_text
import logging

import psycopg2
from psycopg2.extensions import connection


from dollarify.static.db.sqlite3 import queries


CONNECTION: connection = None


def execute_script(file_name, package: Package, commit=True):
    cur = CONNECTION.cursor()
    script = read_text(package, file_name)
    cur.execute(script)
    if commit:
        CONNECTION.commit()
    cur.close()


def connect(host: str, database: str, user: str, password: str, port: int = 5432 ,reset_db=False):
    try:
        global CONNECTION
        CONNECTION = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

        # Check for the UUID v4 Functions (extension: uuid-ossp)
        cur = CONNECTION.cursor()
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        cur.execute("SELECT pg_extension.oid FROM pg_extension WHERE pg_extension.extname='uuid-ossp';")
        installed = cur.fetchone() is not None
        cur.close()

        if not installed:
            raise ImportError('The extension uuid-ossp could not be installed.')
    
        if reset_db is True:
            # Initialize the tables
            execute_script('drop_tables.sql', queries)
            execute_script('create_tables.sql', queries)
            execute_script('init_tables.sql', queries)
            logging.info('The database has been reset successfully!')
        else:
            logging.info('The database reset was aborted.')

        logging.debug(f'Running on {version()}')
    except (psycopg2.DatabaseError) as error:
        logging.error(error)
        

def close():
    if CONNECTION is not None:
        CONNECTION.close()
        logging.debug(f"DB connection terminated.")


def version():
    cur = CONNECTION.cursor()
    cur.execute("SELECT version();")
    response = cur.fetchone()
    cur.close()
    assert response is not None, 'Could not retrieve the version of the database!'
    return response[0]


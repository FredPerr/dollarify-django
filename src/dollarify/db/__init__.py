import codecs
from importlib.resources import Package, read_text
import logging
import psycopg2
from configparser import ConfigParser

from dollarify.static.db.sqlite3 import queries
from dollarify.utils import hashing




def db_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


class DB:

    CONNECTION = None

    def __init__(self):
        raise NotImplementedError("No instance of this class should be created.")

    def connect(host: str, database: str, user: str, password: str, port: int = 5432):
        try:
            DB.CONNECTION = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            cur = DB.CONNECTION.cursor()
            cur.execute('SELECT version();')

            logging.debug(f'Running on {cur.fetchone()[0]}')
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        

    def close():
        if DB.CONNECTION is not None:
            DB.CONNECTION.close()
            logging.debug(f"DB connection terminated.")

    def execute_script(file_name, package: Package, commit=True):
        cur = DB.CONNECTION.cursor()
        script = read_text(package, file_name)
        cur.execute(script)
        if commit:
            DB.CONNECTION.commit()
        cur.close()

    


####################################
# Specific Dollarify DB Management #
####################################

def init():

    # Check for the UUID v4 Functions (extension: uuid-ossp)
    cur = DB.CONNECTION.cursor()
    cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    cur.execute("SELECT pg_extension.oid FROM pg_extension WHERE pg_extension.extname='uuid-ossp';")
    installed = cur.fetchone() is not None
    cur.close()

    if not installed:
        logging.error('The extension uuid-ossp could not be installed.')

    # Initialize the tables
    # DB.execute_script('drop_tables.sql', queries)
    # DB.execute_script('create_tables.sql', queries)
    # DB.execute_script('init_tables.sql', queries)

    from .users import insert, get
    # insert('frederic.perr@gmail.com', 'Frédéric', 'Perron', 'This is a test', '418-111-1111')
    value = get('frederic.perr@gmail.com')
    print(value)
    
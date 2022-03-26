import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DB_SYSTEMS = {
    'sqlite3': 'dollarify.db.sqlite3',
}

DB_MODULE, DB_CONNECTION, DB_CURSOR = None, None, None
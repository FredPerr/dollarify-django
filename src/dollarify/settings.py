import os

DEBUG = True


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DB_SYSTEMS = {
    'sqlite3': 'dollarify.db.sqlite3',
}
import os


# App name lowercased 
APP_NAME = 'dollarify'

# The Flask Application reference.
FLASK_APP = 'dollarify.dollarify.app'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DB = {
    'HOST': 'localhost',
    'NAME': os.environ['DB_NAME'],
    'USER': os.environ['DB_USER'],
    'PASSWORD': os.environ['DB_PASSWORD'],
    'PORT': 5432 # Default port is 5432. This port should be changed.
}


FLASK_SERVER = {
    'PORT': 8000,
    'HOST': 'localhost',
    'CSRF_ENABLED': True,
}


SECRET_KEY = os.environ['SECRET_KEY']


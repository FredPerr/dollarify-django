from dollarify.utils import config


FLASK_CONFIG = config.load('config.ini', 'flask')
DB_CONFIG = config.load('config.ini', 'postgresql')

FLASK_APP = 'dollarify.dollarify.app'
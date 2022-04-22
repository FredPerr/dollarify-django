import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dollarify import views
from dollarify import settings


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def create_app():

    a = Flask(
        import_name="dollarify", 
        static_folder=os.path.join(BASE_DIR, 'dollarify/static'), 
        template_folder=os.path.join(BASE_DIR, 'dollarify/templates'),
    )
    secret_key_value = os.getenv(settings.FLASK_CONFIG['secret_key'])
    a.config['SECRET_KEY'] = secret_key_value
    a.config['SQLALCHEMY_DATABASE_URI'] = os.environ[settings.DB_CONFIG['sqlalchemy_db_uri']]
    a.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    views.register_blueprints(a)
    views.register_error_handlers(a)
    
    return a
    

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
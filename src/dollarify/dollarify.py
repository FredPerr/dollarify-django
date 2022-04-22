import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dollarify import views
from dollarify import settings


def create_app():

    DB = settings.DB

    a = Flask(
        import_name="dollarify", 
        static_folder=os.path.join(settings.BASE_DIR, 'dollarify/static'), 
        template_folder=os.path.join(settings.BASE_DIR, 'dollarify/templates'),
    )

    a.config['SECRET_KEY'] = settings.SECRET_KEY
    a.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB['USER']}:{DB['PASSWORD']}@{DB['HOST']}/{DB['NAME']}"
    a.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    views.register_blueprints(a)
    views.register_error_handlers(a)
    return a
    

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
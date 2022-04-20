import os

from flask import Flask
from dollarify import views


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = None


def create_app(*, db_config, flask_config) -> Flask:
    
    application = Flask(
        import_name="dollarify", 
        static_folder=os.path.join(BASE_DIR, 'dollarify/static'), 
        template_folder=os.path.join(BASE_DIR, 'dollarify/templates'),
    )

    application.config['SECRET_KEY'] = os.getenv(flask_config['SECRET_KEY'])

    print(application.template_folder)

    views.register_blueprints(application)
    views.register_error_handlers(application)
    
    return application
from os import path

from flask import Flask
from dollarify import views


BASE_DIR = path.dirname(path.dirname(__file__))

app = None


def create_app(*, db_config, flask_config) -> Flask:
    
    application = Flask(
        import_name="dollarify", 
        static_folder=path.join(BASE_DIR, 'dollarify/static'), 
        template_folder=path.join(BASE_DIR, 'dollarify/templates')
    )

    print(application.template_folder)

    views.register_blueprints(application)
    views.register_error_handlers(application)
    
    return application
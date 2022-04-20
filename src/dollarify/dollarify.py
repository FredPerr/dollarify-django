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
    secret_key_value = os.getenv(flask_config['secret_key'])
    application.config['SECRET_KEY'] = secret_key_value
    print(secret_key_value) # TODO: Test if the variable works after OS reload.

    views.register_blueprints(application)
    views.register_error_handlers(application)
    
    return application
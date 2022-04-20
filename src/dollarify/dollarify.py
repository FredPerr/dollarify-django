from flask import Flask, Blueprint
from dollarify import views


app = None


def create_app(*, db_config, flask_config) -> Flask:
    
    application = Flask("dollarify")
    
    views.register_blueprints(application)
    views.register_error_handlers(application)
    
    return application
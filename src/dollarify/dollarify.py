from flask import Flask

from dollarify import views
from dollarify.views import http_codes


app = None

def create_app(*, db_config, flask_config):
    application =  Flask("dollarify")
    application.register_blueprint(views.home_bp)
    application.register_blueprint(http_codes.errors_bp)
    return application

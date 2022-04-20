from flask import Flask


app = None

def create_app(*, db_config, flask_config):
    return Flask("dollarify")

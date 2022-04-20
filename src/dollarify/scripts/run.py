import os

import click

from dollarify.utils import config
from dollarify import dollarify


@click.command()
@click.option('-d', '--debug', is_flag=True, default=False, help='Active the debug mode while running')
@click.option('-p', '--production', is_flag=True, default=False, help='Active the production mode while running')
def cli(debug, production):

    postgresql_config = config.load('config.ini', 'postgresql')
    flask_config = config.load('config.ini', 'flask')

    if not production:
        os.environ['FLASK_ENV'] = 'development'

    dollarify.app = dollarify.create_app(db_config=postgresql_config, flask_config=flask_config)
    dollarify.app.run(host=flask_config['host'], port=flask_config['port'], debug=debug)

    

    
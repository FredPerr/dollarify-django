import os

import click

from dollarify import dollarify
from dollarify.scripts import main



@main.cli.command(name='run')
@click.option('-d', '--debug', is_flag=True, default=False, help='Active the debug mode while running')
@click.option('-p', '--production', is_flag=True, default=False, help='Active the production mode while running')
def cli(debug, production):

    from dollarify import settings
    
    os.environ['FLASK_APP'] = settings.FLASK_APP
    if not production:
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_APP'] = 'dollarify'

    dollarify.app = dollarify.create_app()
    dollarify.app.run(host=settings.DB['HOST'], port=settings.FLASK_SERVER['PORT'], debug=debug)


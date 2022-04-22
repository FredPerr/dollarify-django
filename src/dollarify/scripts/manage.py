import os

import click
from flask_migrate.cli import db


@click.group()
def cli():
    pass


@cli.command(name='secret-key')
@click.option('--length', default=16, show_default=True, help='Generate a SECRET KEY for Flask')
def secret_key(length):
    click.secho(os.urandom(length).hex(), fg='green')


cli.add_command(db)


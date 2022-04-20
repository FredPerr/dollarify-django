import os

import click


@click.command()
@click.option('--length', default=16, show_default=True, help='Generate a SECRET KEY for Flask')
def cli(length):
    click.echo(os.urandom(length).hex())

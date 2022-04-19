import logging
import sys
import argparse
import os


from dollarify import db
from dollarify import app
from dollarify.utils import config
from dollarify.debug import debug




def main():

    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='Dollarify', description='Dollarify main command interface')
    parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction, help='Activate the debug mode')
    parser.add_argument('--reset-db', '-rdb', action=argparse.BooleanOptionalAction, help='Reset the database')
    parser.add_argument('run', action='store_true', help='Start the development server of the flask api after running the DB initialisation.')
    args = parser.parse_args(args)

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    
    db.connect(**config.load('database.ini', 'postgresql'), reset_db=args.reset_db)

    if args.debug:
        debug()

    if args.run:
        os.environ['FLASK_ENV'] = 'development'
        app.run(**config.load('website.ini', 'website'), debug=args.debug)


    if db.CONNECTION is not None:
        db.close()


main()
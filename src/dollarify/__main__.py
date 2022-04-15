import logging
import sys
import argparse

from dollarify.db import Database, SQLiteDB, init
from dollarify import api


def test():
    pass

def connect(test_enabled: bool):
    Database.connect(SQLiteDB, 'database.sqlite3')
    init()
    if test_enabled:
        logging.debug('*** Running the test function ***')
        test()
        logging.debug('*** Done with the test function ***')


def main():
    logging.basicConfig(level=logging.DEBUG if namespace.debug else logging.INFO)

    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='Dollarify', description='Dollarify main command interface')
    parser.add_argument('--test', '-t', action=argparse.BooleanOptionalAction, help='Activate the test mode')
    parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction, help='Activate the debug mode')
    parser.add_argument('--api', '-a', action=argparse.BooleanOptionalAction, help='Run the flask api')
    parser.add_argument('run', action='store_true', help='Start the development server of the flask api.')
    namespace = parser.parse_args(args)

    mode = {
        'test': namespace.test,
        'debug': namespace.debug,
        'api': namespace.api,
    }

    if namespace.run:
        mode['api'] = True
        mode['debug'] = True

    connect(namespace.test)

    if namespace.api:
        api.app.run(port=8080, debug=namespace.debug)


    if Database is not None:
        Database.close()


main()
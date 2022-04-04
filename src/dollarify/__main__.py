import logging
import sys
import argparse

from dollarify.db import Database, SQLiteDB, init
from dollarify import settings
from dollarify.db import users


from dollarify.dollarify import User

def test():
    # TODO: Can't getch the user after creation
    user = User.create_and_fetch('test', 'Fred09Fred09', 599)

def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='Dollarify', description='Manage Dollarify CLI')
    parser.add_argument('--test', '-t', action=argparse.BooleanOptionalAction, help='Activate the test mode')
    parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction, help='Activate the debug mode')
    namespace = parser.parse_args(args)
    
    logging.basicConfig(level=logging.DEBUG if namespace.debug else logging.INFO)

    try:
        Database.connect(SQLiteDB, 'database.sqlite3')
        init()
        if namespace.test:
            logging.debug('*** Running the test function ***')
            test()
            logging.debug('*** Done with the test function ***')
    except Exception as e:
        logging.error(e)
    finally:
        if Database is not None:
            Database.close()


main()
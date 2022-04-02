import logging
import sys
import argparse

from dollarify.db import Database, SQLiteDB, init
from dollarify import settings


def test():
    pass

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
        Database.close()


main()
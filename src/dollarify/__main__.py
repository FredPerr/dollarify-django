from ast import alias, arg
import logging
import sys
import argparse

from dollarify.db import Database, SQLiteDB
from dollarify import settings


def test():
    pass

def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='Dollarify', description='Manage Dollarify CLI')
    parser.add_argument('--test', '-t', action=argparse.BooleanOptionalAction, help='Activate the test mode')
    namespace = parser.parse_args(args)
    

    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(level=log_level)

    try:
        Database.connect(SQLiteDB, 'database.sqlite3')
        if namespace.test is True:
            logging.debug('*** Running the test function ***')
            test()
            logging.debug('*** Done with the test function ***')
    except Exception as e:
        logging.error(e)
    finally:
        Database.close()


main()
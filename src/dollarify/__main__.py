import logging
import sys
import argparse

from dollarify.db import Database, SQLiteDB, init
from dollarify.models import IntegerField



def test():
    test = IntegerField('test', 30, True, nullable=False)
    print(test.attributes_db)

def connect(test_enabled: bool):
    Database.connect(SQLiteDB, 'database.sqlite3')
    init()
    if test_enabled:
        logging.debug('*** Running the test function ***')
        test()
        logging.debug('*** Done with the test function ***')


def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='Dollarify', description='Manage Dollarify CLI')
    parser.add_argument('--test', '-t', action=argparse.BooleanOptionalAction, help='Activate the test mode')
    parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction, help='Activate the debug mode')
    namespace = parser.parse_args(args)
    
    logging.basicConfig(level=logging.DEBUG if namespace.debug else logging.INFO)

    connect(namespace.test)

    # Do some other stuff here.

    if Database is not None:
        Database.close()


main()
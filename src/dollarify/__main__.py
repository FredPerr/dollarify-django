import logging
import sys
import argparse

from dollarify.core import Profile
from dollarify.db import Database, SQLiteDB, init


def test():
    # Trade.create(Trade, uuid.generate(), 'APPL', None, 3, 100.01, 0.00, None, None)
    # User.create(User, uuid.generate(), 'Test', 'Test123', 0.0)
    profile = Profile('82addfde9c254b48a65efad439a790b8')
    print(profile.accounts)    


def connect(test_enabled: bool):
    Database.connect(SQLiteDB, 'database.sqlite3')
    init()
    if test_enabled:
        logging.debug('*** Running the test function ***')
        test()
        logging.debug('*** Done with the test function ***')


def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog='Dollarify', description='Dollarify main command interface')
    parser.add_argument('--test', '-t', action=argparse.BooleanOptionalAction, help='Activate the test mode')
    parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction, help='Activate the debug mode')
    namespace = parser.parse_args(args)
    
    logging.basicConfig(level=logging.DEBUG if namespace.debug else logging.INFO)

    connect(namespace.test)

    # Do some other stuff here.

    if Database is not None:
        Database.close()


main()
import logging
import sys
import argparse
import random

from dollarify.db import Database, SQLiteDB, init
from dollarify.models import User


def test():
    user = User('1325434640164da2bc35f55e86fd3c29')
    # user.username = 'Jeremy'
    # user.push()

    user2 = User('1325434640164da2bc35f55e86fd3c29')

    print(id(user))
    print(id(user2))

    print(user2._username)

    


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
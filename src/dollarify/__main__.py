import logging
from datetime import datetime, timezone
import sqlite3

from dollarify import db
from dollarify.utils import time
from dollarify.utils import uuid


def main():

    connection = None
    try:
        db_module, connection, cursor = db.connect('sqlite3')
        db.init(connection, cursor)
        attribs = {
            'user_id': uuid.generate(),
            'account': uuid.generate(),
            'ticker': 'MSFT',
            'buy_date': time.now(),
            ''
             # TODO continue to add the row to the db.


        }

        # db.add_row(connection, cursor, 'trades')


    except Exception as e:
        logging.error(e)
    finally:
        if connection:
            connection.close()


main()
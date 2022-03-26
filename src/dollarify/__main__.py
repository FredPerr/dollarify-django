import logging

from dollarify import db
from dollarify.utils import time
from dollarify.utils import uuid


def main():
    DEBUG = True
    connection = None
    try:
        db_module, connection, cursor = db.connect('sqlite3')
        db.init(db_module, connection, cursor)
        attribs = {
            'user_id': uuid.generate(),
            'account': uuid.generate(),
            'ticker': 'MSFT',
            'buy_date': time.now(),
            'shares': 30,
            'buy_value': 15.30,
            'fees': 0.00,
            'sell_value': None,
            'sell_date': None
        }

        if DEBUG:
            connection.set_trace_callback(print)

        db.add_row(db_module, connection, db.TRADE_TABLE_NAME, attribs)


    except Exception as e:
        logging.error(e)
    finally:
        if connection:
            connection.close()


main()
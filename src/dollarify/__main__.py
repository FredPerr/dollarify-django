import logging

from dollarify import db
from dollarify.utils import time
from dollarify.utils import uuid
from dollarify import dollarify


def main():
    DEBUG = True
    try:
        dollarify.DB_MODULE, dollarify.DB_CONNECTION, dollarify.DB_CURSOR = db.connect('sqlite3')
        db.init()
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
            dollarify.DB_CONNECTION.set_trace_callback(print)

        db.add_row(db.TRADE_TABLE_NAME, attribs)


    except Exception as e:
        logging.error(e)
    finally:
        if dollarify.DB_CONNECTION:
            dollarify.DB_CONNECTION.close()


main()
import logging

from dollarify import db
from dollarify.utils import time
from dollarify.utils import uuid, hashing
from dollarify import dollarify

def test():
    pass


def main():
    DEBUG = True
    try:
        dollarify.DB_MODULE, dollarify.DB_CONNECTION, dollarify.DB_CURSOR = db.connect('sqlite3')
        db.init()
        if DEBUG:
            test()
            dollarify.DB_CONNECTION.set_trace_callback(print)
    except Exception as e:
        logging.error(e)
    finally:
        if dollarify.DB_CONNECTION:
            dollarify.DB_CONNECTION.close()


main()
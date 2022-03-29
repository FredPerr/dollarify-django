import logging

from dollarify import db


def test():
    pass


def main():
    DEBUG = True
    try:
        db.DB_MODULE, db.DB_CONNECTION, db.DB_CURSOR = db.connect('sqlite3')
        db.init()
        if DEBUG:
            test()
            db.DB_CONNECTION.set_trace_callback(print)
    except Exception as e:
        logging.error(e)
    finally:
        if db.DB_CONNECTION:
            db.DB_CONNECTION.close()


main()
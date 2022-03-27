import logging

from dollarify import db
from dollarify import settings

def test():
    pass


def main():
    DEBUG = True
    try:
        settings.DB_MODULE, settings.DB_CONNECTION, settings.DB_CURSOR = db.connect('sqlite3')
        db.init()
        if DEBUG:
            test()
            settings.DB_CONNECTION.set_trace_callback(print)
    except Exception as e:
        logging.error(e)
    finally:
        if settings.DB_CONNECTION:
            settings.DB_CONNECTION.close()


main()
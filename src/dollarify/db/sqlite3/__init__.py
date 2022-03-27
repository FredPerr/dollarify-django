import logging
import sqlite3
from datetime import time as datetime_time
from dollarify import settings
from dollarify.utils.time import time_adapter


def init():
    sqlite3.register_adapter(datetime_time, time_adapter)


def is_connected() -> bool:
    if settings.DB_CONNECTION is not None and isinstance(settings.DB_CONNECTION, sqlite3.Connection):
        try:
            settings.DB_CONNECTION.cursor()
            return True
        except Exception:
            return False

def connect(db_path: str):
    connection = sqlite3.connect(db_path)
    return connection, connection.cursor()


def close():
    if is_connected(settings.DB_CONNECTION):
        settings.DB_CONNECTION.close()


def add_row(table_name, items: dict):
    columns = str(tuple(items.keys())).replace("\'", "")
    values = ('?, ' * len(items.keys())).strip(', ') 
    settings.DB_CURSOR.execute(f"INSERT INTO {table_name} {columns} VALUES({values});", tuple(items.values()))
    settings.DB_CONNECTION.commit()

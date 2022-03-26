import logging
import sqlite3
from datetime import time as datetime_time
from dollarify import dollarify
from dollarify.utils.time import time_adapter


def init():
    sqlite3.register_adapter(datetime_time, time_adapter)


def is_connected() -> bool:
    if dollarify.DB_CONNECTION is not None and isinstance(dollarify.DB_CONNECTION, sqlite3.Connection):
        try:
            dollarify.DB_CONNECTION.cursor()
            return True
        except Exception:
            return False

def connect(db_path: str):
    connection = sqlite3.connect(db_path)
    return connection, connection.cursor()


def close():
    if is_connected(dollarify.DB_CONNECTION):
        dollarify.DB_CONNECTION.close()


def add_row(table_name, items: dict):
    columns = str(tuple(items.keys())).replace("\'", "")
    values = ('?, ' * len(items.keys())).strip(', ') 
    dollarify.DB_CURSOR.execute(f"INSERT INTO {table_name} {columns} VALUES({values});", tuple(items.values()))
    dollarify.DB_CONNECTION.commit()

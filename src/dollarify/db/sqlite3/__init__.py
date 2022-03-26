import logging
import sqlite3
from datetime import time as datetime_time
from dollarify.utils.time import time_adapter


def init():
    sqlite3.register_adapter(datetime_time, time_adapter)


def is_connected(connection) -> bool:
    if connection is not None and isinstance(connection, sqlite3.Connection):
        try:
            connection.cursor()
            return True
        except Exception:
            return False

def connect(db_path: str):
    connection = sqlite3.connect(db_path)
    return connection, connection.cursor()


def close(connection):
    if is_connected(connection):
        connection.close()


def add_row(connection, table_name, items: dict):
    columns = str(tuple(items.keys())).replace("\'", "")
    values = ('?, ' * len(items.keys())).strip(', ') 
    try:
        print(values)
        print(columns)
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {table_name} {columns} VALUES({values});", tuple(items.values()))
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        logging.error(f'Could not insert the new row! {error}')
    finally:
        if connection:
            connection.close()

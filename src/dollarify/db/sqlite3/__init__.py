from pathlib import Path
import sqlite3


def init():
    


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


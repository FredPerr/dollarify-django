# import sqlite3
# from datetime import time as datetime_time
# from dollarify.utils.time import time_adapter
# from dollarify import db


# def init():
#     sqlite3.register_adapter(datetime_time, time_adapter)


# def is_connected() -> bool:
#     if db.DB_CONNECTION is not None and isinstance(db.DB_CONNECTION, sqlite3.Connection):
#         try:
#             db.DB_CONNECTION.cursor()
#             return True
#         except Exception:
#             return False


# def connect(db_path: str):
#     connection = sqlite3.connect(db_path)
#     return connection, connection.cursor()


# def close():
#     if is_connected(db.DB_CONNECTION):
#         db.DB_CONNECTION.close()


# def add_row(table_name, items: dict):
#     columns = str(tuple(items.keys())).replace("\'", "")
#     values = ('?, ' * len(items.keys())).strip(', ') 
#     db.DB_CURSOR.execute(f"INSERT INTO {table_name} {columns} VALUES({values});", tuple(items.values()))
#     db.DB_CONNECTION.commit()

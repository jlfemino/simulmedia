import sqlite3

# TODO: Add support for connection pooling


class BaseDao:
    db_file_path: str = None

    def __init__(self, db_file_path: str):
        self.db_file_path = db_file_path

    def get_connection(self):
        return sqlite3.connect(self.db_file_path)

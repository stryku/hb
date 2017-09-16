import sqlite3 as lite
from enum import Enum

DB_FILE = 'db/database.db'
RECEIPTS_TABLE = 'Receipts'
EXTRACTED_RECEIPTS_TEXTS_TABLE = 'ExtractedReceiptTexts'


class ReceiptStatus(Enum):
    EXTRACTED = 0
    CORRECTED = 1
    CLOSED = 2


class ExtractedReceiptTextStatus(Enum):
    NOT_MERGED = 0
    MERGED = 1


class Db:
    def __init__(self):
        self.db = lite.connect(DB_FILE)
        self.cur = self.db.cursor()
        self.execute('''CREATE TABLE IF NOT EXISTS ''' + RECEIPTS_TABLE + '''
            (
            id INTEGER PRIMARY KEY,
            name varchar(255),
            oryginal_name varchar(255),
            status int DEFAULT 0
            );''')
        self.execute('''CREATE TABLE IF NOT EXISTS ''' + EXTRACTED_RECEIPTS_TEXTS_TABLE + '''
            (
            id INTEGER PRIMARY KEY,
            receipt_id int,
            txt text,
            status int DEFAULT 0
            );''')

    def execute(self, command):
        if not command.endswith(';'):
            command += ';'

        self.cur.execute(command)
        self.db.commit()

    def close(self):
        self.db.close()

    def last_id(self):
        return self.cur.lastrowid

    def get_cur(self):
        return self.cur

    def commit(self):
        self.db.commit()


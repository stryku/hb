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
        self.db.row_factory = lite.Row
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

    def fetchall(self):
        return self.cur.fetchall()


class NotFoundInDbException(Exception):
    pass


class DbDataGetter:
    @staticmethod
    def get_row(table, id, search_by_column='id'):
        db = Db()
        db.execute("select * from " + table + " where " + search_by_column + "=" + id)
        data = db.fetchall()
        if len(data) == 0:
            db.close()
            raise NotFoundInDbException()

        db.close()
        return data[0]

    @staticmethod
    def get_field(table, column, id, search_by_column='id'):
        row = DbDataGetter.get_row(table, id, search_by_column)
        return row[column]

import sqlite3 as lite
from enum import Enum
from database.tables import CreationQueryFactory
from database.table_type import TableType

DB_FILE = 'db/database.db'


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
        self._create_tables()

    @staticmethod
    def _add_semicolon(command):
        if not command.endswith(';'):
            command += ';'

        return command

    def _create_table(self, metadata):
        self.execute(metadata.get_creation_query())

    def _create_tables(self):
        for table_type in TableType:
            self._create_table(CreationQueryFactory.create(table_type))

    def execute(self, command):
        command = Db._add_semicolon(command)
        self.cur.execute(command)
        self.db.commit()

    def execute_escaped(self, command, escaped):
        command = Db._add_semicolon(command)
        self.cur.execute(command, escaped)
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


class DbDataUpdater:
    @staticmethod
    def update_field(table, column, data, key, key_column='id'):
        db = Db()
        db.execute_escaped("update " + table + " set " + column + "=? where " + key_column + "=?", (data, key))
        db.close()

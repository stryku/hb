import sqlite3 as lite
from enum import Enum

DB_FILE = 'db/database.db'


class ReceiptStatus(Enum):
    EXTRACTED = 0
    CORRECTED = 1
    CLOSED = 2


class ExtractedReceiptTextStatus(Enum):
    NOT_MERGED = 0
    MERGED = 1


def init(db):
    db.execute('''CREATE TABLE IF NOT EXISTS Receipt
(
id int PRIMARY KEY,
recv_time timestamp,
name varchar(255),
status int
);''')
    db.execute('''CREATE TABLE IF NOT EXISTS ExtractedReceiptTexts
(
id int PRIMARY KEY,
receipt_id int,
txt text,
status int
);''')


def connect():
    db = lite.connect(DB_FILE)
    init(db)
    return db

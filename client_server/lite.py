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
id INTEGER PRIMARY KEY,
name varchar(255),
oryginal_name varchar(255),
status int DEFAULT 0
);''')
    db.execute('''CREATE TABLE IF NOT EXISTS ExtractedReceiptTexts
(
id INTEGER PRIMARY KEY,
receipt_id int,
txt text,
status int DEFAULT 0
);''')


def connect():
    db = lite.connect(DB_FILE)
    init(db)
    return db

from enum import Enum


class TableType(Enum):
    RECEIPTS = 0,
    EXTRACTED_RECEIPTS_TEXTS = 1


class ReceiptTableMetadata:
    @staticmethod
    def get_name():
        return 'Receipts'

    @staticmethod
    def get_creation_query():
        return '''CREATE TABLE IF NOT EXISTS {}
            (
                id INTEGER PRIMARY KEY,
                name varchar(255),
                original_name varchar(255),
                status int DEFAULT 0
            );'''.format(ReceiptTableMetadata.get_name())


class ExtractedReceiptsTextsTableMetadata:
    @staticmethod
    def get_name():
        return 'ExtractedReceiptTexts'

    @staticmethod
    def get_creation_query():
        return '''CREATE TABLE IF NOT EXISTS {}
            (
            id INTEGER PRIMARY KEY,
            receipt_id int,
            txt text,
            status int DEFAULT 0
            );'''.format(ExtractedReceiptsTextsTableMetadata.get_name())


class TablesMetadataFactory:
    @staticmethod
    def create(type):
        return {
            TableType.RECEIPTS: ReceiptTableMetadata(),
            TableType.EXTRACTED_RECEIPTS_TEXTS: ExtractedReceiptsTextsTableMetadata(),
        }[type]

from database.table_type import TableType


class ReceiptTableMetadata:
    @staticmethod
    def get_columns():
        return [
            'id INTEGER PRIMARY KEY',
            'name varchar(255)',
            'original_name varchar(255)',
            'status int DEFAULT 0'
        ]

    @staticmethod
    def get_name():
        return 'Receipts'


class ExtractedReceiptsTextsTableMetadata:
    @staticmethod
    def get_columns():
        return [
            'id INTEGER PRIMARY KEY',
            'receipt_id int',
            'txt text',
            'status int DEFAULT 0'
        ]

    @staticmethod
    def get_name():
        return 'ExtractedReceiptTexts'


class TablesMetadataFactory:
    @staticmethod
    def create(table_type):
        return {
            TableType.RECEIPTS: ReceiptTableMetadata(),
            TableType.EXTRACTED_RECEIPTS_TEXTS: ExtractedReceiptsTextsTableMetadata()
        }[table_type]
